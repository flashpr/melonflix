#!/usr/bin/python3
from dbcred import *
import mysql.connector
import sys

# MANAGED BY torrent-[re]add.sh
filename = 'Se7en.1995.PROPER.REMASTERED.720p.BluRay.DTS-ES.x264.HuN-prldm'


db = mysql.connector.connect(user=db_user,password=db_password, host='127.0.0.1',database='melonflix')
cursor = db.cursor()

if len(sys.argv) > 1:
        # atjobs FILENAME AS ARG
        set_ondisk = "UPDATE movies SET ondisk='0' WHERE filename='" + sys.argv[1] + "';"
        cursor.execute(set_ondisk)
else:
        set_ondisk = "UPDATE movies SET ondisk='2' WHERE filename='" + filename + "';"
        cursor.execute(set_ondisk)

db.commit()
cursor.close()
db.close()
