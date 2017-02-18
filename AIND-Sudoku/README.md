# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: If there's a naked twin in the same unit regardless of unit's type such as row, column, diagonal,
   3 by 3square, the other boxes in the same unit can't take twin's domain value. For proving, let's suppose one other box in the same unit took one of twin's possible number. Then due to the basis that in a unit boxes have all different number, the twin boxes have one possible domain value. which is failure. So we can eliminate domain value of the other boxes in the same unit with that constraint.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: In case of the diagonal sudoku problem, boxes in the same diagonal should be all different number.
   So we consider not only row, column, 3 by 3 square but also diagonals. When using constraint strategy like elimination, only-choice, naked twin, it is performed on one unit at a time and in isolation from other units. So by simply adding diagonal units to unit collection. we can use already written constraint progagation algorithm and strategy as it is with little change. 

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.