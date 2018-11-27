'''
    THIS IS A TIC-TAC-TOE GAME
    DEVELOPED BY : MITHUN SHOKHWAL
    FIRST GAME CREATED IN PYTHON 30
'''
from random import randint
import os

def clear():
    '''
        CLEAR SCREEN FOR LINUX / UNIX
    '''
    os.system("clear")

def display_board():
    '''
        DISPLAY BOARD FOR TIC-TAC-TOE
    '''
    print(f"\nPlayer {PLAYER_NAME[1]} : {PLAYER_MARKER[1]}")
    print(f"Player {PLAYER_NAME[2]} : {PLAYER_MARKER[2]}")
    print(' {0:^16} || {1:^16} || {2:^16} '.format('', '', ''))
    print(' {0:^16} || {1:^16} || {2:^16} '.format('', '', ''))
    print(' {0:^16} || {1:^16} || {2:^16} '.format(BOARD[1], BOARD[2], BOARD[3]))
    print(' {0:^16} || {1:^16} || {2:^16} '.format('', '', ''))
    print(' {0:^16} || {1:^16} || {2:^16} '.format('', '', ''))
    print(' {0:=<16} <> {1:=^16} <> {2:=>16} '.format('=', '=', '='))
    print(' {0:^16} || {1:^16} || {2:^16} '.format('', '', ''))
    print(' {0:^16} || {1:^16} || {2:^16} '.format('', '', ''))
    print(' {0:^16} || {1:^16} || {2:^16} '.format(BOARD[4], BOARD[5], BOARD[6]))
    print(' {0:^16} || {1:^16} || {2:^16} '.format('', '', ''))
    print(' {0:^16} || {1:^16} || {2:^16} '.format('', '', ''))
    print(' {0:=<16} <> {1:=^16} <> {2:=>16} '.format('=', '=', '='))
    print(' {0:^16} || {1:^16} || {2:^16} '.format('', '', ''))
    print(' {0:^16} || {1:^16} || {2:^16} '.format('', '', ''))
    print(' {0:^16} || {1:^16} || {2:^16} '.format(BOARD[7], BOARD[8], BOARD[9]))
    print(' {0:^16} || {1:^16} || {2:^16} '.format('', '', ''))
    print(' {0:^16} || {1:^16} || {2:^16} '.format('', '', ''))


def player_input(player_num):
    '''
        GET PLAYER INPUT FROM USER
    '''
    while True:
        try:
            location = \
                int(input('\nPlayer {} : Enter position (1-9) : '.format(PLAYER_NAME[player_num])))
            if location not in range(1, 10) or BOARD[location] != '':
                print("Please enter a proper position")
                continue
            else:
                return location
        except ValueError:
            print("Please provide a valid Input")
            continue

def check_boardfull():
    '''
        CHECK IF BOARD IS FULL
    '''
    return '' not in BOARD[1:]

def init_game():
    '''
        INITIALISE GAME FOR THE BEGINNING
    '''
    first_player = randint(1, 2)
    while True:
        marker = \
            input("\nPlayer {}: Choose your marker between 'O' and 'X' : "\
                .format(PLAYER_NAME[first_player]))
        if marker.upper() not in ['X', 'O']:
            print('Invalid Marker, Please try Again!')
            continue
        else:
            PLAYER_MARKER[first_player] = marker.upper()
            if first_player == 1:
                first_player = 2
            else:
                first_player = 1
            if marker.upper() == 'X':
                marker = 'O'
            else:
                marker = 'X'
            PLAYER_MARKER[first_player] = marker
            break

def place_marker(play_marker, pos):
    '''
        PLACE THE MARKER FOR THE BOARD
    '''
    BOARD[pos] = play_marker
    display_board()

def win_check(marker):
    '''
        CHECK IF PLAYER HAS WON THE  GAME
    '''
    return BOARD[1] == BOARD[2] == BOARD[3] == marker or \
            BOARD[4] == BOARD[5] == BOARD[6] == marker or \
            BOARD[7] == BOARD[8] == BOARD[9] == marker or \
            BOARD[1] == BOARD[5] == BOARD[9] == marker or \
            BOARD[1] == BOARD[4] == BOARD[7] == marker or \
            BOARD[2] == BOARD[5] == BOARD[8] == marker or \
            BOARD[3] == BOARD[6] == BOARD[9] == marker or \
            BOARD[3] == BOARD[5] == BOARD[7] == marker

#initialize board
BOARD = ['#', '1', '2', '3', '4', '5', '6', '7', '8', '9']
PLAYER_MARKER = ['#', '-', '-']

## Just for fun
PLAYER_NAME = ['X', '01', '02']

os.system("clear")
display_board()

while True:

    #DECLARE GLOBAL VARIABLES

    BOARD = ['']*10
    PLAYER_MARKER = ['']*3
    PLAYER = randint(1, 2)

    init_game()
    clear()
    display_board()
    print('\nLets Begin the game......\n')
    while True:
        POSITION = player_input(PLAYER)
        os.system("clear")
        place_marker(PLAYER_MARKER[PLAYER], POSITION)
        if win_check(PLAYER_MARKER[PLAYER]):
            print('Player {} has won the game'.format(PLAYER_NAME[PLAYER]))
            break
        if check_boardfull():
            print('Match Drawn!')
            break
        if PLAYER == 1:
            PLAYER = 2
        else:
            PLAYER = 1

    ANS = input('\nWould you like to play the game again (Y/N) : ')
    if ANS.upper() == 'Y':
        clear()
        continue
    else:
        print('\nThanks for wasting your time.')
        break
