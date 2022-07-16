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

docker build . -t stockholm:latest
docker run \
	-v $(pwd)/calculadora:/tmp/calculadora \
	--name stockholm \
	--rm \
	stockholm &