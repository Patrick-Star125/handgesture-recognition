import json

import paho.mqtt.client as mqtt
import time

class MQTTConnect():


    def __init__(self):
        with open('setting.json') as f:
            setting = f.readline()
            setting = json.loads(setting)
            self.IP = setting["IP"]
            self.Port = int(setting["PORT"])
            self.user = setting["USERNAME"]
            self.passward = setting["PASSWORD"]
            self.id = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
            self.Client = None
            self.stopic = setting["TOPIC"]
            self.ptopic = setting["TOPIC"]
            self.heat = 60
            self.qos = setting["QOS"]
            self.Rev = None


    def MQTTClient(self):
        self.Client = mqtt.Client(self.id)
        self.Client.on_connect = self.on_connect
        self.Client.on_message = self.on_message
        self.Client.connect(host=self.IP,port=self.Port,keepalive=self.heat)


    def Remessage(self,msg):
        try:
            self.Rev = msg
            return self.Rev
        except:
            print('erro format')

        pass

    def Publish(self,msg):
        self.Client.publish(topic=self.ptopic,payload=msg,qos=self.qos)

    def on_connect(self,client, userdata, flags, rc):
        if rc == 0:
            print("Connected with result code " + str(rc))
            print("MQTT connected!")
            client.subscribe(topic=self.stopic)
        else:
            print('Connect Error status {0}'.format(rc))


    def on_message(self,client, userdata, msg):
        self.Remessage(msg.payload.decode("utf-8"))
        #print(msg.topic + " " + msg.payload.decode("utf-8"))

