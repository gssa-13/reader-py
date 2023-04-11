FROM python:3.12.0a4-alpine3.17

# Set the working directory to /app Such that inside
# the container our working directory will be app.
WORKDIR /app

# Update, Upgrade and install development dependencies.
# (Add more based on the requirement of the packages you wanted to install)
RUN apk --update --upgrade add --no-cache gcc musl-dev  \
    jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev

# Upgrading pip
RUN python -m pip install --upgrade pip

# Copy requirements.txt
COPY requirements.txt ./

# Install the Python dependencies.
RUN pip install -r requirements.txt

# Copy the current directory . in the project to the workdir . in the image.
COPY . .

EXPOSE 5000
CMD [ "flask", "run","--host","0.0.0.0","--port","5000"]