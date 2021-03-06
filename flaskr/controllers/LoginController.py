from flask import render_template, url_for, session
from werkzeug.utils import redirect

from flaskr import get_db


def get_nav_items():
    return [
        {"name": "Homepage", "url": url_for('login')},
        {"name": "Statistieken", "url": url_for('players')},
    ]


class LoginController:
    def index(self):
        session['status'] = 'login'
        return render_template(
            "login.html",
            nav=get_nav_items()
        )

    def login(self, username):
        db = get_db()
        db.execute(
            'INSERT INTO users (username) VALUES (?)',
            (username,)
        )
        db.commit()
        user = db.execute(
            'SELECT * FROM users ORDER BY id DESC lIMIT(1)'
        ).fetchone()
        session['user'] = {
            "id": user['id'],
            "username": user['username']
        }
        return redirect(url_for('settings'))
