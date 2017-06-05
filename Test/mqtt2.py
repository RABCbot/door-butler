from threading import Thread
import paho.mqtt.client as mqtt

class MqttBot(Thread):

    def __init__(self, host):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(host, 1883, 60)

        Thread.__init__( self )

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.client.subscribe("#")

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

    def run(self):
        self.client.loop_forever()
 
if __name__ == '__main__':
    bot = MqttBot("192.168.101.113")
    bot.setDaemon(True)
    bot.start()
    while True: pass

