# Sudoku solver project
This was my first ever completed Python project. It has a GUI which takes an unsolved sudoku board as input and fills in the blanks.

Since the initial completion I have cleaned some things up and made the algorithm more robust. It now 
does not get stuck in an infinite while loop when faced with certain unsolvable sudokus. I also combined all
of the solving methods into a ```Board``` class which can represent the values and comes with a nice ```__repr__```.

The solving algorithm is the exact cover algorithm invented by Donald Knuth. However, because this algorithm becomes inefficent for
sparse sudokus, we resort to backtracking if a solution is not found quickly.