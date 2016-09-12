import time

class SudokuPuzzle():
    
    """
    Creates an empty sudoku template.
    """
    def __init__(self, puzzle):
        self.grid = []
        self.unsolvedCells = set()
        self.row = []
        self.column = []
        self.square = []
        #Lists the cells that aren't filled in yet.
        for i in range(81): 
            self.unsolvedCells.add(i)
        #Lists the possible values in each row, column and square.
        for i in range(9): 
            self.row.append(set(['1','2','3','4','5','6','7','8','9']))
        for i in range(9): 
            self.column.append(set(['1','2','3','4','5','6','7','8','9']))
        for i in range(9): 
            self.square.append(set(['1','2','3','4','5','6','7','8','9']))
        #Fills in the sudoku grid according to the puzzle.
        for i in range(81):
            ans = puzzle[i]
            self.grid.append(ans)
            if ans != '0':
                self.unsolvedCells.remove(i)
                nRow = i // 9
                nColumn = i % 9
                nSquare = (i // 27 * 3 + i % 9 // 3)
                self.row[nRow].remove(ans)
                self.column[nColumn].remove(ans)
                self.square[nSquare].remove(ans)
        return None
        
    """    
    Display these values as a 2-D grid.
    """
    def __str__(self):
        line = '+' + '+'.join(['-------']*3) + '+'
        sudokuPrint = line + '\n'
        for i in range(9):
            sudokuPrint += '| '
            for j in range(3):
                sudokuPrint += ' '.join(self.grid[i*9 + j*3:i*9 + j*3 + 3])
                sudokuPrint += ' | '
            sudokuPrint += '\n'
            if i == 2 or i == 5 or i==8:
                sudokuPrint += line + '\n'
        sudokuPrint += "Number of unsolved cells: "
        sudokuPrint += "{} \n".format(len(self.unsolvedCells))
        return sudokuPrint
    
    """    
    Eliminates possible values from unsolved cells and fills in answers
    if possible.
    """
    def scan(self): 
        nUnsolvedCells = -1
        #Loop stops when no cells are filled
        while len(self.unsolvedCells) != nUnsolvedCells:
            #Original number of unsolved cells before algorithm is run.
            nUnsolvedCells = len(self.unsolvedCells)
            solvedCells = []
            for i in list(self.unsolvedCells):
                nRow = i // 9
                nColumn = i % 9
                nSquare = (i // 27 * 3 + i % 9 // 3)
                #Determines the set of possible values by intersection of
                #possible values from the row, column and square.
                posValue = (self.row[nRow]
                            & self.column[nColumn] 
                            & self.square[nSquare])
                #Fills in the cell is there is only one possible answer.
                if len(posValue) == 1:
                    ans = next(iter(posValue))
                    self.grid[i] = ans
                    #Cell is solved.
                    self.unsolvedCells.remove(i)
                    #Removes possible values from the sets of its row,
                    #column and square.
                    self.row[nRow].remove(ans)
                    self.column[nColumn].remove(ans)
                    self.square[nSquare].remove(ans)
        return None
        
    """    
    Solves the puzzle.  
    """
    def solve(self):
        #Fills in solvable cells.
        self.scan()
        if len(self.unsolvedCells) == 0:
            return self
        minLength = 10
        
        #Determines the cell with the least number of possible values.
        for i in self.unsolvedCells:
            nRow = i // 9
            nColumn = i % 9
            nSquare = (i // 27 * 3 + i % 9 // 3)
            posValue = (self.row[nRow] 
                        & self.column[nColumn] 
                        & self.square[nSquare])
                        
            #Error: Board is unsolvable
            if len(posValue) == 0:
                return False
            
            #Stores the index, value of the cell and its associated
            #row, column and square.
            if len(posValue) < minLength:
                minIndex = i
                minLength = len(posValue)
                lowValue = posValue
                lowRow = nRow
                lowColumn = nColumn
                lowSquare = nSquare
                if minLength == 2:
                    break
            
        #Tries the possible values of the cell (i.e. guess and check)
        for j, ans in enumerate(lowValue):
            sudokuCopy = self.copy_board()
            sudokuCopy.grid[minIndex] = ans
            sudokuCopy.unsolvedCells.remove(minIndex)
            sudokuCopy.row[lowRow].remove(ans)
            sudokuCopy.column[lowColumn].remove(ans)
            sudokuCopy.square[lowSquare].remove(ans)
            sudokuCopy = sudokuCopy.solve()
            #There is a solution found.
            if sudokuCopy:
                return sudokuCopy
        #Line is executed when there is no solution.
        return sudokuCopy
    
    """
    Duplicates the current sudoku board.
    """
    def copy_board(self):
        sudokuCopy = SudokuPuzzle.__new__(SudokuPuzzle)
        sudokuCopy.grid = copy(self.grid)
        sudokuCopy.unsolvedCells = copy(self.unsolvedCells)
        sudokuCopy.row = copy(self.row)
        sudokuCopy.column = copy(self.column)
        sudokuCopy.square = copy(self.square)
        return sudokuCopy
        
"""
Displays sudoku puzzle and solution. 
"""
def display(puzzle, n):
    sudoku = SudokuPuzzle(puzzle)
    print('Puzzle {}'.format(n+1))
    print(sudoku)
    sudoku = sudoku.solve()
    if sudoku == False:
        print ('Puzzle {} has no solution.'.format(n+1))
        return False
    print('Puzzle {} SOLUTION'.format(n+1))
    print(sudoku)
    return True

"""
Deep copy function  
"""
def copy(array):
    if not isinstance(array, (list,set)):
        return array
    if isinstance(array, set):
        return {copy(entry) for entry in array}
    if isinstance(array, list):
        return [copy(entry) for entry in array]
    return None


"""
LET'S ROLL
"""
UnsolvedPuzzles = 0
TimeSolve = []
Puzzles = []

#50 easy sudoku puzzles from Project Euler   
string = str(open('p096_sudoku.txt', 'r').read())
string = string.split('\n')

n = -1
for i in string:
    if i[0] != 'G':
        Puzzles[n] += i
    else: 
        n += 1
        Puzzles.append('')

#95 hard puzzles from norvig.com
string = str(open('top95.txt', 'r').read())
string = string.split('\n')
for i in string:
        i = i.replace(".","0")
        Puzzles.append(i)

        
#11 harder puzzles from norvig.com
string = str(open('hardest.txt', 'r').read())
string = string.split('\n')
for i in string:
        i = i.replace(".","0")
        Puzzles.append(i)

#SOLVE THEM
for i in range(len(Puzzles)):
    start = time.time()
    solution = display(Puzzles[i], i)
    end = time.time()
    TimeSolve.append(end-start)
    if not solution:
        UnsolvedPuzzles += 1

    
print("Total number of unsolved puzzles: ", UnsolvedPuzzles)
max_time = max(TimeSolve)
max_puzzle = TimeSolve.index(max_time)
print("Longest Puzzle: ", max_puzzle)
print("Time taken: ", max_time)