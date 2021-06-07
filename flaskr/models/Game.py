from datetime import datetime
import random
from flask import session


class Game:
    def __init__(self, number_of_columns, number_of_rows, number_of_colors, can_use_double_colors):
        self.user_id = session.get('user_id')
        self.board = Board(number_of_columns, number_of_rows)
        self.number_of_guesses = 0
        self.start_time = datetime.now()
        self.colors = []
        self.code = []
        self.set_colors(number_of_colors)
        self.generate_code(number_of_columns, can_use_double_colors)

    def set_colors(self, number_of_colors):
        possible_colors = ['']
        for i in range(number_of_colors):
            self.colors.append("#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]))

    def generate_code(self, number_of_columns, can_use_double_colors):
        colors = self.colors.copy()
        for i in range(number_of_columns):
            color = colors[random.randint(0, len(colors) - 1)]
            self.code.append(color)
            if not can_use_double_colors:
                colors.remove(color)

    def check_guess(self, guess):
        check = True
        for index in range(len(guess)):
            if self.code[index] != guess[index]:
                check = False
        return check


class Board:
    def __init__(self, number_of_columns, number_of_rows):
        self.number_of_columns = number_of_columns
        self.number_of_rows = number_of_rows
        self.squares = []
        new = []
        for i in range(number_of_rows):
            for j in range(number_of_columns):
                new.append(None)
            self.squares.append(new)
            new = []
        self.current_row = 0

    def get_current_row(self):
        return self.squares[self.current_row]
