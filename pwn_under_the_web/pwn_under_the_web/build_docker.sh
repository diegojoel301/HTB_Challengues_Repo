#!/bin/bash
docker rm pwn_under_the_web
docker build . -t pwn_under_the_web
docker run -p 1337:8000 --name pwn_under_the_web -it pwn_under_the_web