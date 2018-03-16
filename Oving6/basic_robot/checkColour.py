from behavior import Behavior
from imager2 import Imager
import imager2 as IMR

class CheckColour(Behavior):

    def __init__(self, bbcon, priority):
        super().__init__(bbcon, priority)
        self.sensor = self.bbcon.sensob[0]
        self.match_degree = 0.02
        self.weight = self.priority * self.match_degree

    def consider_activation(self):
        if self.bbcon.wall_detected and not self.bbcon.wall_checked:
            print("cam is active")
            self.active_flag = True
        else:
            print(self.bbcon.wall_detected)
            print(self.bbcon.wall_detected)
            print("cam is not active")
            self.active_flag = False

    def sense_and_act(self):
        im = self.sensor.get_value()
        im = IMR.Imager(image=im).scale(3, 3)
        im.dump_image("test.jpeg")
        #im.display()
        if im.blackboi():
            print("pic is dark!")
            self.motor_recommendation = ['B', 50]
            self.match_degree = 1
        else:
            print("pic is bright")
            self.motor_recommendation = ['S', 0]
            self.match_degree = 0.02
        print("pic taken")
        self.bbcon.wall_checked = True

