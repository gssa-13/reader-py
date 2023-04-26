FROM alpine:3.17.3

LABEL maintainer = "gssa-13"
LABEL description = "Nginx + uWSGI + Flask based on Alpine Linux and managed by Supervisord"

# Copy python requirements file
COPY /app/conf/requirements.txt /tmp/requirements.txt

RUN apk add --no-cache \
    python3 python3-dev \
    bash \
    nginx \
    uwsgi \
    uwsgi-python3 \
    supervisor && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install -r /tmp/requirements.txt && \
#    rm /etc/nginx/conf.d/default.conf && \
    rm -r /root/.cache && \
    mkdir /app

# Copy the Nginx global conf
COPY /app/nginx/nginx.conf /etc/nginx/
# Copy the Flask Nginx site conf
COPY /app/nginx/flask-site-nginx.conf /etc/nginx/conf.d/
# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY /app/conf/uwsgi.ini /etc/uwsgi/
# Custom Supervisord config
COPY /app/conf/supervisord.conf /etc/supervisord.conf

RUN chown -R nginx.nginx app

# Add flask application into a app directory
COPY ./app/flask /app

WORKDIR /app

CMD ["/usr/bin/supervisord"]