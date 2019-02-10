import logging
import json
import time
import requests
import paho.mqtt.client as mqtt
from hcsr04sensor import sensor

CONFIG_FILE = 'config.json'
LOGGER_FILE = 'butler-sensor.log'

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=LOGGER_FILE,
                    filemode='w')
_LOGGER = logging.getLogger(__name__)


class MqttDistance():

    def __init__(self):
        self._prev_presence = "OFF"
        self._prev_time = time.time()
        # config parameters
        self._mqtt_host = 'iot.eclipse.org'
        self._trigger_pin = 17
        self._echo_pin = 27
        self._trigger_temp = 68
        self._trigger_distance = 20
        self._unit_system = 'imperial'
        self._time_interval = 60
        self._publish_distance = False
        self._topic_prefix = 'home/butler/sensor/'
        self.read_config()
        # Distance sensor
        self._sensor = sensor.Measurement(self._trigger_pin,
                                          self._echo_pin,
                                          temperature = self._trigger_temp,
                                          unit = self._unit_system,
                                          round_to=2)
        # Mqtt
        self._client = mqtt.Client()
        self._client.on_connect = self.on_connect
        self._client.on_message = self.on_message
        self._client.connect(self._mqtt_host, 1883, 60)
        # self._client.loop_start()

        _LOGGER.debug('MqttDistance initialized')

    def loop(self):
        self._client.loop_start()
        distance = 0
        presence = 'OFF'
        _LOGGER.debug('Loop started')
        while True:
            try:
                distance = self.read_distance()
                _LOGGER.debug('Distance %s', distance)
                if self._publish_distance:
                    self._client.publish(self._topic_prefix + 'distance', distance)
                if distance < self._trigger_distance:
                    presence = 'ON'
                else:
                    presence = 'OFF'
            except:
                pass

            if presence != self._prev_presence or time.time() - self._prev_time > self._time_interval:
                _LOGGER.debug('Publish presence %s', presence)
                self._client.publish(self._topic_prefix + 'presence', presence)
                self._prev_presence = presence
                self._prev_time = time.time() 

    def stop(self):
        self._client.loop_stop()
        _LOGGER.debug('Loop stopped')
        sys.exit()

    def read_distance(self):
        raw = self._sensor.raw_distance()
        if self._unit_system == 'imperial':
            return self._sensor.distance_imperial(raw)
        if self._unit_system == 'metric':
            return self._sensor.distance_metric(raw)

    def read_config(self):
        try:        
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                _LOGGER.debug(config)
                self._mqtt_host = config['mqtt-host']
                self._trigger_pin = config['trigger-pin']
                self._echo_pin = config['echo-pin']
                self._trigger_temp = config['trigger-temperature']
                self._trigger_distance =  config['trigger-distance']
                self._unit_system =  config['unit-system']
                self._time_interval = config['time-interval']
                self._publish_distance = config['publish-distance']
                self._topic_prefix = config['topic-prefix']
        except IOError as ex:
            _LOGGER.error('Failed to read configuration file, because %s', ex)
            sys.exit()

    def get_config(self):
        return {'mqtt-host': self._mqtt_host,
                'trigger-pin': self._trigger_pin,
                'echo-pin': self._echo_pin,
                'trigger-temperature': self._trigger_temp,
                'trigger-distance': self._trigger_distance,
                'unit-system': self._unit_system,
                'time-interval': self._time_interval,
                'publish-distance': self._publish_distance,
                'topic-prefix': self._topic_prefix}

    def write_config(self):
        try:
            config = self.get_config()
            with open('config.json', 'w') as f:
                json.dump(config, f)
        except IOError as ex:
            _LOGGER.error('Failed to write configuration file, because %s', ex)

    def on_connect(self, client, userdata, flags, rc):
        _LOGGER.debug('Mqtt connected')
        self._client.subscribe(self._topic_prefix + 'config/#')

    def on_message(self, client, userdata, msg):
        key = msg.topic.rsplit('/', 1)[1]
        value = msg.payload.decode('ascii')
        _LOGGER.debug('Message received: %s, payload: %s', key, value)
        if key == 'mqtt-host':
            self._mqtt_host = value
        if key == 'trigger-pin':
            self._trigger_pin = int(value)
        if key == 'echo-pin':
            self._echo_pin = int(value)
        if key == 'trigger-temperature':
            self._trigger_temp = int(value)
        if key == 'trigger-distance':
            self._trigger_distance =  int(value)
        if key == 'unit-system':
            self._unit_system =  value
        if key == 'time-interval':
            self._time_interval = int(value)
        if key == 'publish-distance':
            self._publish_distance = (value == 'true')
        if key == 'topic-prefix':
            self._topic_prefix = value
        if key == 'get':
            config = json.dumps(self.get_config())
            _LOGGER.debug(config)
            self._client.publish(self._topic_prefix + 'config', config)
        if key == 'write':
            self.write_config()

if __name__ == "__main__":

    bot = MqttDistance()
    try:
        bot.loop()
    except:
        bot.stop()
