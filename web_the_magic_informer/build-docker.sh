#!/bin/bash
docker build -t web_magic_informer .
docker run --name=web_magic_informer --rm -p1337:1337 -it web_magic_informer
