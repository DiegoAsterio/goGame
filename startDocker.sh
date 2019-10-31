#!/bin/bash

docker build . -t go-web-app # builds up our image and calls it go-web-app
# -p := HOSTPORT:CONTPORT
# -v := bind volume ./flask to /flask in the container
docker run -p 8080:5000 -v=`pwd `/flask:/flask go-web-app 
