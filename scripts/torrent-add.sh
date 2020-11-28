#!/bin/bash

link=$1

transmission-remote -a $link --start-paused --torrent-done-script /opt/melonflix/scripts/torrent-done.py
sleep 1
id=`transmission-remote -l | tail -n2 | head -n1 | awk '{print $1}'`
name=`transmission-remote -t $id -i | grep Name | awk '{print $NF}'`

IFS='.' read -r -a array <<< "`echo $name | grep -o -e '.*[1,2][0,9][0-9][0-9][^p]\|.*S[0-9][0-9]'`"

l_array="${#array[@]}"
year="${array[$l_array-1]}"
title="${array[0]}"
for (( i=1; i<($l_array-1); i++ )); do
	title="$title+${array[$i]}"
done
    
if [ -n `echo $year | grep -e  '.*[1,2][0,9][0-9][0-9][^p]'` ]; then
	omdb=`curl -s "http://www.omdbapi.com/?apikey=64e7df7f&t=$title&y=$year"`
	transmission-remote -t $id --move /data/media/movies
	media_type="movie"
	media_json=`cat << EOF
{
 "Link": "$link",
 "Filename": "$name",
 "Title": $(echo $omdb | jq .Title),
 "Poster": $(echo $omdb | jq .Poster)
}
EOF
`
	echo "transmission-remote -t $id -rad && /opt/melonflix/scripts/torrent-done.py $name" | at now +4 days
	
else
	omdb=`curl -s "http://www.omdbapi.com/?apikey=64e7df7f&t=$title"`
	transmission-remote -t $id --move /data/media/series
	#TODO
fi

sed -i "/^filename = /s/'.*'/'$name'/" /opt/melonflix/scripts/torrent-done.py
transmission-remote -t $id -s

python3 /opt/melonflix/scripts/db-manager.py "$media_type" "$media_json"
