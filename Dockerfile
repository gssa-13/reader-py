FROM python:3.12.2-alpine3.19

# Set the working directory to /app Such that inside
# the container our working directory will be app.
WORKDIR /app

# Update, Upgrade and install development dependencies.
# (Add more based on the requirement of the packages you wanted to install)
RUN apk --update --upgrade add --no-cache gcc musl-dev  \
    jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev

RUN apk add tesseract-ocr=5.3.3-r1

# Upgrading pip
RUN python -m pip install --upgrade pip

# Copy requirements.txt
COPY requirements.txt ./

# Install the Python dependencies.
RUN pip install -r requirements.txt

RUN pip install tesseract

RUN pip install pytesseract

# Copy the current directory . in the project to the workdir . in the image.
COPY . .

COPY spa.traineddata /usr/share/tessdata/spa.traineddata

EXPOSE 5000
CMD [ "flask", "run","--host","0.0.0.0","--port","5000"]