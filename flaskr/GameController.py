from flask import render_template, url_for

from .Game import Game


def get_nav_items():
    return [
        {"name": "Homepage", "url": url_for('login')},
        {"name": "Statistieken", "url": '/'},
        {"name": "Over ons", "url": '/'}
        # {"name": "Statistieken", "url": url_for('statistics')},
        # {"name": "Over ons", "url": url_for('about_us')},
    ]


class GameController:
    def __init__(self):
        self.game = None

    def settings(self):
        return render_template(
            "settings.html",
            nav=get_nav_items(),
            title='Mastermind - Settings',
        )

    def get_game(self):
        return self.game

    def create_game(self, number_of_columns, number_of_rows, number_of_colors, can_use_double_colors):
        self.game = Game(number_of_columns, number_of_rows, number_of_colors, can_use_double_colors)
        return self.load_game()

    def load_game(self):
        return render_template(
            'game.html',
            nav=get_nav_items(),
            title='Mastermind - Game',
            position_width=self.game.board.number_of_columns,
        )
