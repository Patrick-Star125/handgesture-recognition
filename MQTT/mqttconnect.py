from MQTT.MQTTClient import MQTTConnect as mqtt


class mqttConnect:

    def __init__(self):
        self.mqtt = mqtt()
        self.mqtt.MQTTClient()

    def mqttKeep(self):
        self.mqtt.Client.loop_start()

    def SendServer(self,msg):
        self.mqtt.Publish(msg)

    def RevServer(self):
        if self.mqtt.Rev:
            return self.mqtt.Rev
        else:
            return None



