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

    def settings(self):
        session['status'] = 'settings'
        return render_template(
            "settings.html",
            nav=get_nav_items(),
            title='Mastermind - Settings',
        )

    def get_game(self):
        return self.game

    def create_game(self, number_of_columns, number_of_rows, number_of_colors, can_use_double_colors, cheat_mode):
        session['status'] = 'playing'
        self.game = Game(number_of_columns, number_of_rows, number_of_colors, can_use_double_colors, cheat_mode)
        return self.load_game()

    def load_game(self):
        print(self.game.cheat_mode)
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
            pins=self.game.board.feedback,
            cheat_mode=self.game.cheat_mode,
            secret_code=self.game.code
        )

    def submit(self):
        self.game.board.place(self.game.current_code_input)
        self.game.number_of_guesses += 1

        result = self.game.check_positions(self.game.current_code_input)
        self.game.board.set_feedback(result)
        print('check result: {}'.format(result))
        print('feedback list: {}'.format(self.game.board.feedback))

        if result['correct'] == len(self.game.code):
            session['status'] = 'won'
            self.save_game()
            return redirect(url_for('won'))
        elif self.game.number_of_guesses == self.game.losing_condition:
            session['status'] = 'lose'
            self.save_game()
            return redirect(url_for('lose'))
        return redirect(url_for('game'))

    def save_game(self):
        db = get_db()
        db.execute(
            'INSERT INTO games (user_id, number_of_guesses, start_time) VALUES (?,?,?)',
            (self.game.user_id, self.game.number_of_guesses, self.game.start_time.strftime("%d %b, %Y %H:%M:%S"))
        )
        db.commit()

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
