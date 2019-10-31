#!/bin/bash

docker build . -t go-web-app # builds up our image and calls it go-web-app
docker run \
       -p 8080:5000 \ # HOSTPORT:CONTPORT
       -v=`pwd`/flask:/flask \ # bind volume ./flask to /flask in the container
       go-web-app 
