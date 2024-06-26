#!/bin/bash
docker build --tag=web_spybug .
docker run -p 1337:1337 --rm -it web_spybug
