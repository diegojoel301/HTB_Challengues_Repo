FROM php:8.1-fpm

# Install system packages
RUN apt update && apt install -y mariadb-server mariadb-client \
    supervisor nginx

RUN docker-php-ext-install mysqli pdo pdo_mysql && docker-php-ext-enable pdo_mysql

# Install imagick
RUN apt-get update && apt-get install -y \
    libmagickwand-dev libmagickcore-dev

RUN pecl install imagick-3.7.0 && docker-php-ext-enable imagick

COPY flag.txt /root/flag.txt

# Configure php-fpm and nginx
COPY config/fpm.conf /usr/local/etc/php-fpm.d/www.conf
COPY config/supervisord.conf /etc/supervisord.conf
COPY config/nginx.conf /etc/nginx/nginx.conf
COPY config/php.ini /usr/local/etc/php/php.ini

# Copy challenge files
COPY magicom /www

# Setup permissions
RUN chown -R www-data:www-data /www/uploads

# Expose the port nginx is listening on
EXPOSE 1337

# Populate database and start supervisord
# CMD while true; do sleep 10; done
COPY --chown=root entrypoint.sh /entrypoint.sh

# Setup readflag
COPY config/readflag.c /
RUN gcc -o /readflag /readflag.c && chmod 4755 /readflag && rm /readflag.c

ENTRYPOINT ["/entrypoint.sh"]