#!/bin/bash

docker build . -t stockholm:latest

docker run \
	-it \
	-v $(pwd)/calculadora:/tmp/calculadora \
	--name stockholm \
	--rm \
	stockholm