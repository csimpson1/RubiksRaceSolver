from game_grid import RandomGrid,RubiksGrid

class Engine:
    
    def __init__(self,startingGrid,targetGrid):
        self.startingGrid = startingGrid
        self.currentGrid = startingGrid
        self.targetGrid = targetGrid
        self.seen = {}
        self.visited = []
        
        #self.toVisit = [] #This is a priority queue
        #startingGridScore = self.score(self.startingGrid, 0)
        #heapq.heappush(self.toVisit, (startingGridScore, startingGrid))
        #heapq.heappush(self.toVisit, (0,heapq.heappush(self.toVisit, (startingGridScore, startingGrid)), startingGrid))
        """
        There's 9 3x3 squares that can be taken from a 5x5 grid. Inside the subgrid, a square can be at most 10 away from its destination (corner to corner case).
        So an upper bound on the worst case for one subgrid is 90
        """
        self.distanceUB = 2 * self.startingGrid.size
        self.scoreUB = self.distanceUB * (self.targetGrid.size) ** 2
        self.solved=False 
    
    def explore(self, depth = 0):
        print(self.currentGrid)
        deeper = depth + 1
        #Check if this is the first round of the game
        if depth == 0:
            self.currentGrid.score = self.score(self.currentGrid, 0)
        
        #If the current grid is solved, then we're done! Add it to the list of visited nodes, and return it
        
        if self.currentGrid.score == 0:
            self.visited.append(self.currentGrid)
            self.solved = True
        
        #If the grids not solved, get the children, score them and keep going
        else:
            
            blank = self.currentGrid.lookup[0]
            children = self.currentGrid.get_children(blank[0],blank[1])
            candidates = []
            """
            Check if a node has children, and if we've seen them before. If there's no children, or all of them were visited previously
            then return. There's no more exploration that can be done from this node.
            """
            
            for child in children:
                childInt = child.to_int()
                if childInt not in self.seen:
                    self.seen[childInt] = 1
                    child.score = self.score(child, depth=deeper)
                    candidates.append(child)
            
            if not candidates:
                self.visited.pop()
                return
            
            #Explore the children in order of highest score
            candidates.sort(key=lambda child:child.score, reverse=True)
            
            for child in candidates:
                self.visited.append(child)
                self.currentGrid = child
                self.explore(deeper)
        
            
        
    def score(self, rubiksGrid, depth):
        grid = rubiksGrid.grid
        size = self.targetGrid.size
        finalScore = self.scoreUB
        
        for i in range(len(grid) - size + 1):
            for j in range(len(grid)-size + 1):
                #print(f'{i} {j}')
                #There's a bug here, this grid is not correctly shaped
                #posTargetLoc = grid[i:i+size][j:j+size]
                """
                We want to extract subgrids of size n. There's two counter's here. The first 
                will go from 0 to (size of main grid) - (size of target grid, call this k. The second,
                goes from k to k + size.
                
                """
                posTargetLoc = [grid[k][j:j+size] for k in range(i, i+size)]
                partialScore = 0
                candidateScore = 0
                
                #Bug here: The coordinates, k,l are local. We need them as global coordinates
                for k in range(size):
                    for l in range(size):
                        
                        #if i == 2 and j == 2:
                            #print('here')
                            #print(f'translated x coord is {i + k}')
                            #print(f'translated y coord is {j + l}')
                        
                        color = posTargetLoc[k][l]
                        targetColor = self.targetGrid.grid[k][l]
                        if color != targetColor:
                            choices = rubiksGrid.lookup[targetColor]
                            minDistance = self.distanceUB #Again the maximum distance in an nxn grid is corner to corner, or n+n in manhattan distance
                
                            for choice in choices:
                                #k, l are the local coordinates in the subgrd we've chosen. (i,j) is the top corner in the subgrid in global coords.
                                distance = abs((i+k)-choice[0]) + abs((j + l)-choice[1])
                                if distance < minDistance:
                                    minDistance = distance
                            partialScore += minDistance
                candidateScore += partialScore
                #print(f'Done a grid: Score={candidateScore}')
                
                if candidateScore < finalScore:
                    finalScore = candidateScore
                    
                if candidateScore == 0:
                    self.solved = True
                    
                
        finalScore += depth
        return finalScore
    
    def is_solved(self, grid):
        if self.score(grid,0) == 0:
            return True
        else:
            return False

if __name__ == '__main__':
    
    grid = [
    [4, 5, 6, 2, 0],
    [4, 2, 4, 5, 1],
    [3, 3, 2, 1, 5], 
    [1, 2, 4, 6, 5], 
    [1, 3, 6, 3, 6]]
    
    grid1 = [
    [4,5,0,6,2],
    [4,2,4,5,1],
    [3,3,2,1,5],
    [1,2,4,6,5],
    [1,3,6,3,6]
    ]
    
    tGrid = [
        [2, 5, 5],
        [4, 6, 5],
        [6, 3, 6]]
    
    rubiksGrid = RubiksGrid(grid=grid1)
    targetGrid = RandomGrid(grid=tGrid)
    
    engine = Engine(startingGrid=rubiksGrid, targetGrid=targetGrid)
    #print(engine.score(engine.startingGrid,depth=1))
    
    engine.explore()
    if engine.solved:
        for node in engine.visited:
            print(node)
    
                            
                                