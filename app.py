from flask import Flask, url_for
from flask import render_template
from flask import request, redirect

app = Flask(__name__)

def getNavItems():
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
        nav=getNavItems(),
        title='Mastermind - Log In',
    )

@app.route('/settings', methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        req = request.form
        double_color = req.get('doubleColor')
        color_amount = req.get('colorAmount')
        position_amount = req.get('positionAmount')
        return redirect(url_for('game'))

    return render_template(
        "settings.html",
        nav=getNavItems(),
        title='Mastermind - Settings',
    )

@app.route('/game', methods=["GET", "POST"])
def game():
    if request.method == "POST":
        req = request.form
        return redirect(url_for(''))

    return render_template(
        'game.html',
        nav=getNavItems(),
        title='Mastermind - Game',
    )

if __name__ == '__main__':
    app.run()