from app import app, redirect_url
from flask import render_template, redirect, request
from dbcred import *
import os
import re
import mysql.connector


@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')

@app.route('/movies')
def movies():

    db = mysql.connector.connect(user=db_user, password=db_password, host='127.0.0.1',database='melonflix')

    cursor = db.cursor()
    
    query1 = "SELECT filename, title, poster, ondisk FROM movies WHERE ondisk=1 ORDER BY title ASC"
    query2 = "SELECT filename, title, poster, ondisk FROM movies WHERE ondisk=2 ORDER BY title ASC"
    query0 = "SELECT filename, title, poster, ondisk FROM movies WHERE ondisk=0 ORDER BY title ASC"
    
    cursor.execute(query1)
    list1 = cursor.fetchall()
    cursor.execute(query2)
    list2 = cursor.fetchall()
    cursor.execute(query0)
    list0 = cursor.fetchall()

    all_list = list1 + list2 + list0
    return render_template('movielist.html',lists=all_list)

@app.route('/series')
def series():

    cursor = db.cursor()
    
    query = "SELECT filename, title, poster, season FROM series ORDER BY title ASC"
    
    cursor.execute(query)

    return render_template('serieslist.html',lists=cursor)

@app.route('/episodes/<title>')
def episodes(title):

    cursor = db.cursor()

    query = "SELECT filename, title, poster, season, episodes FROM series WHERE filename='" + title + "'"
    cursor.execute(query)
    lists = cursor.fetchone()

    episodes = int(lists[4]) + 1

    return render_template('episodelist.html',lists=lists,episodes=episodes)


@app.route('/play/<video>')
def play(video):
    filename = video.split("+")[0]
    episode = ""
    if len(video.split("+")) > 1:
        episode = video.split("+")[1]

    db = mysql.connector.connect(user=db_user, password=db_password, host='127.0.0.1',database='melonflix')
    cursor = db.cursor()
    
    query = "SELECT title FROM movies WHERE filename='" + filename + "' UNION SELECT title FROM series WHERE filename='" + filename + "'"

    cursor.execute(query)
    title = cursor.fetchone()[0] + " " + episode
    
    cmd = 'DISPLAY=:0.0 vlc $(find /data/media/ \( -name "*.mkv" -o -name "*.avi" -o -name "*.mp4" \) | grep ' + filename + '.*' + episode + ' | grep -v -i sample) -f '
    os.popen(cmd)
    volume = os.popen('printf "%x" $(pactl list sinks | grep front-left: | cut -d " " -f3)').read()
    return render_template('controller.html',volume=volume, title=title)

@app.route('/rc/<action>')
def rc(action):
    if action == 'pause':
        os.popen('kill -s 19 $(pgrep vlc)')
    if action == 'resume':
        os.popen('kill -s 18 $(pgrep vlc)')
    if action == 'quit':
        os.popen('killall vlc')
        #return redirect('/')

@app.route('/addmedia', methods=['POST'])
def addmedia():
    url = request.form['url']

    cmd = "bash /opt/melonflix/scripts/torrent-add.sh '" + url + "'"
    os.popen(cmd)
    return redirect('/index')

@app.route('/test')
def test():
    pass
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')
