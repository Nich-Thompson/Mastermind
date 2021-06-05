import os

from flask import Flask, url_for, session
from flask import render_template
from flask import request, redirect
from flaskr.db import get_db
from .Game import Game
from json import JSONEncoder
from json import JSONDecoder


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
            db = get_db()
            db.execute(
                'INSERT INTO user (username) VALUES (?)',
                (username,)
            )
            db.commit()
            user = db.execute(
                'SELECT * FROM user ORDER BY id DESC lIMIT(1)'
            ).fetchone()
            session['user_id'] = user['id']
            return redirect(url_for('settings'))
        nav = get_nav_items()
        return render_template(
            "login.html",
            nav=nav
        )

    @app.route('/settings', methods=["GET", "POST"])
    def settings():
        if session.get('user_id') is None:
            return redirect(url_for('login'))
        if request.method == "POST":
            req = request.form
            session['double_color'] = req.get('double_color')
            session['color_amount'] = req.get('color_amount')
            session['position_width'] = req.get('position_width')
            session['position_height'] = req.get('position_height')
            session['game'] = JSONEncoder().encode(
                Game(None, int(req.get('position_width')), int(req.get('position_height')),
                     int(req.get('color_amount')), bool(req.get('double_color'))))
            print(JSONDecoder().decode(session['game']).number_of_guesses)
            return redirect(url_for('game'))

        return render_template(
            "settings.html",
            nav=get_nav_items(),
            title='Mastermind - Settings',
        )

    @app.route('/game', methods=["GET", "POST"])
    def game():
        if session.get('user_id') is None:
            return redirect(url_for('login'))
        if request.method == "POST":
            req = request.form
            return redirect(url_for(''))
        print(type(session.get('position_width')))
        print(session.get('position_width'))

        return render_template(
            'game.html',
            nav=get_nav_items(),
            title='Mastermind - Game',
        )

    @app.route('/select_color', methods=["GET", "POST"])
    def select_color():
        if request.method == "POST":
            return render_template(
                'game.html',
                nav=get_nav_items(),
                title='Mastermind - Game',
            )

    return app


def get_nav_items():
    return [
        {"name": "Homepage", "url": url_for('login')},
        {"name": "Statistieken", "url": '/'},
        {"name": "Over ons", "url": '/'}
        # {"name": "Statistieken", "url": url_for('statistics')},
        # {"name": "Over ons", "url": url_for('about_us')},
    ]


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

    def from_json(json_object):
        return Game(json_object['fname'])


if __name__ == '__main__':
    app = create_app()
    app.run()
