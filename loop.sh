#!/bin/bash

while :
do
	fswatch -o ~/Screenshots/Temp | xargs -n1 ~/Screenshots/Script/manage.py
done
