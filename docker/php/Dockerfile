FROM php:7.4-fpm

RUN apt-get update && apt-get install -y \
        libpq-dev \
        wget \
        zlib1g-dev \
        libmcrypt-dev \
        libzip-dev \
        && docker-php-ext-install pdo pdo_mysql

COPY --from=composer:1.10 /usr/bin/composer /usr/bin/composer

RUN usermod -u 1000 www-data && mkdir /var/www/genre
WORKDIR /var/www/genre

CMD ["php-fpm"]
