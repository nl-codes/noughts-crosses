'''
Module to generate computer moves
Module to check leaderboard text file existance
Module to convert text file object format to dictionary
'''
import random
import os.path
import json
random.seed()

def draw_board(board):
    '''
    Draws board structure and 
    displays noughts and crosses'''

    for rows in board:
        print("\t  -------------  ")
        print("\t|",end="")
        for element in rows:
            print(f" {element} ",end=" |")    #element = [" ", "X", "O"]
        print()
    print("\t  -------------  ")


def welcome(board):
    '''Prints welcome message to user and
    draws the board'''

    print('Welcome to the "Unbeatable Noughts and Crosses" game.')
    print('The board layout is shown below:')
    draw_board(board)
    print('When prompted, enter the number corresponding to the square you want.')


def initialise_board(board):
    '''Set all cells of board to " " 1 space'''

    for row, elements in enumerate(board):
        for column, _ in enumerate(elements):
            board[row][column] = " "    #Empty all the cells of board
    return board

def get_player_move(board):
    '''Gets player move in integer and
    Returns row and column of integer in board'''

    while True:
        valid_input = range(1,10)
        flat_board = []
        for row in board:
            for point in row:
                flat_board.append(point)    #Converts nested list to a single list

        try:
            choice = input('\t\t\t1 2 3\n\t\t\t4 5 6\nChoose your square :\t7 8 9 : ')
            if not choice.isdigit():
                raise ValueError("Input inapprpriate, please enter integers 1-9")
            choice = int(choice)
            if choice not in valid_input:
                raise ValueError("Input out of range, please enter 1-9")
            if flat_board[choice - 1] != " ":
                raise ValueError("Cell already occupied, Please choose another cell")

            #Extract row and column from chosen integer index
            index = choice - 1
            total_columns = len(board[0])
            row = index // total_columns
            col = index % total_columns
            break
        except ValueError as err:
            print(f'error : {err}')
    return row, col

def choose_computer_move(board):
    '''Generates computer move in integer and
    Returns row and column of integer in board'''

    flat_board = []
    for row in board:
        for cell in row:
            flat_board.append(cell)    #Converts nested list to a single list

    while True:
        choice = random.randint(1,9)    #Generate random integer from 1 to 9
        try:
            if flat_board[choice - 1] != " ":    #Checks if cell is empty or not
                raise ValueError

            index = choice - 1
            total_columns = len(board[0])
            row = index // total_columns
            col = index % total_columns
            break
        except ValueError:
            pass
    return row, col


def check_for_win(board, mark):
    '''Checks if someone won the game
    Returns True is yes, no otherwise'''

    flat_board = []
    for row in board:
        for point in row:
            flat_board.append(point)    #Converts nested list to a single list

    win_condition = [
        flat_board[0] == flat_board[1] == flat_board[2] == mark, #Check Horizontal ...
        flat_board[3] == flat_board[4] == flat_board[5] == mark,
        flat_board[6] == flat_board[7] == flat_board[8] == mark,
        flat_board[0] == flat_board[3] == flat_board[6] == mark, #Check Vertical ...
        flat_board[1] == flat_board[4] == flat_board[7] == mark,
        flat_board[2] == flat_board[5] == flat_board[8] == mark,
        flat_board[0] == flat_board[4] == flat_board[8] == mark, #Check Diagonal ..
        flat_board[2] == flat_board[4] == flat_board[6] == mark
    ]
    if True in win_condition: #if any condition above is true, game is over
        return True
    return False

def check_for_draw(board):
    '''Checks if all cells are occupied
    Returns True if yes, False otherwise'''

    flat_board = []
    for row in board:
        for point in row:
            flat_board.append(point)    #Converts nested list to a single list

    if " "  in flat_board:    #If all cells aren't occupied, it isn't draw
        return False
    return True    #If all the cells are occupied, it is draw

def play_game(board):
    '''
    Displays welcome message,
    Initializes the board to be empty,
    Loop begins :
    Asks user for input,
    Updates board with user move and displays board,
    Checks if user won or tied the game,
    if user wins return 1 ,
    if tied returns 0,
    Computer plays move,
    Updates board with user move and displays board,
    Checks if computer won or tied the game,
    if computer wins return -1,
    if tied returns 0,
    Returns to loop,
    '''

    #Display welcome message, set all cells to empty, display the empty board
    initialise_board(board)
    draw_board(board)


    while True:
        #Prompts user to select cell, updates board with user move
        #Updates board with user move
        #Check if game is drawn
        #Check if game is won by payer
        row, column = get_player_move(board)
        board[row][column] = "X"
        if check_for_draw(board):
            print('|-----GAME DRAW-----|')
            return 0
        if check_for_win(board,"X"):
            print('|-----PLAYER WON-----|')
            return 1

        #Generates random cell to mark, updates board with computer move
        #Updates board with computer move
        #Check if game is drawn
        #Check if game is won by computer
        row, column = choose_computer_move(board)
        board[row][column] = "O"
        draw_board(board)
        if check_for_draw(board):
            print('|-----GAME DRAW-----|')
            return 0
        if check_for_win(board,"O"):
            print('|-----COMPUTER WON-----|')
            return -1

def menu():
    '''Prompts user for choice, validates choice and returns choice'''

    #Display menu options
    print('Enter one of the following options:')
    print('\t1 - Play the game')
    print('\t2 - Save score in file leaderboard.txt')
    print('\t3 - Load and display the scores from the leaderboard.txt')
    print('\tq - End the program')

    valid_input = ['1','2','3','q']
    while True:
        try:
            choice = input('1, 2, 3 or q? : ')
            if choice not in valid_input:
                raise ValueError ('Input out of option! Please choose : [1, 2, 3, or q]')
            break
        except ValueError as err:
            print(f"\nerror : {err}")
    return choice

def load_scores():
    '''Returns dictionary of {"Player" : Score} by
    Importing saved scores from leaderboard.txt'''

    try:
        if not os.path.exists("leaderboard.txt"):    #raise error if file doesn't exist
            raise FileNotFoundError
        with open('leaderboard.txt','r',encoding='utf-8') as score_board:
            text_file_data = score_board.read()
            if len(text_file_data) == 0:
                leaders = {}    #create new dictionary if there are no records
            else:
                leaders = json.loads(text_file_data)    #import data as dictionary
    except FileNotFoundError:
        print('\nerror : leaderboard.txt does not exist')
    return leaders

def save_score(score):
    '''Prompts user for name and
    Add the score of user to leaderboard.txt'''

    try:
        username = input('Enter your name : ')

        if not os.path.exists("leaderboard.txt"):    #raise error if file doesn't exist
            raise FileNotFoundError

        with open('leaderboard.txt','r',encoding='utf-8') as score_board:
            text_file_data = score_board.read()
            if len(text_file_data) == 0:
                leaders = {}    #create new dictionary if there are no existing records
            else:
                leaders = json.loads(text_file_data)    #import data as dictionary

        if username in leaders:
            #if user already played before, add score to existing
            score += leaders[username]

        add_score = {username : score}
        leaders.update(add_score)

        with open('leaderboard.txt','w',encoding='utf-8') as score_board:
            update = json.dumps(leaders, indent=2)    #write vertically in json formats
            score_board.write(update)
    except FileNotFoundError:
        print('\nerror : leaderboard.txt does not exist')


def display_leaderboard(leaders):
    '''Displays the name and score of player
    saved in leaderboard.txt'''

    print('S.N.\tName |=> Score')
    print('---------------------')
    count = 1
    for name, score in leaders.items():
        print(f'{count}.\t{name} |=> {score}')
        count += 1
