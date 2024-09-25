import os
from pool import conn
import routes
import flask

app = flask.Flask(__name__)

cur = conn.cursor()
conn.commit()

cur.close()
conn.close()
