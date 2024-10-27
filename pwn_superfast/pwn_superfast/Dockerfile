FROM php@sha256:c5aa11a8d2dfe5c895d67bd602118362d017e724b7ec3e5b6e296dd5c92110c4
RUN apt-get update
RUN apt-get install -y procps gdb nano wget
RUN useradd --user-group --no-log-init ctf
COPY challenge/php_logger.so /php_logger.so
COPY challenge /web
RUN mv /web/flag.txt /
WORKDIR /web
EXPOSE 1337
# Para pwndbg: https://github.com/pwndbg/pwndbg/releases/download/2024.08.29/pwndbg_2024.08.29_amd64.deb
RUN wget https://github.com/pwndbg/pwndbg/releases/download/2024.08.29/pwndbg_2024.08.29_amd64.deb
RUN dpkg -i pwndbg_2024.08.29_amd64.deb
USER root
CMD ["/web/start.sh"]

