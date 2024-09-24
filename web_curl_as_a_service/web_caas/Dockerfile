FROM debian:buster-slim

# Setup user
RUN useradd www

# Install system packages
RUN apt-get update && apt-get install -y \
    supervisor \
    nginx \
    lsb-release \
    curl \
    wget \
    gnupg2 \
    php-fpm

# Configure php-fpm and nginx
COPY config/fpm.conf /etc/php/7.3/fpm/php-fpm.conf
COPY config/supervisord.conf /etc/supervisord.conf
COPY config/nginx.conf /etc/nginx/nginx.conf

# Copy challenge files
COPY challenge /www

# Copy flag
COPY flag /

# Setup permissions
RUN chown -R www:www /www /var/lib/nginx

# Expose the port nginx is listening on
EXPOSE 80

# Start supervisord to manage services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
