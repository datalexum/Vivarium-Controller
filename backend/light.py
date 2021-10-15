import time
import paho.mqtt.client as mqtt


class Light:
    def __init__(self, host: str, port: int, topic: str):
        str(int(time.time()))
        self.client = mqtt.Client(client_id="python-"+str(int(time.time())))
        self.client.connect(host, port)
        self.topic = topic

    def setChannel(self, channel: int, intensity: int):
        self.client.publish("cmnd/"+self.topic+"/channel"+str(channel), str(intensity))

    def dimWhite(self, intensity: int):
        self.setChannel(1,0)
        self.setChannel(2, 0)
        self.setChannel(3, 0)
        self.setChannel(4, intensity)
        if intensity > 0:
            self.setChannel(5, intensity/3)
        else:
            self.setChannel(5, 0)

    def getStatus(self):
        pass
