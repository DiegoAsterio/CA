from enum import Enum
import numpy as np
import pdb
import cv2 as cv

class Neigh(Enum):
    MOORE = 1
    VONNEUMAN = 2

class GOL:

    def __init__(self, moore):
        if moore:
            self.neighbourhood = Neigh.MOORE
        else:
            self.neighbourhood = Neigh.VONNEUMAN
        self.petriDish = None

    def countMHood(x,y,mat):
        counter = 0
        lenX, lenY = mat.shape
        for i in range(-1,2):
            for j in range(-1,2):
                if i != 0 or j != 0:
                    if x+i >= 0 and x+i < lenX and y+j >= 0 and y+j<lenY:
                        counter += mat[x+i,y+j]
        return counter

    # def exploreVNHood(self,x,y):

    def initializePetriDishRandomly(self,sizeX,sizeY):
        petriDish = np.random.randint(0,2,sizeY*sizeX)
        self.petriDish.resize((sizeY,sizeX))


    def initializePlayground(self):
        Rpentomino = np.array([[0,1,1],
                               [1,1,0],
                               [0,1,0]])
        self.petriDish = np.zeros((50,50))
        self.petriDish[23:26,23:26] = Rpentomino

    def initializePlayground3(self):
        diehard = np.array([[0,0,0,0,0,0,0,1,0],
                            [0,1,1,0,0,0,0,0,0],
                            [0,0,1,0,0,0,1,1,1]])
        self.petriDish = np.zeros((50,50))
        self.petriDish[23:26,23:32] = diehard

        
    def initializePlayground2(self):
        glider= np.array([[0,1,0],
                          [0,0,1],
                          [1,1,1]])
        self.petriDish = np.zeros((25,25))
        self.petriDish[1:4,1:4] = glider

        
    def generateSnapshots(self,generations):
        ret = [self.petriDish]
        population = self.petriDish
        for _ in range(generations):
            population = self.developCA(population)
            ret.append(population)
        return ret

    def developCA(self,population):
        lenY, lenX = population.shape
        ret = np.zeros((lenY,lenX))
        for i in range(lenY):
            for j in range(lenX):
                hood = GOL.countMHood(i,j,population)
                if population[i,j] == 1:
                    # pdb.set_trace()
                    if hood == 2 or hood == 3:
                        ret[i,j] = 1
                    else:
                        ret[i,j] = 0
                elif hood == 3:
                    ret[i,j] = 1
                else:
                    ret[i,j] = 0
        return ret
    
myGol = GOL(True)
myGol.initializePlayground3()
snapshots = myGol.generateSnapshots(130)
snapshots = list(map(lambda x:cv.resize(x*255,(512,512),interpolation=cv.INTER_AREA), snapshots))
for i in range(len(snapshots)):
    cv.imwrite("./imgs/CA" + str(i) + ".png",snapshots[i])


