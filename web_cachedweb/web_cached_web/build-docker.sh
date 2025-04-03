#!/bin/bash
docker rm -f web_cached_web
docker build --tag=web_cached_web .
docker run -p 1337:1337 -it --rm --name=web_cached_web web_cached_web