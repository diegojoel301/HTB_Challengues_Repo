FROM golang:1.22-alpine3.18

WORKDIR /challenge/

COPY ./challenge/ /challenge/

COPY ./flag.txt /flag.txt

RUN go mod download -x \
 && go install github.com/air-verse/air@latest \
 && go install github.com/a-h/templ/cmd/templ@latest \
 && go get github.com/a-h/templ/runtime \
 && go get github.com/a-h/templ
 && go mod tidy
EXPOSE 1337
EXPOSE 50045

COPY --chown=root entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
