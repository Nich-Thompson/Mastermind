from flask import Flask, url_for
from flask import render_template
from flask import request, redirect

app = Flask(__name__)


def get_nav_items():
    return [
        {"name": "Homepage", "url": url_for('login')},
        {"name": "Statistieken", "url": '/'},
        {"name": "Over ons", "url": '/'}
        # {"name": "Statistieken", "url": url_for('statistics')},
        # {"name": "Over ons", "url": url_for('about_us')},
    ]


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        req = request.form
        username = req.get("username")
        return redirect(url_for('settings'))

    return render_template(
        "login.html",
        nav=get_nav_items(),
        title='Mastermind - Log In',
    )


@app.route('/settings', methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        req = request.form
        double_color = req.get('double_color')
        color_amount = req.get('color_amount')
        position_amount = req.get('position_amount')
        return redirect(url_for('game'))

    return render_template(
        "settings.html",
        nav=get_nav_items(),
        title='Mastermind - Settings',
    )


@app.route('/game', methods=["GET", "POST"])
def game():
    if request.method == "POST":
        req = request.form
        return redirect(url_for(''))

    return render_template(
        'game.html',
        nav=get_nav_items(),
        title='Mastermind - Game',
    )


if __name__ == '__main__':
    app.run()
