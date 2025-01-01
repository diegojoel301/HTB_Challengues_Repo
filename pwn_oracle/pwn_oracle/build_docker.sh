#!/bin/bash
docker build --tag=oracle .
docker run -it -p 1337:1337 --rm --name=oracle oracle
