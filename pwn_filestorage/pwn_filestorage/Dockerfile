FROM ubuntu@sha256:a06ae92523384c2cd182dcfe7f8b2bf09075062e937d5653d7d0db0375ad2221
EXPOSE 1337
RUN apt update && apt install -y socat python3 && rm -rf /var/lib/apt/lists/*
RUN useradd --user-group --system --no-log-init ctf
USER ctf
WORKDIR /home/ctf
COPY challenge/file_storage challenge/flag.txt ./
ENTRYPOINT ["socat", "tcp-l:1337,reuseaddr,fork", "EXEC:/home/ctf/file_storage"]
