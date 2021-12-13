from Connect.connect import connect
from  MQTT.mqttconnect import mqttConnect as mqtt
import sys

class client:

    def __init__(self):
        self.connect = connect()

    def ReLog(self,log,img):
        self.connect.set_Log(log,img)


    def Revmsg(self):
        return self.mqtt.RevServer()

    def Sendmsg(self,msg):
        self.mqtt.SendServer(msg)

    def MQTTClient(self):
        self.mqtt = mqtt()

    def MQTTKeep(self):
        self.mqtt.mqttKeep()

    def GetVideo(self):
        cap = self.connect.get_cap()
        return cap

    def Operation(self):
        pass