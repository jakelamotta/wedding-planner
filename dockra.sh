#!/bin/bash
VERSION=$1

if [[ "x"$VERSION = "x" ]]
then
    echo "Must specify version"
    exit -1
fi

#docker container stop wedding
#docker container rm wedding
docker rmi wedding
docker build --tag "wedding" .
#docker run -d --name wedding -p 20000:8001 wedding:latest

docker tag wedding:latest banaj-johansson.se:5000/wedding-web:latest
docker tag wedding:latest banaj-johansson.se:5000/wedding-web:$VERSION

docker push banaj-johansson.se:5000/wedding-web:latest
docker push banaj-johansson.se:5000/wedding-web:$VERSION
