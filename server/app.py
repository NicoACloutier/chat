import os
from pool import conn

cur = conn.cursor()
conn.commit()

cur.close()
conn.close()
