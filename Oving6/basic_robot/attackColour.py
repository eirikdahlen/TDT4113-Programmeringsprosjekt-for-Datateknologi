from behavior import Behavior
from imager2 import Imager
import imager2 as IMR

class AttackColour(Behavior):

    def __init__(self, bbcon, priority):
        super().__init__(bbcon, priority)
        self.sensor = self.bbcon.sensob[0]
        self.match_degree = 0.02
        self.weight = self.priority * self.match_degree

    def consider_activation(self):
        if self.bbcon.wall_detected and not self.active_flag:
            self.active_flag = True
        else:
            self.active_flag = False

    def sense_and_act(self):
        im = self.sensor.get_value()
        im = IMR.Imager(image=im).scale(3, 3)
        im.dump_image("test.jpeg")
        #im.display()
        if im.blackboi():
            print("pic is dark!")
            self.motor_recommendation = ['B', 20]
            self.match_degree = 1
        else:
            print("pic is bright")
            self.motor_recommendation = ['S', 0]
            self.match_degree = 0.02

