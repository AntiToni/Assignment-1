import pygame
import ctypes
from turingmachine import TuringMachine
errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)

GRID_SIZE = (160,90)
NUM_MACHINES = 2

pygame.init()
screenSize = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode((screenSize[0], screenSize[1]), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

tileSize = screenSize[0]/GRID_SIZE[0]
enabledTiles = {}

for x in range(GRID_SIZE[0]):
    for y in range(GRID_SIZE[1]):
        enabledTiles[x,y] = 0

simSpeed = 16
stepsPerFrame = 1
showHeads = True

machineList = []

for i in range(NUM_MACHINES):
    machineList.append(TuringMachine(enabledTiles))

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

    screen.fill('pink')

    for (x, y) in enabledTiles:
        tileVal = enabledTiles[(x, y)]
        if tileVal == 1:
            tile = pygame.Rect(x*tileSize, y*tileSize, tileSize, tileSize)
            pygame.draw.rect(screen, 'blue', tile, 0)
        elif showHeads and tileVal != 0:
            # Draw head in red
            tile = pygame.Rect(x*tileSize, y*tileSize, tileSize, tileSize)
            pygame.draw.rect(screen, 'green', tile, 0)
    
    pygame.display.flip()

    frameRate = 1.0 / (clock.tick(simSpeed) / 1000)
    print('TPS: ' + str(int(frameRate*stepsPerFrame)) + ' FPS: ' + str(int(frameRate)) + ' (TFPS: ' + str(simSpeed) + ' TPF: ' + str(stepsPerFrame) + ')')

pygame.quit()