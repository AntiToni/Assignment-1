import pygame
import io
import os
from time import perf_counter
import numpy as np
import ctypes
from math import ceil
from turingmachine import TuringMachine

from sys import platform
if platform == "win32":
    errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)

##
#   CHANGEABLE PARAMETERS
##
GRID_SIZE = (320,180)       # Should be multiples of 16 and 9 for best results on 16:9 screens
NUM_MACHINES = 2            # Large numbers remove visible complexity
MIN_STATES = 50             # Large number of states causes more random movement, less order
MAX_STATES = 50
LOAD_FILE = 'chaotic'        # Leave empty to randomly generate
LOAD_FROM_FILE = True       # True if loading from file, False if randomly generating

BG_COLOUR = 'black'
TILE_COLOUR = 'white'
HEAD_COLOUR = 'red'
##
#   END CHANGEABLE PARAMETERS
##

START_POS = (GRID_SIZE[0]//2, GRID_SIZE[1]//2)  #   Generally looks best if start position is in centre
STATE_RANGE = (MIN_STATES, MAX_STATES)

pygame.init()
screenSize = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode((screenSize[0], screenSize[1]), pygame.FULLSCREEN | pygame.DOUBLEBUF, 16)  
clock = pygame.time.Clock()
running = True

tileSize = (screenSize[0]/float(GRID_SIZE[0]), screenSize[1]/float(GRID_SIZE[1]))   
tileGrid = np.full(GRID_SIZE, False, dtype=bool)

simSpeed = 16
stepsPerFrame = 1
showHeads = True

machineList = []

if not LOAD_FROM_FILE:
    for i in range(NUM_MACHINES):
        machineList.append(TuringMachine(tileGrid, GRID_SIZE, START_POS, STATE_RANGE))
else:
    if os.path.isfile(LOAD_FILE):
        with open(LOAD_FILE, 'r') as file:
            machineStrings = file.read().split('\nBREAK\n')
            for ms in machineStrings:
                tNum = int(len(ms.splitlines())/2)
                machineList.append(TuringMachine(tileGrid, GRID_SIZE, START_POS, (tNum,tNum), ms))
    else:
        print('Load File Invalid')
        exit()
    
headUpdates = [None for i in range(len(machineList))]

screen.fill(BG_COLOUR)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                saveString = ''
                for machine in machineList:
                    saveString += str(machine) + '\nBREAK\n'
                saveString = saveString[:-7]
                for i in range(1,101):
                    if not os.path.isfile('save_' + str(i)):
                        with open('save_' + str(i), 'w') as file:
                            file.write(saveString)
                        break
            if event.key == pygame.K_h:
                showHeads = not showHeads
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

    updateSet = set()
    # First add previous head positions to update set
    for pos in headUpdates:
        if pos is not None:
            updateSet.add(pos)

    overallTime = 0.0
    totalStepTime = 0.0
    totalSetTime = 0.0
    totalHeadTime = 0.0

    # Then step through machines
    for i in range(stepsPerFrame):
        for j in range(len(machineList)):
            stepStart = perf_counter()
            updates = machineList[j].step()
            totalStepTime += perf_counter() - stepStart

            setStart = perf_counter()
            if updates[0] is not None:
                updateSet.add(updates[0])
            totalSetTime += perf_counter() - setStart

            headStart = perf_counter()
            headUpdates[j] = updates[1]
            totalHeadTime += perf_counter() - headStart
            overallTime += perf_counter() - stepStart

    for pos in updateSet:
        tileVal = tileGrid[pos[0]][pos[1]]
        if not tileVal:
            tile = pygame.Rect(ceil(pos[0]*tileSize[0]), ceil(pos[1]*tileSize[1]), ceil(tileSize[0]), ceil(tileSize[1]))
            pygame.draw.rect(screen, BG_COLOUR, tile, 0)
        else:
            tile = pygame.Rect(ceil(pos[0]*tileSize[0]), ceil(pos[1]*tileSize[1]), ceil(tileSize[0]), ceil(tileSize[1]))
            pygame.draw.rect(screen, TILE_COLOUR, tile, 0)

    if showHeads:
        for pos in headUpdates:
            # Draw head in red
            tile = pygame.Rect(ceil(pos[0]*tileSize[0]), ceil(pos[1]*tileSize[1]), ceil(tileSize[0]), ceil(tileSize[1]))
            pygame.draw.rect(screen, HEAD_COLOUR, tile, 0)
    
    pygame.display.flip()

    frameRate = 1.0 / (clock.tick(simSpeed) / 1000)
    print('TPS: ' + str(int(frameRate*stepsPerFrame)) + ' FPS: ' + str(int(frameRate)) + ' (TFPS: ' + str(simSpeed) + ' TPF: ' + str(stepsPerFrame) + ')')

pygame.quit()