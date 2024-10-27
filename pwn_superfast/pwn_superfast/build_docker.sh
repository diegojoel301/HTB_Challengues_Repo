#!/bin/sh
docker build . -t pwn_superfast && \
docker run -p1337:1337 --cap-add=SYS_PTRACE --security-opt seccomp=unconfined -it pwn_superfast
