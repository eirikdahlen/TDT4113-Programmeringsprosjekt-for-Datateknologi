import time

from reflectance_sensors import ReflectanceSensors
from irproximity_sensor import IRProximitySensor
from ultrasonic import Ultrasonic
from camera import Camera

from zumo_button import ZumoButton
from sensob import Sensob
from motob import Motob
from arbitrator import Arbitrator

# her skal alle behaviors importeres.
import followline
import avoid_front_collision
import checkColour

class Bbcon:

    def __init__(self):
        self.arbitrator = Arbitrator(self)
        #Oppretter fire sensob objekter. Kamera, ir, reflectance og ultra.
        cam = Sensob()
        cam.add_sensor(Camera())
        ir = Sensob()
        ir.add_sensor(IRProximitySensor())
        reflect = Sensob()
        reflect.add_sensor(ReflectanceSensors())
        ultra = Sensob()
        ultra.add_sensor(Ultrasonic())
        self.sensob = [cam,ir,reflect,ultra]
        self.motobs = [Motob()]
        self.behaviors = []
        self.wall_detected = False
        self.wall_checked = False


    def activate_behavior(self, behavior):
            behavior.active_flag=True

    def dactivate_behavior(self, behavior):
            behavior.active_flag=False


    def add_behavior(self, behavior):
        self.behaviors.append(behavior)


    def add_sensob(self, sensob):
        self.sensob.append(sensob)

    def run(self):
        ZumoButton().wait_for_press()
        while True:
            print("number of behaviors:", len(self.behaviors))
            for behavior in self.behaviors:
                if not behavior.active_flag:
                    behavior.consider_activation()
                if behavior.active_flag:
                    print(behavior)
                    behavior.sensor.update()
                    behavior.sense_and_act()
                   # print(behavior.motor_recommendation)
            recommendations = self.arbitrator.choose_action()
            print("rec ", recommendations)
            if recommendations[1]== True:
                print("Prosess avsluttet.")
                break
            for motob in self.motobs:
                motob.update(recommendations[0])
            time.sleep(0.2)
            for sensob in self.sensob:
                sensob.reset()
