#!/bin/sh
RESOURCE=localhost:5000/tracks
curl -v -X GET $RESOURCE
sleep 30