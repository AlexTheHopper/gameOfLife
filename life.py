import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

##Game of life

gridSize = 100
#Fills grid with random
randomGrid = False
#Treats the window edges as connecting:
loopWindow = True

if randomGrid:
    grid = np.random.randint(0,2, size=(gridSize, gridSize))
else:
    grid = np.zeros((gridSize,gridSize))



#Creates glider at given location, coordinates are top left of glider 3x3
def createGlider(x,y,grid):
        grid[x:x+3,y:y+3] = [[1, 0, 0],
                             [0, 1, 1],
                             [1, 1, 0]]
        
#Creates light weight spaceship at given location, coordinates are top left of ship 5x4
def createLightWeightShip(x,y,grid):
        grid[x:x+4,y:y+5] = [[0, 1, 0, 0, 1],
                             [1, 0, 0, 0, 0],
                             [1, 0, 0, 0, 1],
                             [1, 1, 1, 1, 0]]

        
createGlider(10,10,grid)
createLightWeightShip(50,10,grid)

#Checks each individial coordinate
def checkChange(miniGrid, value):

    #Check for dead cells - needs 3 alive neighbours to be born
    if value == 0:
        if np.sum(miniGrid) == 3:
            return 1 
        else: 
            return 0
        
    #Check for alive cells - needs 2 or 3 alive neighbours to stay alive.
    else:
        if np.sum(miniGrid) == 3 or np.sum(miniGrid) == 4:
            return 1
        else:
            return 0
            
#Checks entire grid, accounting for cases on array edge
def updateGrid(gridOld):
    global gridSize
    #We need a new grid as to not account for changes already made each timestep
    gridNew = np.zeros((gridSize,gridSize))

    for i in range(gridSize):
        for j in range(gridSize):

            if loopWindow:
                L = len(gridOld)
                returnGrid = [[gridOld[(i-1+L)%L,(j-1+L)%L], gridOld[(i-1+L)%L,(j+L)%L], gridOld[(i-1+L)%L,(j+1+L)%L]],
                              [gridOld[(i+L)%L,(j-1+L)%L], gridOld[(i+L)%L,(j+L)%L], gridOld[(i+L)%L,(j+1+L)%L]],
                              [gridOld[(i+1+L)%L,(j-1+L)%L], gridOld[(i+1+L)%L,(j+L)%L], gridOld[(i+1+L)%L,(j+1+L)%L]]]
                gridNew[i,j] = checkChange(returnGrid, gridOld[i,j])

            else:
                #Check to see if i,j is on an edge
                iLow = 1
                iHigh = 2
                jLow = 1
                jHigh = 2
                
                if i == 0:
                    iLow = 0
                elif i == gridSize - 1:
                    iHigh = 1

                if j == 0:
                    jLow = 0
                elif j == gridSize - 1:
                    jHigh = 1

                #Check neighbours based on location
                gridNew[i,j] = checkChange(gridOld[i-iLow:i+iHigh,j-jLow:j+jHigh], gridOld[i,j])

            
    return gridNew

#Animate function:
time = 0
def animate(i):
    global grid
    global time

    grid = updateGrid(grid)

    plt.cla()
    plt.xticks([]) 
    plt.yticks([]) 
    plt.title('Your Game of Life after '+str(time)+' generations.')
    plt.imshow(grid, cmap='binary')
    time += 1
    


ani = FuncAnimation(plt.gcf(), animate, interval = 1, frames = 30)
plt.show()

        