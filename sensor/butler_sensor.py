import sys
import signal
import logging
import json
import time
import threading
import paho.mqtt.client as mqtt
from hcsr04sensor import sensor

FIRMWARE = 'RABCBot 2019-02-16 7AM'
CONFIG_FILE = 'butler_sensor.json'
LOGGER_FILE = 'butler_sensor.log'

def handle_exit(sig, frame):
    raise(SystemExit)

signal.signal(signal.SIGTERM, handle_exit)

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=LOGGER_FILE,
                    filemode='w')
_LOGGER = logging.getLogger(__name__)

class Config():
    def __init__(self, filename):
        self._json = {}
        try:        
            with open(filename, 'r') as f:
                self._json = json.load(f)
        except IOError as ex:
            _LOGGER.error('Failed to read configuration file, because %s', ex)
            raise

    @property
    def Json(self):
        return self._json

    def Write(self, filename):
        try:
            with open(filename, 'w') as f:
                json.dump(self._json, f)
        except IOError as ex:
            _LOGGER.error('Failed to write configuration file, because %s', ex)
            raise


class Mqtt():

    def __init__(self, host, topic):
        self._client = mqtt.Client()
        self._topic_prefix = topic
        self._client.on_connect = self.top_on_connect
        self._client.on_message = self.top_on_message
        self._client.connect(host, 1883, 60)
        self._on_connect = None
        self._on_message = None

    def __del__(self):
        self.stop()

    def start(self, forever):
        _LOGGER.debug('Mqtt loop starting...')
        if forever:
            self._client.loop_forever()
        else:
            self._client.loop_start()

    def stop(self):
        _LOGGER.debug('Mqtt loop stopping...')
        self._client.loop_stop()

    @property
    def on_connect(self):
        return self._on_connect

    @on_connect.setter
    def on_connect(self, func):
        self._on_connect = func

    def top_on_connect(self, client, userdata, flags, rc):
        _LOGGER.debug('Mqtt connected')
        self._client.subscribe(self._topic_prefix + 'set/#')
        self._client.subscribe(self._topic_prefix + 'get/#')
        self._client.subscribe(self._topic_prefix + 'cmd/#')
        self._client.subscribe('home/status')
        if self._on_connect is not None:
            self._on_connect(client, userdata, flags, rc)

    @property
    def on_message(self):
        return self._on_message

    @on_message.setter
    def on_message(self, func):
        self._on_message = func

    def top_on_message(self, client, userdata, msg):
        _LOGGER.debug('Message received: %s, payload: %s', msg.topic, msg.payload.decode('ascii'))
        if self._on_message is not None:
            self._on_message(client, userdata, msg)

    def publish(self, topic, payload):
        self._client.publish(self._topic_prefix + topic, payload)

class Worker():

    def __init__(self, config):
        self._prev_presence = None
        self._prev_time = time.time()
        # config parameters
        self._trigger_pin = config['trigger_pin']
        self._echo_pin = config['echo_pin']
        self._sensor_temperature = config['sensor_temperature']
        self._distance_threshold =  config['distance_threshold']
        self._unit_system =  config['unit_system']
        self._publish_distance = config['publish_distance']
        self._working = False
        self._sleep_time = config['sleep_time']
        self._refresh_time = config['refresh_time']
        # Mqtt
        self._mqtt = Mqtt(config['mqtt_host'], config['topic_prefix'])
        self._mqtt.on_message = self.on_message
        self._mqtt.start(False)
        # Distance sensor
        self._sensor = sensor.Measurement(self._trigger_pin,
                                          self._echo_pin,
                                          temperature = self._sensor_temperature,
                                          unit = self._unit_system,
                                          round_to=2)
        _LOGGER.debug('Worker initialized')

    def on_message(self, client, userdata, msg):
        if msg.topic == 'home/status':
            self.send_status()
        t = msg.topic.rsplit('/', 2)
        verb = t[1]
        key = t[2]
        value = msg.payload.decode('ascii')
        if verb == 'set':
            self.set_config(key, value)
        if verb == 'cmd':
            self.run_command(key, value)

    def send_status(self):
        self._mqtt.publish('firmware', FIRMWARE)
        self._mqtt.publish('trigger_pin', self._trigger_pin)
        self._mqtt.publish('echo_pin', self._echo_pin)
        self._mqtt.publish('sensor_temperature', self._sensor_temperature)
        self._mqtt.publish('unit_system', self._unit_system)
        self._mqtt.publish('distance_threshold', self._distance_threshold)
        self._mqtt.publish('publish_distance', self._publish_distance)
        self._mqtt.publish('sleep_time', self._sleep_time)
        self._mqtt.publish('refresh_time', self._refresh_time)

    def set_config(self, key, value):
        if key == 'trigger_pin':
            self._trigger_pin = int(value)
        if key == 'echo_pin':
            self._echo_pin = int(value)
        if key == 'sensor_temperature':
            self._sensor_temperature = int(value)
        if key == 'unit_system':
            self._unit_system =  value
        if key == 'distance_threshold':
            self._distance_threshold = round(float(value))
        if key == 'publish_distance':
            self._publish_distance = (value == 'True')
        if key == 'sleep_time':
            self._sleep_time = int(value)
        if key == 'refresh_time':
            self._refresh_time = int(value)
        self._mqtt.publish(key, value)


    def run_command(self, key, value):
        if key == 'start':
            self.start()
        if key == 'pause':
            self.pause()
        #if key == 'write':
        #    self.write_config()


    def start(self):
        if self._working == False:
            self._working = True
            self.work()

    def pause(self):
        if self._working == True:
            self._working = False

    def work(self):
        distance = 0
        presence = None
       
        while True:
            try:
                if self._working:
                    distance = self.read_distance()
                    _LOGGER.debug('Distance %s', distance)
                    if self._publish_distance:
                        self._mqtt.publish('distance', distance)
                    if distance < self._distance_threshold:
                        presence = 'ON'
                    else:
                        presence = 'OFF'
                    _LOGGER.debug('Presence %s', presence)
                    if presence != self._prev_presence or time.time() - self._prev_time > self._refresh_time:
                        self._mqtt.publish('presence', presence)
                        self._prev_presence = presence
                        self._prev_time = time.time()
                time.sleep(self._sleep_time)
            except (KeyboardInterrupt, SystemExit):
                self._mqtt.stop()
                _LOGGER.debug('Worker stopped')
                sys.exit()
            except (UnboundLocalError, SystemError, RuntimeError):
                pass
            except Exception as ex:
                _LOGGER.error(str(ex))
                raise
                

    def read_distance(self):
        raw = self._sensor.raw_distance()
        if self._unit_system == 'imperial':
            return self._sensor.distance_imperial(raw)
        if self._unit_system == 'metric':
            return self._sensor.distance_metric(raw)

if __name__ == "__main__":
    # print(sys.argv[0])
    c = Config(CONFIG_FILE)
    w = Worker(c.Json)
    w.start()


