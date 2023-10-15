from random import randint, random
from time import perf_counter
from math import pow
import numpy as np

MIN_STATES = 5
MAX_STATES = 5
DIR_LIST = ['U','D','L','R']

class TuringMachine:
    totalReadTime = 0.0
    totalUpdateTime = 0.0
    overallTime = 0.0

    def __init__(self, tape : np.ndarray, gridSize, startPos, stateRange = (MIN_STATES, MAX_STATES), program : str = None):
        self.tape = tape
        self.trf = {}
        self.head = list(startPos)
        self.gridSize = gridSize
        self.state = 0

        if program is not None:
            for line in program.splitlines():
                s1, r, s2, w, dir = line.split(',')
                self.trf[int(s1),r.lower() == 'true'] = (int(s2), w.lower() == 'true', dir)
        else:
            numStates = randint(stateRange[0], stateRange[1])
            for s1 in range(numStates):
                for r in range(0,2):
                    self.trf[s1,bool(r)] = (randint(0,numStates-1), bool(randint(0,1)), DIR_LIST[randint(0,3)])

    def step(self):
        updatePos1 = None
        updatePos2 = None
        changed = False

        state, tape = self.state, self.tape
        head_x, head_y = self.head
        r = tape[head_x][head_y] # False = disabled, True = enabled
        action = self.trf.get((state, r))
        if action:
            s2, w, dir = action
            changed = r != w
            tape[head_x, head_y] = w
            self.moveHead(dir)

            updatePos2 = tuple(self.head)
            self.state = s2
            updatePos1 = (head_x, head_y) if changed else None
        
        return updatePos1, updatePos2

    def moveHead(self, dir : str):
        if dir == 'L':
            self.head[0] -= 1
            if self.head[0] < 0:
                self.head[0] += self.gridSize[0]
        elif dir == 'R':
            self.head[0] += 1
            if self.head[0] >= self.gridSize[0]:
                self.head[0] -= self.gridSize[0]
        elif dir == 'U':
            self.head[1] -= 1
            if self.head[1] < 0:
                self.head[1] += self.gridSize[1]
        elif dir == 'D':
            self.head[1] += 1
            if self.head[1] >= self.gridSize[1]:
                self.head[1] -= self.gridSize[1]
        else:
            raise 'You done entered a wrong direction.'
        
    def __str__(self):
        output = ''
        for (s1,r),(s2,w,dir) in self.trf.items():
            output += str(s1) + ',' + str(r) + ',' + str(s2) + ',' + str(w) + ',' + str(dir) + '\n'

        return output[:-1]