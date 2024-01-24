def main():
    example_board = [
        [5, 1, 8, 6, 0, 0, 4, 0, 0],  # 0
        [0, 0, 6, 0, 0, 0, 0, 0, 7],  # 1
        [4, 3, 0, 2, 0, 0, 0, 0, 6],  # 2
        [7, 0, 0, 0, 0, 0, 0, 3, 0],  # 3
        [0, 6, 4, 0, 1, 8, 2, 0, 5],  # 4
        [0, 5, 0, 7, 2, 6, 9, 4, 8],  # 5
        [0, 0, 9, 0, 0, 1, 8, 2, 3],  # 6
        [0, 2, 1, 0, 0, 0, 7, 0, 0],  # 7
        [3, 0, 0, 0, 4, 0, 0, 6, 9],  # 8
    ]  # 0 1 2 3 4 5 6 7 8
    print("\n\nNew SudoKo Board:\n")
    print_board(example_board)
    fill_board(example_board)
    print("\n\nSOLVED:\n")
    print_board(example_board)
    print()


def print_board(board: list):
    """
    prints a Sudoku board.

    :param board: cells of Sudoku board
    :type board: 2D list of int
    :return: void function, prints out the Sudoku board
    :rtype: none
    """
    # loop through each row:
    for row in range(len(board)):
        # for every 3 row elemnt, we need to print out a horzontal line:
        if row != 0 and row % 3 == 0:  # make sure it's not the first row
            print("-" * 22)
        # loop through each column:
        for col in range(len(board[7])):  # why 7? cause it's lucky
            # for every 3 column elemnt, we need to print out a vertical line
            if col != 0 and col % 3 == 0:  # make sure it's not the first column
                print("| ", end="")  # make sure it doesn't go to next line
            # prints the cell element. But if it's the last column, we move to the next row:
            print(board[row][col]) if col == 8 else print(board[row][col], end=" ")


def find_empty_cell(board: list):
    """
    Finds empty Sudoku cell in a current row.

    :param board: Sudoku board
    :type board: 2D list of int
    :return: a coordinate of an empty cell
    :rtype: tuple of 2 int
    """
    # loop through each row
    for row in range(len(board)):
        # loop through each column
        for col in range(len(board[7])):  # why 7? cause it's lucky
            # if the cell is empty, denoted by 0, return the coordinate:
            if board[row][col] == 0:
                return row, col  # tuple of int

    # otherwise, if no empty cell, return nothing:
    return None


def validate_input(board: list, coordinate: tuple, input: int):
    """
    Check if input number we try satisfies the Sukdoku rules:
        - Each vertical column can only contain numbers from 1 to 9 with no duplicates
        - Each horizontal row can only contain numbers from 1 to 9 with no duplicates
        - Each 3 x 3 square can only contain numbers from 1 to 9 with no duplicates

    :param board: Sudoku board
    :param coordinate: coordiate of the cell we want to input the number
    :param input: an integer to try in the empty cell at 'coordinate'
    :type board: 2D list of int
    :type coordinate: tuple
    :type input: int
    :return: whether the number satisfies the rules
    :rtype: bool
    """
    # unpack the coordinate tuple:
    row_coord, col_coord = coordinate

    # FIRST, validate the COLUMN condition:
    # loop through every row cell of that specific column, EXCEPT the empty row_coord we are looking at:
    for row in range(len(board)):
        # if any of the existing elemnts equal our input number, retrun False immediately:
        if board[row][col_coord] == input and row != row_coord:
            return False

    # SECOND, validate the ROW condition:
    # loop through every column cell of that specific row, EXCEPT the empty col_coord we are looking at:
    for col in range(len(board[7])):
        # if any of the existing elements equal our input number, return False immediately:
        if board[row_coord][col] == input and col != col_coord:
            return False
    """
    Explanation of navigating each 3x3 squares and how to find it:
        0     1     2       3     4     5       6     7     8
    0 (0,0) (0,1) (0,2) | (0,3) (0,4) (0,5) | (0,6) (0,7) (0,8)
    1 (1,0) (1,1) (1,2) | (1,3) (1,4) (1,5) | (1,6) (1,7) (1,8)
    2 (2,0) (2,1) (2,2) | (2,3) (2,4) (2,5) | (2,6) (2,7) (2,8)
      ------------------|-------------------|-----------------
    3 (3,0) (3,1) (3,2) | (3,3) (3,4) (3,5) | (3,6) (3,7) (3,8)
    4 (4,0) (4,1) (4,2) | (4,3) (4,4) (4,5) | (4,6) (4,7) (4,8)
    5 (5,0) (5,1) (5,2) | (5,3) (5,4) (5,5) | (5,6) (5,7) (5,8)
      ------------------|-------------------|-----------------
    6 (6,0) (6,1) (6,2) | (6,3) (6,4) (6,5) | (6,6) (6,7) (6,8)
    7 (7,0) (7,1) (7,2) | (7,3) (7,4) (7,5) | (7,6) (7,7) (7,8)
    8 (8,0) (8,1) (8,2) | (8,3) (8,4) (8,5) | (8,6) (8,7) (8,8)

    :: Square Coordinate System ::
            0       1       2
        0 (0,0)   (0,1)   (0,2)
        1 (1,0)   (1,1)   (1,2)
        2 (2,0)   (2,1)   (2,2)

    Example: (5,2), Answer: Square 4 Why? Because its row_pos is less than 6 but more than 2 and its col_pos is less than 3

    How do we tell computer that?
        Well, 5 // 3 = 1 and 2 // 3 = 0
        Thus, the square coordinate is (1, 0), which is square 4.

    Notice that the Square coordinates have exact same coordinates as the Square 1.
    And all of the coordinates in Square 4 are related to (1,0):
        Row Indices of Square 4 is 3,4,5. Column Indices of Square 4 is 0,1,2
        Which means, the row indices of Square 4 ranges from 1 * 3 to (1 * 3) + 3, so [3, 6) or [3,5]
        Similarly, the column indices of Square 4 ranges from 0 * 3 to (0 * 3) + 3, so [0,3) or [0,2]
    """
    # THIRD, validate the 3 x 3 square condition:
    # we need to first figure out which 3x3 we are in currently:
    # first, find the Square Coordinates of that square:
    row_square, col_square = row_coord // 3, col_coord // 3
    # NOW, we'll check every cell in that square:
    # loop through each row of that square:
    for row in range(row_square * 3, row_square * 3 + 3):
        # loop through each column of that square:
        for col in range(col_square * 3, col_square * 3 + 3):
            # if any cell has same number as our input EXCEPT the cell we are inputting our number in, return False:
            if board[row][col] == input and (row, col) != coordinate:
                return False

    # by here, we should've checked every possible condition to raise False:
    return True


def fill_board(board: list):
    """
    Solves the Sudoku board using backtracking algorithm recursively.

    :param board: Sudoku board
    :type board: 2D list of int
    :return: boolean inidicating whether the board is complete or not
    :rtype: bool
    """
    # first, see if any empty cells left:
    empty_cell = find_empty_cell(board)  # this is a tuple

    # BASE_CASE: check if we have already completed the Sudoku board:
    if not empty_cell:
        # if no more empty cells, return True:
        return True
    else:  # Otherwise, keep solving
        # define an empty cell to solve:
        empty_row, empty_col = empty_cell  # unpacking a tuple

    # NOW: we are going to try numbers from 1 to 9 in the empty cell & see if it works:
    for input in range(1, 10):
        # if input works, replace the empty cell with that value:
        if validate_input(board, empty_cell, input):
            board[empty_row][empty_col] = input
            # After each replacement, recursively, check if the board is sovled:
            # if the board is not solved, recursion will happen and it will be ran until no more emtpy cells left:
            if fill_board(board):
                # if solved, end solving and return True
                return True
            # Otherwise, leave the empty cell unchanged because our previous input obvioulsy doens't work
            else:
                # atp, we know that there's no possible value for current cell, so we leave it unchanged, we backtrack to prev. cell
                board[empty_row][
                    empty_col
                ] = 0  # as we set it to empty cell again, we try next number in our for-loop

    # (part of recursion) If none of the numbers from 1 to 9 work in the current empty cell, return False, which means that remains as 0/empty.
    return False


if __name__ == "__main__":
    main()
