import behavior

class AvoidFrontCollision(behavior.Behavior):
    def __init__(self, bbcon, priority):
        super().__init__(bbcon, priority)
        self.sensor = self.bbcon.sensob[3]  # ultrasonic-sensoren
        self.match_degree = 0.02
        self.weight = self.priority * self.match_degree

    def consider_activation(self):
        return

    def sense_and_act(self):
        distance = self.sensor.get_value()
        print("distance: ", distance)
        if distance < 6:
            self.motor_recommendation = ['S', 0]
            self.match_degree = 1
            self.bbcon.wall_detected = True
            print("Wall detected")
        else:
            self.motor_recommendation = ['F', 0]
            self.match_degree = 0.02
            self.bbcon.wall_detected = False
