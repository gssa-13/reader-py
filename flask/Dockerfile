FROM python:3.12.0a4-alpine3.17

LABEL authors="gssa-13"

# Set the working directory to /app Such that inside
# the container our working directory will be app.
RUN mkdir /app

WORKDIR /app

# Add requirements.txt and main.py to /app in container
ADD requirements.txt /app

ADD main.py /app

# Update, Upgrade and install development dependencies.
# (Add more based on the requirement of the packages you wanted to install)
RUN apk --update --upgrade add --no-cache gcc musl-dev  \
    jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev

# Upgrading pip
RUN python -m pip install --upgrade pip

# Install the Python dependencies.
RUN pip install -r requirements.txt

CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:8000", "main:app"]