import copy


def is_done(board):
    for element in ["O", "X"]:
        # Check both diagonals
        if board[0][0] == board[1][1] == board[2][2] == element or board[0][2] == board[1][1] == board[2][0] == element:
            return True, element  # Returns True and the winning element if either diagonal is completed.
        # Check rows and columns
        for i in [0, 1, 2]:
            if board[i][0] == board[i][1] == board[i][2] == element or board[0][i] == board[1][i] == board[2][i] == element:
                return True, element  # Returns True and the winning element if any row or column is completed.
    return False, ""  # No winner yet, so return False and an empty string.


def get_emptyplaces(board):
    list = []
    for i in [0, 1, 2]:
        for j in [0, 1, 2]:
            if board[i][j] == " ":
                list.append((i, j))  # Appends the position (row, column) if it is empty.
    return list


def print_board(board):
    print("\n")
    for i in board:
        print(i)


def minimax(board, is_maximising, p, alpha, beta):
    count.append("")  # Tracks nodes checked to measure performance.
    empty = get_emptyplaces(board)  # Get all empty spaces for possible moves.
    check = is_done(board)  # Check if there's a winner or the game is over.

    # Base case: if there's a winner
    if check[0]:
        if check[1] == "X":  # AI wins
            return 1, 0
        else:  # Opponent wins
            return -1, 0
    # Base case: if it's a draw (no moves left)
    if len(empty) == 0:
        return 0, 0

    if is_maximising:  # AI's turn to maximize score
        best = -1  # Initialize best score as the lowest
        best_move = empty[0]  # Default best move
        for i in empty:
            temp_board = copy.deepcopy(board)
            temp_board[i[0]][i[1]] = "X"  # Simulate the move
            return_value = minimax(temp_board, False, p + 1, alpha, beta)  # Recursive call
            if best < return_value[0]:  # Check if this move is better
                best = return_value[0]
                best_move = i
        return best, best_move  # Return best score and best move
    else:  # Opponent's turn to minimize score
        best_min = 1  # Initialize best score as the highest
        best_min_move = empty[0]  # Default best move
        for i in empty:
            temp_board = copy.deepcopy(board)
            temp_board[i[0]][i[1]] = "O"  # Simulate the move
            return_value = minimax(temp_board, True, p + 1, alpha, beta)  # Recursive call
            if best_min > return_value[0]:  # Check if this move is better
                best_min = return_value[0]
                best_min_move = i
        return best_min, best_min_move  # Return best score and best move



count = []
while True:
    print("\n\n---Sampik Gupta MiniMax---\n")
    use_pruning = input("Enter 1 to use alpha beta pruning, else anything else\n")
    Board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]  # Initialize an empty board.
    count = []
    won = False
    while len(get_emptyplaces(Board)) > 0:
        print_board(Board)  # Print the current board state.
        Check = is_done(Board)  # Check if there's a winner.
        if Check[0]:
            won = True
            print(Check[1], " Won")  # Display the winner.
            break
        t = tuple(map(int, input("Enter Location: ").split(',')))  # Get user input.
        if t in get_emptyplaces(Board):
            count = []
            Board[t[0]][t[1]] = "O"  # Human places "O" on their chosen spot.
            chosenLocation = minimax(Board, True, 0, -1, +1)  # AI calculates best move.
            c = chosenLocation[1]
            if c != 0:
                Board[c[0]][c[1]] = "X"  # AI places "X" at the best move location.
            print("Nodes Checked: ", len(count))  # Display number of nodes checked.
        else:
            print("Occupied!")  # Warns if the spot is already occupied.
    if not won:
        print("Draw")  # If no moves are left and no winner, declare a draw.



