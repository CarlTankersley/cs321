import unittest
import puzzle8
import search
import time

class TestMethods(unittest.TestCase):

    offTwoPuzzle = puzzle8.state([3,4,5,2,0,6,1,8,7])

    gradePuzzle1 = puzzle8.state([8,7,6,5,4,3,2,1,0])
    gradePuzzle2 = puzzle8.state([1,2,3,4,5,6,7,8,0])
    

    def setUp(self):
        self.gradePuzzles = [247860748,253206748,253780508,152293420,
                             300501380, 108306836]
        self.pathLengths = [2,4,8,10,12,16]

    def testItDeepGrading(self):
        print("The last iteration may be very slow. On my laptop, it took")
        print("approximately 5-6 minutes to run the last test.")
        startTime = time.time()
        for i in range(len(self.gradePuzzles)):
            print("\nTrying to find a solution for puzzle with solution of depth",
                  self.pathLengths[i])
            print("Starting puzzle:")
            puzzle8.display(self.gradePuzzles[i])
            solnPath = search.DFS(self.gradePuzzles[i], self.pathLengths[i])
            print("Found a solution, of depth", len(solnPath))
            print("Solution path:", solnPath)
            self.assertEqual(len(solnPath),self.pathLengths[i])
        print('it deep time',time.time()-startTime)
    


if __name__=='__main__':
    unittest.main()
