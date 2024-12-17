ID=1
RESOURCE=localhost:5000/tracks/$ID
curl -v -X DELETE $RESOURCE
sleep 30