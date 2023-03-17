import numpy as np
from itertools import product
import time


class Board:
    """
    The Board class is a wrapper for a list of lists that represents the sudoku, complete with a nice "__repr__" and methods for checking validity
    and solving sudokus. Zeros represent empty spaces.
    """
    def __init__(self, list_of_rows) -> None:
        self.numbers = list_of_rows
        self.length = len(self.numbers)
        assert self.length == len(list_of_rows[1])

    def __len__(self):
        return self.length
    
    def __repr__(self) -> str:
        print("")
            #This first function is for printing sudoku boards in the terminal. After the addition of the tkinter GUI, its obselete except for debugging..
        for i in range(self.length):
            if i % 3 == 0 and i != 0:
                print("- - - + - - - + - - -") #tells us to add a row of  - on
                                                    # every third row
            for j in range(len(self[i])):
                if j % 3 == 0 and j != 0:
                    print("| ", end = "")
                if j == 8:
                    if self[i, j] == 0:
                        print(".")
                    else:
                        print(self[i, j]) #We have to add this case so that it doesn't print the space rows on the same line
                else:
                    if self[i, j] == 0:
                        print("." + " ", end = "")
                    else:
                        print(str(self[i, j]) + " ", end ="")
        return ""

    def __getitem__(self, idx):
        if isinstance(idx, tuple):
            return self.numbers[idx[0]][idx[1]]
        else:
            return self.numbers[idx]

    def get_blocks(self):
        # This returns a np array, in which each list corresponds to 
        return np.array(self.numbers).reshape((3,3,3,3)).transpose((0,2,1,3)).reshape((9,9))
    
    def flip(self):
        return Board(np.array(self.numbers).T.tolist())


    def valid_check(self):
        target = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        blocks = self.get_blocks()
        for num in target:
            for i in range(self.length):
                # Define "row" the i'th row
                row = self[i]

                # Define "column" the i'th column
                col = [row[i] for row in self]

                # Define "block" the i'th block
                block = list(blocks[i])

                if row.count(num) > 1 or col.count(num) > 1 or block.count(num) > 1:
                    return False
                    #We return false if any of the conditions are not satisfied.

        return True

    def find_empties(self):
        return [(i,j) for i in range(self.length) for j in range(self.length) if self[i,j] == 0]

    def solved_check(self):
        target = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        blocks = self.get_blocks()
        for i in range(self.length):
            # Define "row" the i'th row
            row = self[i]

            # Define "column" the i'th column
            col = [row[i] for row in self]

                # Define "block" the i'th block
            block = blocks[i]


            if set(row) != target or set(col) != target or set(block) != target:
                return False
            
        return True
    
    def solve(self):
        """
        This is where the solving happens. We first try Donald Knuth's exact cover algorithm. If this hasn't presented a solution after a certain
        period of time, we resort to an exhaustive search backtracking algorithm. This is because the Knuth algorithm is bad at very sparse 
        sudokus that have many solutions.
        The Sudoku is assumed to be unsolvable if Knuth's algorithm terminates prematurely, or if no solution has been found within 10 seconds of 
        exhaustive search. 
        The exhaustive search with backtracking can be slow for certain inputs which require it to check a very large number of combinations. If the 
        search has not identified a quick solution, we transpose the matrix and try again. The combinations which were previously the last to be tried, are now the
        first, and so very long waits are avoided.

        I have yet to find a Sudoku for which this method does not return the desired solution/non-solution in an acceptable time 
        frame.
        """

        def exact_cover(x, y):
            x = {j: set() for j in x}
            for i, row in y.items():
                for j in row:
                    x[j].add(i)
            return x
        def solve(x, y, solution):
            if not x:
                yield list(solution)
            else:
                c = min(x, key=lambda c: len(x[c]))
                for r in list(x[c]):
                    solution.append(r)
                    cols = select(x, y, r)
                    for s in solve(x, y, solution):
                        yield s
                    deselect(x, y, r, cols)
                    solution.pop()

        def select(x, y, r):
            cols = []
            for j in y[r]:
                for i in x[j]:
                    for k in y[i]:
                        if k != j:
                            x[k].remove(i)
                cols.append(x.pop(j))
            return cols

        def deselect(x, y, r, cols):
            for j in reversed(y[r]):
                x[j] = cols.pop()
                for i in x[j]:
                    for k in y[i]:
                        if k != j:
                            x[k].add(i)

        start_time = time.time()
        try:
        
            grid = self.numbers
            res = [line for line in grid]
            x = ([("rc", rc) for rc in product(range(9), range(9))] +
                    [("rn", rn) for rn in product(range(9), range(1, 10))] +
                    [("cn", cn) for cn in product(range(9), range(1, 10))] +
                    [("bn", bn) for bn in product(range(9), range(1, 10))])
            y = dict()
            for r, c, n in product(range(9), range(9), range(1, 10)):
                b = (r // 3) * 3 + (c // 3)
                y[(r, c, n)] = [
                    ("rc", (r, c)),
                    ("rn", (r, n)),
                    ("cn", (c, n)),
                    ("bn", (b, n))]

            x = exact_cover(x, y)
            for i, line in enumerate(grid):
                for j, tile in enumerate(line):
                    if tile:
                        select(x, y, (i, j, tile))

            
            for solution in solve(x, y, []):
                if time.time() - start_time > 0.1:
                    raise TimeoutError
                for (r, c, n) in solution:
                    res[r][c] = n

            if any([0 in line for line in res]):
                # Return unsolvable if the Knuth algorithm terminates prematurely.
                return "Unsolvable"

            return Board(res)
        
        except:
            pass

        try:
            print("Using backtracking")
            
            newbo = Board(self.numbers)
            empties = newbo.find_empties()
            i = 0
            while not newbo.solved_check():

                if time.time() - start_time > 5:
                    raise TimeoutError
                
                newbo.numbers[empties[i][0]][empties[i][1]] = newbo[empties[i][0]][empties[i][1]] + 1 
                if newbo[empties[i][0], empties[i][1]] == 10:
                    newbo.numbers[empties[i][0]][empties[i][1]] = 0
                    i -= 1
                elif newbo.valid_check():
                    i += 1
            
            return newbo
        except:
            pass

        try:
            self.numbers = np.array(self.numbers).T.tolist()
            
        
            
            newbo = Board(self.numbers)
            empties = newbo.find_empties()
            i = 0
            while not newbo.solved_check():
                
                if time.time() - start_time > 10:
                    raise TimeoutError("appears to be impossible")

                newbo.numbers[empties[i][0]][empties[i][1]] = newbo[empties[i][0]][empties[i][1]] + 1 
                if newbo[empties[i][0], empties[i][1]] == 10:
                    newbo.numbers[empties[i][0]][empties[i][1]] = 0
                    i -= 1
                elif newbo.valid_check():
                    i += 1
            return newbo.flip()
        except:
            return "Unsolvable"
        

if __name__ == "__main__":
    bo = Board([
            [0, 0, 5, 0, 0, 0, 8, 0, 0],
            [8, 1, 6, 0, 0, 5, 4, 2, 7],
            [7, 0, 2, 6, 0, 0, 0, 1, 9],
            [2, 0, 0, 0, 0, 7, 3, 0, 1],
            [6, 9, 0, 1, 0, 8, 7, 0, 0],
            [3, 7, 1, 5, 0, 0, 0, 4, 0],
            [0, 6, 0, 9, 0, 2, 0, 0, 0],
            [1, 0, 3, 0, 4, 0, 9, 7, 0],
            [5, 8, 0, 7, 0, 0, 2, 6, 4]
        ])
    
    bo2 = Board([
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0 ,0],
            [0, 0, 3, 0, 0, 0, 0, 0 ,0],
            [0, 0, 0, 0, 0, 0, 0, 0 ,0],
            [0, 0, 0, 0, 5, 0, 0, 0 ,0],
            [0, 0, 0, 0, 0, 0, 0, 0 ,0],
            [0, 0, 0, 0, 0, 0, 0, 0 ,0],
            [0, 0, 0, 0, 0, 0, 0, 0 ,0],
            [9, 0, 0, 0, 0, 0, 0, 0 ,0]
        ])

    print(bo.solve())