import io

TURMITE = [[[1,2,1],[1,8,1]],[[1,2,1],[0,2,0]]]
# TURMITE = [[[1,8,1],[1,2,0]],[[1,4,1],[1,4,2]],[[0,1,0],[0,4,0]]]
SAVE_FILE = 'chaotic'

saveString = ''
for rot in range(4):
    for s in range(len(TURMITE)):
        for c in range(len(TURMITE[s])):
            # New state must be specified state and cur rotation plus turn amount specified.
            # No turn
            if TURMITE[s][c][1] == 1:
                turnAmount = 0
            # Turn right
            elif TURMITE[s][c][1] == 2:
                turnAmount = 1
            # U turn
            elif TURMITE[s][c][1] == 4:
                turnAmount = 2
            # Turn left
            elif TURMITE[s][c][1] == 8:
                turnAmount = 3
            
            newRot = rot + turnAmount
            # Deal with overrotating
            if newRot > 3:
                newRot -= 4

            # Get direction should move depending on new rotation
            dirList = ['L','U','R','D']
            direction = dirList[newRot]

            saveString += (str(s*4+rot) + ',' + ('True' if c else 'False') + ',' + str(TURMITE[s][c][2]*4+newRot) + ',' + ('True' if TURMITE[s][c][0] else 'False') + ',' + direction + '\n')
            
with open(SAVE_FILE, 'w') as file:
    file.write(saveString[:-1])