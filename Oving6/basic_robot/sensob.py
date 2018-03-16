

class Sensob():

    def __init__(self):
        self.sensor = None
        self.value = None

    def update(self):
        self.sensor.update()
        self.value = self.sensor.get_value()

    def reset(self):
        self.sensor.reset()

    def add_sensor(self, sensor):
        self.sensor = sensor

    def get_sensor(self):
        return self.sensor

    def get_value(self):
        return self.value
