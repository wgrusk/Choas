#!/bin/bash

JSONS=`ls ./data/*.json`
TXTS=`ls ./data/*.txt`

# From https://stackoverflow.com/questions/8063228/how-do-i-check-if-a-variable-exists-in-a-list-in-bash
contains () { [[ "$1" =~ (^|[[:space:]])"$2"($|[[:space:]]) ]]; }

for JSON in $JSONS ; do
	FILENAME=`echo "$JSON" | sed "s/.json//g"`
	OUTFILE="$FILENAME_stripped.txt"
	echo "arg 2: $FILENAME-stripped.txt"
	python3 scraper_stripper.py "$JSON" "$FILENAME-stripped.txt"
done
