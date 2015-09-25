from . import Application
from .extensions import celery

if __name__ == '__main__':
    app = Application()
    with app.app_context():
        celery.start()
