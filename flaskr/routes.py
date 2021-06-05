from flask import Flask, url_for, session
from flask import render_template
from flask import request, redirect
from flaskr.db import get_db
from flask import Blueprint

site = Blueprint('site', __name__, template_folder='templates')


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
        return redirect(url_for('settings', user['username']))
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
