from flask import Flask
app = Flask(__name__)
app.secret_key = 'genrandomnum'
app.config.from_object('config')
from catalogapp import views
