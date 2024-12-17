#!/bin/sh
NAME="Everybody+(Backstreet's+Back)+(Radio+Edit)"
ARTIST="Artist"
RESOURCE=localhost:5000/tracks
echo "{ \"name\":\"$NAME\", \"artist\":\"$ARTIST\" }" > input
curl -H "Content-Type: application/json" -v -X PUT -d @input $RESOURCE 
sleep 30