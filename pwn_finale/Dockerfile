FROM ubuntu:20.04
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update --fix-missing && apt-get -y upgrade
RUN apt-get install -y socat

RUN useradd -m ctf

COPY challenge/* /home/ctf/

RUN chown -R ctf:ctf /home/ctf/

WORKDIR /home/ctf
USER root

EXPOSE 9001/tcp

ENTRYPOINT ["socat", "TCP-LISTEN:9001,fork", "EXEC:'./finale'"]
