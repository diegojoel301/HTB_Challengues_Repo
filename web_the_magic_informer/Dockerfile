FROM node:18-alpine3.14

# Install packages
RUN apk add --update --no-cache curl supervisor gcc musl-dev curl sqlite

# Setup app
RUN mkdir -p /app

# Copy flag
COPY flag.txt /root/flag

# Add readflag binary
COPY config/readflag.c /
RUN gcc -o /readflag /readflag.c && chmod 4755 /readflag && rm /readflag.c

# Add application
WORKDIR /app
COPY challenge .
RUN chown -R node:node /app

# Set debug password
RUN DEBUG_PASS=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 15 | head -n 1) \
   && echo "DEBUG_PASS=${DEBUG_PASS}" > /app/debug.env

# Install dependencies
RUN yarn

# Setup superivsord
COPY config/supervisord.conf /etc/supervisord.conf

# Expose the port node-js is reachable on
EXPOSE 1337

# Start the node-js application
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
