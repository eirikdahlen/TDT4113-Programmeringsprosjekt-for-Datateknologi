
from bbcon import *

# Initialiserer Bbcon-objektet
# Bbcon-objektet initialiserer alle sensorene og motorer
controller = bbcon()

# Initialiserer behaviors
follow_line = followline.Followline(controller, 1)
avoid = avoid_front_collision.AvoidFrontCollision(controller, 2)
check = checkColour.CheckColour(controller, 2)

# Legger til behaviors
controller.add_behavior(follow_line)
#controller.add_behavior(avoid)
controller.add_behavior(check)


controller.activate_behavior(follow_line)  # followline skal være aktiv fra starten av
print("Followline-behavior activated")
#controller.activate_behavior(avoid)  # avoid skal alltid være aktiv
#print("Avoid-behavior activated")





controller.run()
