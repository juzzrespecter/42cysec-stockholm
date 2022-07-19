#!/bin/bash

PORT=30001

if [ "$1" == 'exec' ]; then
	docker exec -it stockholm /bin/bash
	exit 0
fi

if [ "$1" == 'listen' ]; then
	nc -lk $PORT >> .key_log
	exit 0
fi

HOST_FLAG=""
if [[ $(uname) == "Linux" ]]; then
	HOST_FLAG="--add-host=host.docker.internal:host-gateway"
fi

docker build . -t stockholm:latest
docker run \
	-v $(pwd)/calculadora:/tmp/calculadora \
	--name stockholm \
	--rm \
	$HOST_FLAG \
	stockholm &