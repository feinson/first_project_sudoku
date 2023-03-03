import numpy as np

class Board:

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
    
    def solver(self):
        newbo = Board(self.numbers)
        empties = newbo.find_empties()
        i = 0
        while not newbo.solved_check():
            newbo.numbers[empties[i][0]][empties[i][1]] = newbo[empties[i][0]][empties[i][1]] + 1 
            if newbo[empties[i][0], empties[i][1]] == 10:
                newbo.numbers[empties[i][0]][empties[i][1]] = 0
                i -= 1
            elif newbo.valid_check():
                i += 1
        return newbo

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

    print(bo.solver())