import random
import numpy as np

from lib.game.player import Player
from itertools import product


class Bot(Player):
    state_space = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

    # Initializing state values
    each_player = ['X', 'O', ' ']

    states_dictionary = {}
    # listing all possible states
    states = [[list(i[0:3]), list(i[3:6]), list(i[6:10])] for i in product(each_player, repeat=9)]


    Total_moves = 9
    print("Total number of actions = ", Total_moves)

    # getting Total number of states
    Total_states = len(states)
    # Intializing agent intial value as 0
    sv_O = np.full(Total_states, 0.0)

    # Training file
    sv_O = np.loadtxt('lib/game/trained_O.txt', dtype=np.float64)

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

    # Defining the state values for agent O
    for i in range(Total_states):
        states_dictionary[i] = states[i]
        won_by, _ = cur_state(states_dictionary[i])
        if won_by == 'X':
            sv_O[i] = -1
        elif won_by == 'O':
            sv_O[i] = 1

    def check_draw(self, sv):
        draw = 0
        for i in range(3):
            for j in range(3):
                if sv[i][j] is ' ':
                    draw = 1
        if draw is 0:
            return 0, "Draw"

    def play(self, sv, each_player, cell):
        if sv[int((cell - 1) / 3)][(cell - 1) % 3] is ' ':
            sv[int((cell - 1) / 3)][(cell - 1) % 3] = each_player
        else:
            cell = int(input(" Choose again, Cell is not empty: "))
            sv.play(sv, each_player, cell)

    # Defining new state function: which traverse over rows and columns and returns new state
    def new(self, state):
        ns = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        for i in range(3):
            for j in range(3):
                ns[i][j] = state[i][j]
        return ns

    def get_Predicted_Values(self, sv):
        if(self.check_draw(sv)):
            return 0
        print("The current state :" + str(sv))
        actions = []
        curr_state_values = []
        empty_cells = []

        csv = list(self.states_dictionary.keys())[list(self.states_dictionary.values()).index(self.state_space)]
        for i in range(3):
            for j in range(3):
                if sv[i][j] is ' ':
                    empty_cells.append(i * 3 + (j + 1))
        for empty_cell in empty_cells:
            actions.append(empty_cell)
            new_state = self.new(sv)
            self.play(new_state, "O", empty_cell)
            next_sid = list(self.states_dictionary.keys())[list(self.states_dictionary.values()).index(new_state)]
            curr_state_values.append(self.sv_O[next_sid])

        print('Possible Action moves = ' + str(actions))
        print('Action Move values = ' + str(curr_state_values))
        best_move_id = np.argmax(curr_state_values)
        best_move = actions[best_move_id]
        return best_move
