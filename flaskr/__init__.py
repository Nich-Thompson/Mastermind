import os

from flask import Flask, url_for, session
from flask import request, redirect

from flaskr.db import get_db
from flaskr.controllers.GameController import GameController
from flaskr.controllers.LoginController import LoginController

login_controller = LoginController()
game_controller = GameController()


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
        session.clear()
        if request.method == "POST":
            req = request.form
            username = req.get("username")
            return login_controller.login(username)
        return login_controller.index()

    @app.route('/settings', methods=["GET", "POST"])
    def settings():
        if session.get('user_id') is None:
            return redirect(url_for('login'))
        if request.method == "POST":
            req = request.form
            return game_controller.create_game(int(req.get('position_width')), int(req.get('position_height')),
                                               int(req.get('color_amount')), bool(req.get('double_color')))
        return game_controller.settings()

    @app.route('/game', methods=["GET", "POST"])
    def game():
        print(game_controller.get_game().user_id)
        if session.get('user_id') is None:
            return redirect(url_for('login'))
        if request.method == "POST":
            req = request.form
            return redirect(url_for(''))

        return game_controller.load_game()

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
        game_controller.submit()
        return game_controller.load_game()

    return app


if __name__ == '__main__':
    app = create_app()
    login_controller.set_nav()
    game_controller.set_nav()
    app.run()
