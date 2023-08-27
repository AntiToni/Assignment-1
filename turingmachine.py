from random import randint, random
from math import pow

MIN_STATES = 5
MAX_STATES = 5
DIR_LIST = ['U','D','L','R']

class TuringMachine:
    def __init__(self, tape : dict, startPos = (80,45), program : str = None, gridSize = (160,90)):
        self.tape = tape
        self.trf = {}
        self.head = list(startPos)
        self.gridSize = gridSize
        self.state = 0

        if program is not None:
            for line in program.splitlines():
                s1, r, s2, w, dir = line.split(',')
                self.trf[int(s1),int(r)] = (int(s2), int(w), dir)
        else:
            numStates = randint(MAX_STATES,MAX_STATES)
            for s1 in range(numStates):
                for r in range(0,2):
                    self.trf[s1,r] = (randint(0,numStates-1), randint(0,1), DIR_LIST[randint(0,3)])

    def step(self):
        r = self.tape[tuple(self.head)] # 0 = disabled, 1 = enabled, 2 = head disabled, 3 = head enabled
        if r > 1:
            r -= 2
        action = self.trf.get((self.state, r))
        if action:
            s2, w, dir = action
            if w == 1:
                self.tape[tuple(self.head)] = 1
            else:
                self.tape[tuple(self.head)] = 0
            self.moveHead(dir)

            # Head of tape should be different colour
            headVal = self.tape[tuple(self.head)]
            if headVal in [0,2]:
                self.tape[tuple(self.head)] = 2
            elif headVal in [1,3]:
                self.tape[tuple(self.head)] = 3

            self.state = s2

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