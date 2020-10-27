import copy
import random

class RandomGrid:
    
    def __init__(self,n=None,includeBlank=None, grid=None, lookup=None):
        #This is weird, we have this parameter which is default by all intents and purposes however its not
        #actually
        if not grid:
            if includeBlank:
                colors = [0]
            else:
                colors = []
                
            for i in range(n-1):
                for j in range(6):
                    colors.append(j+1)
            #print(colors)
            
            #self.grid = [random.sample(colors,n) for i in range(n)]
            random.shuffle(colors)
            self.grid=[[colors.pop() for i in range(n)] for j in range(n)]
            self.size = n
        
        else:
            self.grid = grid
            self.size = len(grid)
            
        if not lookup:
            self.create_lookup()
        
        else:
            self.lookup = lookup
            
    
    def create_lookup(self):
        
        self.lookup = {
        0 : None,
        1 : [],
        2 : [],
        3 : [],
        4 : [],
        5 : [],
        6 : []
            }
        
        for i in range(self.size):
            for j in range(self.size):
                color = self.grid[i][j]
                if color != 0:
                    self.lookup[color].append((i,j))
                else:
                    self.lookup[0] = (i,j)
        
        #sort each of the lists
        #for color in [1,2,3,4,5,6]:
        #    self.lookup[color].sort()
    
    def get_updated_lookup(self,x1,y1,x2,y2):
        """
        Return an updated lookup to reflect that we have swapped (x1,y1), (x2,y2).
        It is assumed that (x1,y1) is the location of the blank
        """
        
        color = self.grid[x2][y2]
        
        newLookup = copy.deepcopy(self.lookup)
        newLookup[0] = (x2,y2)
        newLookup[color].remove((x2,y2))
        newLookup[color].append((x1,y2))
        #newLookup[color].sort()
        return newLookup
                
            
    def __str__(self):
        rowStrings = []
        
        for i in range(len(self.grid)):
            stringRep = [str(i) for i in self.grid[i]]
            row = ' '.join(stringRep)
            rowStrings.append(row)
        
        return '\n'.join(rowStrings) + '\n'
    
    def to_int(self):
        """
        Converts the nested list structure of the grid into an integer for hashing purposes
        The integer is constructed, reading digit by digit, left to right, top to bottom
        """
        
        intRep = 0
        for i in range(self.size):
            for j in range(self.size):
                intRep += self.grid[i][j] * (10 ** (self.size**2 - (j + i*5 + 1)))
                
        return intRep
    
class RubiksGrid(RandomGrid):
    
    def __init__(self, grid=None, lookup=None):
        super().__init__(n=5,includeBlank=True, grid=grid, lookup=None)
        self.score = None
    
    
    def make_move(self,x1,y1,x2,y2, previousMove=None):
        """
        Return the grid that results from moving the "blank" square from coords (x1,y1) to (x2,y2)
        """
        
        
        #Check if we are moving the blank square
        if self.grid[x1][y1] != 0:
            print(f'Position ({x1},{y1}) is not blank, instead has color code {self.grid[x1][y1]}.')
            return None
        
        else:
            gridDistance = abs(x1-x2) + abs(y1-y2)
            
            #Check if we are not moving the blank at all
            if gridDistance == 0:
                print("Start and end coordinates are the same")
                return None
            
            #Check if we are "jumping" the blank. We should only move it one unit up, right, left, or down
            elif gridDistance > 1:
                print(f"Invalid move: coordinates ({x1},{y1}) and ({x2},{y2}) are too far apart")
                return None
            
            
            else:
                
                #Check if the current move is the inverse of the previous move
                if  previousMove:
                    prevx1 = previousMove[0]
                    prevy1 = previousMove[1]
                    prevx2 = previousMove[2]
                    prevy2 = previousMove[3]
                
                    if x1 == prevx2 and y1 == prevy2 and x2 == prevx1 and y2 == prevy2:
                        print(f"The current move ({x1},{y1},{x2},{y2}) will invert the previous move ({prevx1},{prevy1},{prevx2},{prevy2})")
                        return None
                
                #Check if we are going to cause an OOB error
                
                if (x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0):
                    print(f"One or more of the coordinates ({x1},{y1}) or ({x2},{y2}) specifies a negative index")
                    return None
                
                elif (x1 > self.size-1 or y1 > self.size-1 or x2 > self.size-1 or y2 > self.size-1 ):
                    print(f"One or more of the coordinates ({x1},{y1}) or ({x2},{y2}) specifies an out of bounds index")
                    return None
                
                else:
                    newGrid = copy.deepcopy(self.grid)
                    newGrid[x1][y1],newGrid[x2][y2] = newGrid[x2][y2], newGrid[x1][y1]
                    newLookup = self.get_updated_lookup(x1, y1, x2, y2)
                    
                    return RubiksGrid(grid=newGrid, lookup=newLookup)
                
        
    
    def get_children(self,x,y):
        """
        Retun all the game boards that could result from some valid move
        """
        children = []
        for delta in [-1,1]:
                #Try all possible moves within 1 manhattan distance. If these are valid moves,
                #and return a child object, then append them to the list of children
                child1 = self.make_move(x, y, x + delta, y)
                child2 = self.make_move(x, y, x, y + delta)
                
                if child1:
                    children.append(child1)
                if child2:
                    children.append(child2)
                    
        return children    
                
    def find_blank(self):        
        """
        Find the blank square. This needs to be optimized for larger grids, as currently it's quadratic in the grid size
        """
        
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return (i, j)
        

    
    