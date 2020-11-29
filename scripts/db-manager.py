from pathlib import Path
from dbcred import *
import re
import requests
import json
import mysql.connector
import sys


def update_movies_table():
    params = json.loads(sys.argv[2])
    add_movie = "INSERT INTO movies (filename,title,poster,link,ondisk) VALUES ('" + params['Filename'] + "','" + re.escape(params['Title']) + "','" + params['Poster'] + "','" + re.escape(params['Link']) + "', '1');"
    cursor.execute(add_movie)
    print("add movie: " + params['Filename'])
    db.commit()

def update_series_table():

	for filename in slist:
		if filename not in slistdb:
			episodes = 0
			for f in Path("/data/media/series/" + filename).glob("**/*"):
				strf = str(f)
				if re.search(".*\.[mkv,avi,mp4]+$",strf):
					episodes += 1
							
			tarray = filename.split(".")
			qs = tarray.pop(0)
			y = 0

			for part in tarray:
				if re.search('^S[0-9][0-9]',part):
					y = part
					break
				else:
					qs = qs + "+" + part
			
			print(qs)
			print("y:" + str(y))
			print("e:" + str(episodes))
				
			url = "http://www.omdbapi.com/?apikey=64e7df7f&t=" + qs
				
			r = requests.get(url)
			j = json.loads(r.text)
			
			if j["Response"] == "True":
				add_series = "INSERT INTO series (filename,title,poster,season,episodes) VALUES ('" + filename + "','" + j['Title'] + "','" + j['Poster'] + "','" + str(y) + "','" + str(episodes) + "');"
				cursor.execute(add_series)
				print("add series: " + filename )
				db.commit()

	for filename in slistdb:
		if filename not in slist:
			del_series = "DELETE FROM series WHERE filename='" + filename + "';"
			cursor.execute(del_series)
			print("delete series: " + filename)
			db.commit()



if __name__ == "__main__":
	
	db = mysql.connector.connect(user=db_user,password=db_password, host='127.0.0.1',database='melonflix')
	cursor = db.cursor()
	
	if len(sys.argv) > 1:
		type = sys.argv[1]
		print("MANAGEDB.PY: UPDATING WITH THE TYPE : " + type)
		
		if type == 'movies':
			update_movies_table()
		elif type == 'series':
			update_series_table()
	else:
		print("MANAGEDB.PY: No argument was given")

	cursor.close()
	db.close()
