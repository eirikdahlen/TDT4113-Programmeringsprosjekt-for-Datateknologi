import behavior

class Followline(behavior.Behavior):

    def __init__(self, bbcon, priority):
        super().__init__(bbcon, priority)
        self.sensor = self.bbcon.sensob[2]
        self.match_degree = 0.8
        self.weight = self.priority * self.match_degree

    def consider_activation(self):
        if self.bbcon.wall_detected:
            return
        values = self.sensor.get_value()
        for i in range(6):
            if values[i]<0.2:
                self.active_flag = True



    def sense_and_act(self):
        values = self.sensor.get_value()
        self.match_degree = 0.8
        if self.bbcon.wall_detected:
            self.motor_recommendation = ['S', 0]
            self.active_flag=False
            print("followline deactivated because of wall")

        elif values[2] < 0.2 and values[3] < 0.2:
            self.motor_recommendation = ['F', 0]

        elif values[0] < 0.2:
            self.motor_recommendation = ['L', 20]
        elif values[1] < 0.2:
            self.motor_recommendation = ['L', 10]

        elif values[5] < 0.2:
            self.motor_recommendation = ['R', 20]
        elif values[4] < 0.2:
            self.motor_recommendation = ['R', 10]
        else:
            self.motor_recommendation = ['S', 0]
            self.active_flag=False
            print("followline deactivated because of missing line")

            # for å teste kamera
            self.bbcon.wall_detected = True



