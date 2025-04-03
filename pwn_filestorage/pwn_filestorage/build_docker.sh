#!/usr/bin/env bash

docker build . -t pwn_filestorage && \
    docker run -it -p1337:1337 --rm --name pwn_filestorage pwn_filestorage
