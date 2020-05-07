import numpy as np
import kivy
from math import inf as infinity
from itertools import product
from kivy.app import App
from collections import defaultdict
import random
import time

# Initializing the Tic-Tac-Toe environment
# Three rows-Three columns, creating an empty list of three empty lists
state_space = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
# No. of players = 2 : X & O
players = ['X', 'O']


# Defining the play state_value, player and the cell number
def play(sv, each_player, cell):
    if sv[int((cell - 1) / 3)][(cell - 1) % 3] is ' ':
        sv[int((cell - 1) / 3)][(cell - 1) % 3] = each_player
    else:
        cell = int(input(" Choose again, Cell is not empty: "))
        play(sv, each_player, cell)


# Defining new state function: which traverse over rows and columns and returns new state
def new(state):
    ns = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    for i in range(3):
        for j in range(3):
            ns[i][j] = state[i][j]
    return ns


# Determining the current state value and determining the win
def cur_state(state_space):
    if (state_space[0][0] == state_space[0][1] and state_space[0][1] == state_space[0][2] and state_space[0][
        0] is not ' '):
        return state_space[0][0], "Done"
    if (state_space[1][0] == state_space[1][1] and state_space[1][1] == state_space[1][2] and state_space[1][
        0] is not ' '):
        return state_space[1][0], "Done"
    if (state_space[2][0] == state_space[2][1] and state_space[2][1] == state_space[2][2] and state_space[2][
        0] is not ' '):
        return state_space[2][0], "Done"

    if (state_space[0][0] == state_space[1][0] and state_space[1][0] == state_space[2][0] and state_space[0][
        0] is not ' '):
        return state_space[0][0], "Done"
    if (state_space[0][1] == state_space[1][1] and state_space[1][1] == state_space[2][1] and state_space[0][
        1] is not ' '):
        return state_space[0][1], "Done"
    if (state_space[0][2] == state_space[1][2] and state_space[1][2] == state_space[2][2] and state_space[0][
        2] is not ' '):
        return state_space[0][2], "Done"

    if (state_space[0][0] == state_space[1][1] and state_space[1][1] == state_space[2][2] and state_space[0][
        0] is not ' '):
        return state_space[1][1], "Done"
    if (state_space[2][0] == state_space[1][1] and state_space[1][1] == state_space[0][2] and state_space[2][
        0] is not ' '):
        return state_space[1][1], "Done"
    # if none of the above is true there must be a draw
    draw = 0
    for i in range(3):
        for j in range(3):
            if state_space[i][j] is ' ':
                draw = 1
    if draw is 0:
        return None, "Draw"

    return None, "Not Done"


# Defining the outline of the Tic-Tac Toe for the state_space or environment
def outline(state_space):
    print('----------------')
    print('| ' + str(state_space[0][0]) + ' || ' + str(state_space[0][1]) + ' || ' + str(state_space[0][2]) + ' |')
    print('----------------')
    print('| ' + str(state_space[1][0]) + ' || ' + str(state_space[1][1]) + ' || ' + str(state_space[1][2]) + ' |')
    print('----------------')
    print('| ' + str(state_space[2][0]) + ' || ' + str(state_space[2][1]) + ' || ' + str(state_space[2][2]) + ' |')
    print('----------------')


# Initializing state values
each_player = ['X', 'O', ' ']
states_dictionary = {}
# listing all possible states
states = [[list(i[0:3]), list(i[3:6]), list(i[6:10])] for i in product(each_player, repeat=9)]
# getting Total number of states
Total_states = len(states)
print("Total number of states = ", Total_states)
# Total number of moves/ actions in Tic-Tac-Toe is 9
Total_moves = 9
print("Total number of actions = ", Total_moves)
# Intializing agent intial value as 0
sv_O = np.full(Total_states, 0.0)

# Defining the state values for agent O
for i in range(Total_states):
    states_dictionary[i] = states[i]
    won_by, _ = cur_state(states_dictionary[i])
    if won_by == 'X':
        sv_O[i] = -1
    elif won_by == 'O':
        sv_O[i] = 1


# Using Update rule of Temporal difference to update the state value of 'O'
# V(s) <- V(s) + alpha * ((V(s^f) - V(s))
# current_state_value <- current_state_value + learning_rate * (new_state_value - current_state_value)
def update_O(alpha, csv, nsv):
    # alpha: learning rate, csv: current state value, nsv: next state value
    sv_O[csv] = sv_O[csv] + alpha * sv_O[nsv]


# Testing our Tic-Tac-Toe agent 'O' vs. Human
# Temporal difference: A RL Algo.
def TD(sv, each_player):
    actions = []
    curr_state_values = []
    empty_cells = []
    for i in range(3):
        for j in range(3):
            if sv[i][j] is ' ':
                empty_cells.append(i * 3 + (j + 1))

    for empty_cell in empty_cells:
        actions.append(empty_cell)
        new_state = new(sv)
        play(new_state, each_player, empty_cell)
        next_sid = list(states_dictionary.keys())[list(states_dictionary.values()).index(new_state)]
        curr_state_values.append(sv_O[next_sid])

    print('Possible Action moves = ' + str(actions))
    print('Action Move values = ' + str(curr_state_values))
    best_move_id = np.argmax(curr_state_values)
    best_move = actions[best_move_id]
    return best_move


# Now Playing
# Loading policy or the trained state values
sv_O = np.loadtxt('lib/game/trained_O.txt', dtype=np.float64)

play_more = "Y"
while play_more == 'Y' or play_more == 'y':
    state_space = [[' ', ' ', ' '],[' ', ' ', ' '],[' ', ' ', ' ']]
    curr_state = "Not Done"
    print("\n Let's start New Game!")
    outline(state_space)
    #todo choose player
    input_choice = input("Choose which player to go first - X (Human) or O(RL Agent): ")
    won_by = None

    if input_choice == 'X' or input_choice == 'x':
        cid = 0
    else:
        cid = 1

    while curr_state == "Not Done":
        csv = list(states_dictionary.keys())[list(states_dictionary.values()).index(state_space)]
        if cid == 0:
            print("Now Human's turn:")
            cell_select = int(input("It's your turn! Choose a block to place X (1 to 9): "))
            play(state_space, players[cid], cell_select)

        else:
            cell_select = TD(state_space,players[cid])
            play(state_space,players[cid], cell_select)
            print("Agent O placed at" + str(cell_select))

        outline(state_space)
        won_by, curr_state = cur_state(state_space)
        if won_by is not None:
            print(str(won_by) + " Won Won Won!")
        elif curr_state is "Draw":
            print("Draw Draw Draw!!!")
        else:
            cid = (cid + 1) % 2

    play_more = input('Wanna Play more? Hit Y/N')
print('See you again! :D')

