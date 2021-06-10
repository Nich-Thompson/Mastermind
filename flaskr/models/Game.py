from datetime import datetime
import random
from enum import Enum

from flask import session


def count_result(result):
    count = 0
    for key in result:
        count += result[key]
    return count


class Game:
    def __init__(self, number_of_columns, number_of_rows, number_of_colors, can_use_double_colors, cheat_mode):
        self.user_id = session.get('user')['id']
        self.board = Board(number_of_columns, number_of_rows)
        self.number_of_guesses = 0
        self.start_time = datetime.now()
        self.colors = []
        self.code = []
        self.set_colors(number_of_colors)
        self.current_color = self.colors[0].name
        self.generate_code(number_of_columns, can_use_double_colors)
        self.height = number_of_columns
        self.losing_condition = number_of_rows
        self.current_code_input = {}
        self.cheat_mode = cheat_mode
        for i in range(number_of_columns):
            self.current_code_input[i] = self.colors[0].name

    def set_colors(self, number_of_colors):
        class Colors(Enum):
            red = 0
            orange = 2
            yellow = 4
            green = 6
            blue = 8
            purple = 1
            pink = 3
            brown = 5
            white = 7
            black = 9

        for i in range(number_of_colors):
            self.colors.append(Colors(i))

    def generate_code(self, number_of_columns, can_use_double_colors):
        colors = self.colors.copy()
        for i in range(number_of_columns):
            color = colors[random.randint(0, len(colors) - 1)]
            self.code.append(color.name)
            if not can_use_double_colors:
                colors.remove(color)
        print('code: {}'.format(self.code))

    def check_positions(self, positions):
        colors_in_code = self.get_colors_in_code()
        correct = {}
        right_color = {}
        incorrect = {}

        positions = list(positions.values())
        print('guess: {}'.format(positions))

        for index in range(len(positions)):
            if self.code[index] == positions[index]:
                if positions[index] in correct.keys():
                    correct[positions[index]] += 1
                else:
                    correct[positions[index]] = 1
            else:
                check = False
                for index2 in range(len(self.code)):
                    if self.code[index2] == positions[index]:
                        check = True
                        break
                if check:
                    if positions[index] in right_color.keys():
                        right_color[positions[index]] += 1
                    else:
                        right_color[positions[index]] = 1
                else:
                    if positions[index] in incorrect.keys():
                        incorrect[positions[index]] += 1
                    else:
                        incorrect[positions[index]] = 1

        remove_keys = []
        for color in right_color:
            diff = 0
            if color in correct.keys():
                if color in colors_in_code.keys():
                    diff = correct[color] + right_color[color] - colors_in_code[color]
            if diff > 0:
                right_color[color] -= diff
                if color in incorrect.keys():
                    incorrect[color] += 1
                else:
                    incorrect[color] = 1
                for count in range(diff - 1):
                    incorrect[color] += 1
                if right_color[color] == 0:
                    remove_keys.append(color)

        for color in remove_keys:
            del right_color[color]
        return {'correct': count_result(correct), 'right_color': count_result(right_color),
                'incorrect': count_result(incorrect)}

    def get_colors_in_code(self):
        colors = {}
        for index in range(len(self.code)):
            if self.code[index] in colors.keys():
                colors[self.code[index]] += 1
            else:
                colors[self.code[index]] = 1
        return colors


class Board:
    def __init__(self, number_of_columns, number_of_rows):
        self.number_of_columns = number_of_columns
        self.number_of_rows = number_of_rows
        self.squares = []
        self.feedback = []
        new = []
        for i in range(number_of_columns):
            for j in range(number_of_rows):
                new.append(None)
            self.squares.append(new)
            new = []
        self.current_row = 0

    def get_current_row(self):
        return self.squares[self.current_row]

    def set_feedback(self, feedback):
        self.feedback.append(feedback)

    def place(self, positions):
        for i in range(self.number_of_columns):
            self.squares[i][self.current_row] = positions[i]
        self.current_row += 1
