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
        nav=getNavItems()
    )

@app.route('/settings')
def settings():
    if request.method == "POST":
        return redirect(url_for('settings'))
    
    return render_template(
        "settings.html",
        nav=getNavItems(),
    )

if __name__ == '__main__':
    app.run()