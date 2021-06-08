FROM php:7.4-fpm

RUN echo 'root:12345' | chpasswd

RUN apt-get update && apt-get install -y \
        libpq-dev \
        zlib1g-dev \
        libmcrypt-dev \
        libzip-dev \
        software-properties-common\
        python3 \
        python3-pip \
        libssl-dev \
        libffi-dev \
        python3-dev \
        build-essential \
        libsndfile1 \
        && docker-php-ext-install pdo pdo_mysql \
        && pip3 install --upgrade pip \
        && pip3 install llvmlite \
        librosa

RUN mkdir -m 777 /tmp/numba_cache
ENV NUMBA_CACHE_DIR=/tmp/numba_cache/

COPY --from=composer:1.10 /usr/bin/composer /usr/bin/composer

RUN usermod -u 1000 www-data && mkdir /var/www/genre
WORKDIR /var/www/genre

ARG XDEBUG_VERSION=2.9.1

RUN pecl install xdebug-${XDEBUG_VERSION} \
        && docker-php-ext-enable xdebug

RUN echo 'xdebug.remote_autostart=1' >> /usr/local/etc/php/php.ini && \
    echo 'xdebug.remote_mode=req' >> /usr/local/etc/php/php.ini && \
    echo 'xdebug.remote_connect_back=1 ' >> /usr/local/etc/php/php.ini && \
    echo 'xdebug.remote_port=9003' >> /usr/local/etc/php/php.ini && \
    echo 'xdebug.remote_enable=1' >> /usr/local/etc/php/php.ini && \
    echo 'post_max_size=32M' >> /usr/local/etc/php/php.ini && \
    echo 'upload_max_filesize=32M' >> /usr/local/etc/php/php.ini

CMD ["php-fpm"]
