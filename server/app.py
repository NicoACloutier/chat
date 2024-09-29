import os
from pool import conn
from routes import users
import flask

app = flask.Flask(__name__)

cur = conn.cursor()
conn.commit()

users.create_user_api(app, conn)
