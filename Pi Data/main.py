#from MotorModule import Motor
import KBModule as kb

##################################
"""Define Motor Config"""

##################################

kb.init()
 
def main():
    if kb.getKey('2'):
        print('Forward')
        #motor.forward(_,_,_,_)
    if kb.getKey('S'):
        pass

    else:
        pass#motor.stop()

if __name__ == '__main__':
    while True:
        main()