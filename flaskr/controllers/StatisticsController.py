from flask import render_template, url_for

from flaskr import get_db


def get_nav_items():
    return [
        {"name": "Homepage", "url": url_for('login')},
        {"name": "Statistieken", "url": url_for('players')},
        {"name": "Over ons", "url": '/'}
        # {"name": "Over ons", "url": url_for('about_us')},
    ]


class StatisticsController:
    def __init__(self):
        self.view = None

    def get_players(self):
        return render_template(
            "player_view.html",
            nav=get_nav_items(),
            title='Mastermind - Statistieken',
            stats=self.load_players(),
        )

    def get_statistics(self, username):
        return render_template(
            "statistics.html",
            nav=get_nav_items(),
            title='Mastermind - Statistieken',
            stats=self.load_statistics(username),
            username=username,
        )

    def load_players(self):
        db = get_db()
        cursor_object = db.execute('SELECT DISTINCT(username) FROM users')
        stats = cursor_object.fetchall()
        return stats

    def load_statistics(self, username):
        db = get_db()
        cursor_object = db.execute(
            'SELECT * FROM games WHERE user_id IN (SELECT id FROM users WHERE username = (?))',
            (username,)
        )
        stats = cursor_object.fetchall()
        return stats
