FROM python:3.11.3-alpine3.17

RUN mkdir "/srv/flask-app"

COPY . /srv/flask_app

WORKDIR /srv/flask_app

# Update, Upgrade and install development dependencies.
# (Add more based on the requirement of the packages you wanted to install)
RUN apk --update --upgrade add --no-cache gcc musl-dev  \
    jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev

#install
RUN apk add --no-cache nginx=1.22.1-r0 python3-dev uwsgi-python3

# Upgrading pip
RUN python -m pip install --upgrade pip

# Install the Python dependencies.
RUN pip install -r requirements.txt --src /usr/local/src

COPY nginx.conf /etc/nginx

RUN chmod +x ./start.sh

CMD ["./start.sh"]
