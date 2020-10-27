import unittest
from game_grid import RubiksGrid

class TestGameGrid(unittest.TestCase):
    
    def setUp(self):
        self.randomGame = RubiksGrid()
        
        grid = [
            [4, 5, 6, 2, 0],
            [4, 2, 4, 5, 1],
            [3, 3, 2, 1, 5], 
            [1, 2, 4, 6, 5], 
            [1, 3, 6, 3, 6]]
        
        self.fixedGameEdge = RubiksGrid(grid=grid)
        
        fourChildren = [
            [4, 5, 6, 2, 5],
            [4, 2, 4, 0, 1],
            [3, 3, 2, 1, 5], 
            [1, 2, 4, 6, 5], 
            [1, 3, 6, 3, 6]]
        
        self.fixedGame = RubiksGrid(grid=fourChildren)
    
    def test_random_grid_setup(self):
        self.assertIsInstance(self.randomGame.find_blank(), tuple)
    
    def test_find_blank(self):
        self.assertEqual(self.fixedGameEdge.find_blank(), (0,4))
        
    def test_lookup(self):
        red = self.fixedGame.lookup[4]
        self.assertIn((0,0),red)
        self.assertIn((1,0), red)
        self.assertIn((1,2), red)
        self.assertIn((3,2), red)
        
        self.assertEqual(self.fixedGame.lookup[0],(1,3))
    def test_get_updated_lookup(self):
        newLookup = self.fixedGame.get_updated_lookup(1,3,1,2)
        color = self.fixedGame.grid[3][2]
        
        self.assertIn((0,0),newLookup[color])
        self.assertIn((1,0), newLookup[color])
        self.assertIn((1,2), newLookup[color])
        self.assertIn((3,2), newLookup[color])
    
    def test_make_move(self):
        legalMove = self.fixedGameEdge.make_move(0, 4, 1, 4)
        newGrid =[
            [4, 5, 6, 2, 1],
            [4, 2, 4, 5, 0],
            [3, 3, 2, 1, 5], 
            [1, 2, 4, 6, 5], 
            [1, 3, 6, 3, 6]]
        
        self.compare_grids(legalMove,newGrid)
        
        noMove = self.fixedGameEdge.make_move(0,4,0,4)
        self.assertIsNone(noMove)   
        
        notBlank = self.fixedGameEdge.make_move(0,3,0,4)
        self.assertIsNone(notBlank)
        
        jump = self.fixedGameEdge.make_move(0,4,2,4)
        self.assertIsNone(jump)
        
        negativeIdx = self.fixedGameEdge.make_move(0,4,-1,4)
        self.assertIsNone(negativeIdx)
        
        oobIdx = self.fixedGameEdge.make_move(0,4,0,5)
        self.assertIsNone(oobIdx)
        
        inverse = self.fixedGameEdge.make_move(0,4,1,4, previousMove=(1,4,0,4))
        self.assertIsNone(inverse)
        
        notInverse = self.fixedGameEdge.make_move(0,4,1,4,previousMove=(0,3,0,4))
        self.compare_grids(notInverse, newGrid)
        
        
        
    def test_get_children_edge(self):
        #Testing the edge case
        children = self.fixedGameEdge.get_children(0, 4)
        
        child1 = [
            [4, 5, 6, 2, 1],
            [4, 2, 4, 5, 0],
            [3, 3, 2, 1, 5], 
            [1, 2, 4, 6, 5], 
            [1, 3, 6, 3, 6]]
        
        child2 = [
            [4, 5, 6, 0, 2],
            [4, 2, 4, 5, 1],
            [3, 3, 2, 1, 5], 
            [1, 2, 4, 6, 5], 
            [1, 3, 6, 3, 6]]
        
        validMoves = [child1,child2]
        
        self.compare_children(children, validMoves)
        
    def test_get_children(self):
        kid1 = [
            [4, 5, 6, 0, 5],
            [4, 2, 4, 2, 1],
            [3, 3, 2, 1, 5], 
            [1, 2, 4, 6, 5], 
            [1, 3, 6, 3, 6]]
        
        kid2 = [
            [4, 5, 6, 2, 5],
            [4, 2, 4, 1, 0],
            [3, 3, 2, 1, 5], 
            [1, 2, 4, 6, 5], 
            [1, 3, 6, 3, 6]]
                
        kid3 = [
            [4, 5, 6, 2, 5],
            [4, 2, 4, 1, 1],
            [3, 3, 2, 0, 5], 
            [1, 2, 4, 6, 5], 
            [1, 3, 6, 3, 6]]
                
        kid4 = [
            [4, 5, 6, 2, 5],
            [4, 2, 0, 4, 1],
            [3, 3, 2, 1, 5], 
            [1, 2, 4, 6, 5], 
            [1, 3, 6, 3, 6]]
        
        validMoves = [kid1, kid2, kid3, kid4]
        children = self.fixedGame.get_children(1, 3)
        
        self.compare_children(children, validMoves)
        
    
    def test_to_int(self):
        """
        [4, 5, 6, 2, 5],
            [4, 2, 4, 0, 1],
            [3, 3, 2, 1, 5], 
            [1, 2, 4, 6, 5], 
            [1, 3, 6, 3, 6]]
        """
        rep = 4562542401332151246513636
        self.assertEqual(rep, self.fixedGame.to_int())
    
    """
    HELPER FUNCTIONS
    """            
    
    def compare_grids(self,grid1,grid2):
        """
        Compares a RubiksGrid object with a nested list
        """
        for i in range(len(grid1.grid)):
            for j in range(len(grid1.grid)):
                self.assertEqual(grid1.grid[i][j],grid2[i][j])    
    
    def compare_children(self,kids,validMoves):
        """
        Compare's a list of RubiksGrid objects against a list of grids
        """
        
        for child in kids:
            count = 0
            if child.grid in validMoves:
                count += 1
            
            self.assertEqual(count,1)
        
if __name__ == "__main__":
    unittest.main()