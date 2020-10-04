import sys
import signal
import logging
import json
import time
import threading
import paho.mqtt.client as PahoMqtt
from hcsr04sensor import sensor

FIRMWARE = 'RABCBot 2019-02-19 8:20AM'
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
        self._filename = filename
        self._modified = False
        try:
            with open(filename, 'r') as f:
                self._json = json.load(f)
        except IOError as ex:
            _LOGGER.error('Failed to read configuration file, because %s', ex)
            raise

    def get(self, name):
        return self._json[name]

    def set(self, name, value):
        self._json[name] = value
        self._modified = True

    def write(self):
        if self._modified:
            try:
                with open(self._filename, 'w') as f:
                    json.dump(self._json, f)
                    self._modified = False
            except IOError as ex:
                _LOGGER.error('Failed to write configuration file, because %s', ex)
                raise

class Mqtt():

    def __init__(self, host, topic):
        self._client = PahoMqtt.Client()
        self._topic_prefix = topic
        self._client.on_connect = self.top_on_connect
        self._client.on_message = self.top_on_message
        self._client.connect(host, 1883, 60)
        self._on_connect = None
        self._on_message = None

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
        self._config = config
        self._working = False
        # Mqtt
        self._mqtt = Mqtt(config.get('mqtt_host'), config.get('topic_prefix'))
        self._mqtt.on_message = self.on_message
        self._mqtt.start(False)
        # Distance sensor
        self._sensor = sensor.Measurement(self._config.get('trigger_pin'),
                                          self._config.get('echo_pin'),
                                          temperature = self._config.get('sensor_temperature'),
                                          unit = self._config.get('unit_system'),
                                          round_to=2)
        _LOGGER.debug('Worker initialized')

    def on_message(self, client, userdata, msg):
        if msg.topic == 'home/status':
            self.send_config()
        t = msg.topic.rsplit('/', 2)
        verb = t[1]
        key = t[2]
        value = msg.payload.decode('ascii')
        if verb == 'set':
            self.set_config(key, value)
        if verb == 'cmd':
            self.run_command(key, value)

    def send_config(self):
        self._mqtt.publish('firmware', FIRMWARE)
        self._mqtt.publish('trigger_pin', self._config.get('trigger_pin'))
        self._mqtt.publish('echo_pin', self._config.get('echo_pin'))
        self._mqtt.publish('sensor_temperature', self._config.get('sensor_temperature'))
        self._mqtt.publish('unit_system', self._config.get('unit_system'))
        self._mqtt.publish('distance_threshold', self._config.get('distance_threshold'))
        self._mqtt.publish('publish_distance', str(self._config.get('publish_distance')).lower())
        self._mqtt.publish('sleep_time', self._config.get('sleep_time'))
        self._mqtt.publish('refresh_time', self._config.get('refresh_time'))

    def set_config(self, key, value):
        if key == 'trigger_pin':
            self._config.set(key, int(value))
        if key == 'echo_pin':
            self._config.set(key, int(value))
        if key == 'sensor_temperature':
            self._config.set(key, int(value))
        if key == 'unit_system':
            self._config.set(key, value)
        if key == 'distance_threshold':
            self._config.set(key, round(float(value)))
        if key == 'publish_distance':
            self._config.set(key, value == 'true')
        if key == 'sleep_time':
            self._config.set(key, int(value))
        if key == 'refresh_time':
            self._config.set(key, int(value))
        self._mqtt.publish(key, value)


    def run_command(self, key, value):
        if key == 'start':
            self.start()
        if key == 'pause':
            self.pause()
        if key == 'write':
            self._config.write()

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
                    if self._config.get('publish_distance'):
                        self._mqtt.publish('distance', distance)
                    if distance < self._config.get('distance_threshold'):
                        presence = 'ON'
                    else:
                        presence = 'OFF'
                    _LOGGER.debug('Presence %s', presence)
                    if presence != self._prev_presence or time.time() - self._prev_time > self._config.get('refresh_time'):
                        self._mqtt.publish('presence', presence)
                        self._prev_presence = presence
                        self._prev_time = time.time()
                time.sleep(self._config.get('sleep_time'))
            except (KeyboardInterrupt, SystemExit):
                self._mqtt.stop()
                _LOGGER.debug('Worker stopped')
                break
            except (UnboundLocalError, SystemError, RuntimeError):
                pass
            except Exception as ex:
                _LOGGER.error(str(ex))
                raise
                

    def read_distance(self):
        raw = self._sensor.raw_distance()
        if self._config.get('unit_system') == 'imperial':
            return self._sensor.distance_imperial(raw)
        if self._config.get('unit_system') == 'metric':
            return self._sensor.distance_metric(raw)

if __name__ == "__main__":
    # print(sys.argv[0])
    c = Config(CONFIG_FILE)
    w = Worker(c)
    w.start()
    c.write()


