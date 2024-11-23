from MotorModule import Motor
import KBModule as kb

##################################
###Define Motor Config###
# Pin Order for motor class connected to L298N board: EnA In1 In2 (left), EnB, In3, In4(right)
motor = Motor(2,3,4, 22,17,27)
##################################

kb.init() #init pygame to read key presses
 
def main():
    if kb.getKey('w'):
        motor.move(0.40, 0, 0.1)
        print("forward")
    if kb.getKey('s'):
        motor.move(-0.40, 0, 0.1)
        print("reverse")
    if kb.getKey('a'):
        motor.move(0.30, -0.5, 0.1)
        print("turn left")
    if kb.getKey('d'):
        motor.move(0.30, 0.5, 0.1)
        print("turn right")
    else:
        motor.stop()

if __name__ == '__main__':
    while True:
        main()