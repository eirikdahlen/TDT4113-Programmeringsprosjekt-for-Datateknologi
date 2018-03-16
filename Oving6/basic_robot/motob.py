from motors import Motors

__author__ = "Frikk Hald Andersen"

class Motob :

    def __init__(self):
        self.value = None
        self.motors = Motors()

    def update(self, v):
        self.value = v
        self.operate()

    def operate(self):
        if self.value[0] == 'S':
            self.motors.stop()
        elif self.value[0] == 'F':
            self.motors.forward(0.5, 0.3)
        elif self.value[0] == 'B':
            self.motors.backward(0.3, 0.3)
        elif self.value[0] == 'R':
            self.motors.right(0.5, 0.3)
        elif self.value[0] == 'L':
            self.motors.left(0.5, 0.3)




