from flask import Flask
app = Flask(__name__)
app.secret_key = 'genrandomnum'
app.config.from_object('config')
from catalogapp import views

if not app.debug:
    # Setup logging for application
    import logging
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler('tmp/catalogapp.log', 'a',
                                       1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('catalogapp startup')
