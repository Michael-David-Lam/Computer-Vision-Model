import pygame

def init():
    pygame.init()
    window = pygame.display.set_mode((100, 100))

"""Return true if the passed string is the key being pressed, according to pygame formatting"""
def getKey(keyName):
    answer = False
    for event in pygame.event.get():
        pass
    key = pygame.key.get_pressed()
    pgKey = getattr(pygame, 'K_{}'.format(keyName)) #get key name from pygame format
    
    if key[pgKey]: #True when the passed keyName is the key currently pressed
        answer = True 

    pygame.display.update()
    return answer

#############################
# For testing
def main():
    if getKey('A'):
        print('A')
    if getKey('S'):
        print('S')   
    if getKey('W'):
        print('W')
    if getKey('D'):
        print('D')   
    else:
        print('idle...') 

if __name__ == '__main__':
    init()
    while True:
        main()