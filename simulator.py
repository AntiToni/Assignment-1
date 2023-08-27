import pygame
import ctypes
from math import ceil
from turingmachine import TuringMachine
errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)

##
#   CONTROLS
#   H - HIDE TM HEADS
#   ESC - END SIMULATION
#   -/= - DECREASE/INCREASE SIMULATION SPEED
##

##
#   CHANGEABLE PARAMETERS
##
GRID_SIZE = (320,180)       # Should be multiples of 16 and 9 for best results on 16:9 screens
NUM_MACHINES = 10           # Large numbers remove visible complexity
MIN_STATES = 10             # Large number of states causes more random movement, less order
MAX_STATES = 10
##
#   END CHANGEABLE PARAMETERS
##

START_POS = (GRID_SIZE[0]//2, GRID_SIZE[1]//2)  #   Generally looks best if start position is in centre
STATE_RANGE = (MIN_STATES, MAX_STATES)

pygame.init()
screenSize = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode((screenSize[0], screenSize[1]), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

tileSize = (screenSize[0]/float(GRID_SIZE[0]), screenSize[1]/float(GRID_SIZE[1]))
enabledTiles = {}

for x in range(GRID_SIZE[0]):
    for y in range(GRID_SIZE[1]):
        enabledTiles[x,y] = 0

simSpeed = 16
stepsPerFrame = 1
showHeads = True

machineList = []

for i in range(NUM_MACHINES):
    machineList.append(TuringMachine(enabledTiles, GRID_SIZE, START_POS, STATE_RANGE))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                if showHeads: 
                    showHeads = False 
                else:
                    showHeads = True
            if event.key == pygame.K_EQUALS:
                if simSpeed < 60:
                    simSpeed *= 2
                else:
                    stepsPerFrame *= 2
            if event.key == pygame.K_MINUS:
                if stepsPerFrame > 1:
                    stepsPerFrame //= 2
                    if stepsPerFrame == 0:
                        stepsPerFrame = 1
                else:
                    simSpeed //= 2
                    if simSpeed == 0:
                        simSpeed = 1
            if event.key == pygame.K_ESCAPE:
                running = False

    for i in range(stepsPerFrame):
        for machine in machineList:
            machine.step()

    screen.fill('black')

    for (x, y) in enabledTiles:
        tileVal = enabledTiles[(x, y)]
        if tileVal == 1:
            tile = pygame.Rect(ceil(x*tileSize[0]), ceil(y*tileSize[1]), ceil(tileSize[0]), ceil(tileSize[1]))
            pygame.draw.rect(screen, 'white', tile, 0)
        elif showHeads and tileVal != 0:
            # Draw head in red
            tile = pygame.Rect(ceil(x*tileSize[0]), ceil(y*tileSize[1]), ceil(tileSize[0]), ceil(tileSize[1]))
            pygame.draw.rect(screen, 'red', tile, 0)
    
    pygame.display.flip()

    frameRate = 1.0 / (clock.tick(simSpeed) / 1000)
    print('TPS: ' + str(int(frameRate*stepsPerFrame)) + ' FPS: ' + str(int(frameRate)) + ' (TFPS: ' + str(simSpeed) + ' TPF: ' + str(stepsPerFrame) + ')')

pygame.quit()