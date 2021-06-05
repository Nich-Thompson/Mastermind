import os

from flask import Flask, url_for, session
from flask import render_template
from flask import request, redirect
from flaskr.db import get_db


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
            db = get_db()
            db.execute(
                'INSERT INTO user (username) VALUES (?)',
                (username,)
            )
            db.commit()
            user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('settings', username=user['username']))
        nav = [
            {"name": "Homepage", "url": url_for('login')},
            {"name": "Statistieken", "url": '/'},
            {"name": "Over ons", "url": '/'}
            # {"name": "Statistieken", "url": url_for('statistics')},
            # {"name": "Over ons", "url": url_for('about_us')},
        ]
        return render_template(
            "login.html",
            nav=nav
        )

    @app.route('/settings/<username>')
    def settings(username):
        return render_template(
            "settings.html",
            username=username
        )

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()