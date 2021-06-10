import os

from flask import Flask, url_for, session
from flask import request, redirect

from flaskr.db import get_db
from flaskr.controllers.GameController import GameController
from flaskr.controllers.LoginController import LoginController
from flaskr.controllers.StatisticsController import StatisticsController

login_controller = LoginController()
game_controller = GameController()
statistics_controller = StatisticsController()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    @app.route('/', methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            req = request.form
            username = req.get("username")
            return login_controller.login(username)
        return login_controller.index()

    @app.route('/statistics', methods=["GET", "POST"])
    def statistics():
        return statistics_controller.get_statistics()

    @app.route('/settings', methods=["GET", "POST"])
    def settings():
        if session.get('user') is None:
            return redirect(url_for('login'))
        if session.get('status') != 'settings' and session.get('status') != 'won' and session.get('status') != 'login':
            return redirect(url_for('game'))

        if request.method == "POST":
            req = request.form
            return game_controller.create_game(int(req.get('position_width')), int(req.get('position_height')),
                                               int(req.get('color_amount')), bool(req.get('double_color')))
        return game_controller.settings()

    @app.route('/game', methods=["GET", "POST"])
    def game():
        if session.get('user') is None:
            return redirect(url_for('login'))
        if session.get('status') != 'playing':
            return redirect(url_for('settings'))

        if request.method == "POST":
            req = request.form
            return redirect(url_for(''))

        return game_controller.load_game()

    @app.route('/won', methods=["GET"])
    def won():
        if session.get('user') is None:
            return redirect(url_for('login'))
        if session.get('status') == 'lose':
            return redirect('lose')
        if session.get('status') != 'won':
            return redirect('game')
        return game_controller.load_won(session.get('user')['username'])

    @app.route('/color/<picked_color>', methods=["GET", "POST"])
    def pick_color(picked_color):
        game_controller.game.current_color = picked_color
        return game_controller.load_game()

    @app.route('/pin/<picked_pin>', methods=["GET", "POST"])
    def pick_pin(picked_pin):
        game_controller.game.current_code_input[int(picked_pin)] = game_controller.game.current_color
        return game_controller.load_game()

    @app.route('/submit', methods=["GET", "POST"])
    def submit():
        return game_controller.submit()

    return app


if __name__ == '__main__':
    app = create_app()
    login_controller.set_nav()
    game_controller.set_nav()
    app.run()
