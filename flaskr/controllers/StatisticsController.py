from flask import render_template, url_for

from flaskr import get_db


def get_nav_items():
    return [
        {"name": "Homepage", "url": url_for('login')},
        {"name": "Statistieken", "url": url_for('statistics')},
        {"name": "Over ons", "url": '/'}
        # {"name": "Over ons", "url": url_for('about_us')},
    ]


class StatisticsController:
    def __init__(self):
        self.view = None

    def get_statistics(self):
        return render_template(
            "statistics.html",
            nav=get_nav_items(),
            title='Mastermind - Statistieken',
            stats=self.load_statistics(),
        )

    def load_statistics(self):
        db = get_db()
        cursor_object = db.execute('SELECT * FROM games')
        stats = cursor_object.fetchall()
        return stats