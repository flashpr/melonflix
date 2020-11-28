#!/bin/bash

link=$1
media_type=$2

transmission-remote -a $link -w /data/media/$media_type --torrent-done-script /opt/melonflix/scripts/torrent-done.py -s
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
    
if [[ "$media_type" == "movies" ]]; then
	echo "transmission-remote -t $id -rad && /opt/melonflix/scripts/torrent-done.py $name" | at now +4 days
	
else
	transmission-remote -t $id --move /data/media/series
	#TODO
fi

sed -i "/^filename = /s/'.*'/'$name'/" /opt/melonflix/scripts/torrent-done.py
