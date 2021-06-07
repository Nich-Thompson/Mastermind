from flask import render_template, url_for, session
from werkzeug.utils import redirect

from flaskr import get_db
from flaskr.models.Game import Game


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
        self.status = 'settings'

    def settings(self):
        self.status = 'settings'
        return render_template(
            "settings.html",
            nav=get_nav_items(),
            title='Mastermind - Settings',
        )

    def get_game(self):
        return self.game

    def create_game(self, number_of_columns, number_of_rows, number_of_colors, can_use_double_colors):
        self.status = 'playing'
        self.game = Game(number_of_columns, number_of_rows, number_of_colors, can_use_double_colors)
        return self.load_game()

    def load_game(self):
        return render_template(
            'game.html',
            nav=get_nav_items(),
            title='Mastermind - Game',
            position_width=self.game.board.number_of_columns,
            position_height=self.game.board.number_of_rows,
            colors=self.game.colors,
            current_color=self.game.current_color,
            current_code_input=self.game.current_code_input,
            squares=self.game.board.squares,
        )

    def submit(self):
        num = self.game.number_of_guesses
        for i in range(self.game.height):
            self.game.board.squares[i][num] = self.game.current_code_input[i]
        self.game.number_of_guesses += 1
        # TODO: Loss condition here

    def place(self, positions):
        result = self.game.check_positions(positions)
        if result[0].length == self.game.code.length:
            self.status = 'won'
            db = get_db()
            db.execute(
                'INSERT INTO games (user_id, number_of_guesses, start_time) VALUES (?,?,?)',
                (self.game.user_id, self.game.number_of_guesses, self.game.start_time.strftime("%d %b, %Y %H:%M:%S"))
            )
            db.commit()
            return redirect(url_for('won'))

    def load_won(self, username):
        # db = get_db()
        # games = db.execute(
        #     'SELECT * FROM games'
        # )
        # for game in games:
        #     print(game['id'])
        #     print(game['number_of_guesses'])
        #     print(game['start_time'])
        return render_template(
            'won.html',
            nav=get_nav_items(),
            title='Mastermind - Game',
            username=username,
            number_of_guesses=self.game.number_of_guesses,
            start_time=self.game.start_time,
            code=self.game.code
        )
