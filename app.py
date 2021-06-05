from flask import Flask, url_for, session
from flask import render_template
from flask import request, redirect

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


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
        session['username'] = req.get("username")
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
        session['double_color'] = req.get('double_color')
        session['color_amount'] = req.get('color_amount')
        session['position_width'] = req.get('position_width')
        session['position_height'] = req.get('position_height')
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


@app.route('/select_color', methods=["GET", "POST"])
def button():
    if request.method == "POST":
        return render_template(
            'game.html',
        )


if __name__ == '__main__':
    app.run()
