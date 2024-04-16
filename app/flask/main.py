from flask import Flask, jsonify, request
from pypdf import PdfReader
from base64 import b64decode
import os
import uuid

app = Flask(__name__)

@app.route("/ping")
def show():
    return {
        "data": {
            "attributes": {
                "content": "Este es un mensaje de prueba para configurar el subdominio"
            }
        }
    }


@app.route("/api/v1/link/tools", methods=['POST'])
def store():
    request_json = request.get_json()
    request_data = request_json['data']
    object_file = request_data['file']

    b64 = object_file['b64']
    filename = object_file['name']
    mimetype = object_file['mimetype']

    # Decode the Base64 string, making sure that it contains only valid characters
    _bytes = b64decode(b64, validate=True)

    # Perform a basic validation to make sure that the result is a valid PDF file
    # Be aware! The magic number (file signature) is not 100% reliable solution to validate PDF files
    # Moreover, if you get Base64 from an untrusted source, you must sanitize the PDF contents
    if _bytes[0:4] != b'%PDF':
        raise ValueError('Missing the PDF file signature')

    path_file = str(uuid.uuid1()) + filename + '.pdf'

    # Write the PDF contents to a local file
    f = open(path_file, 'wb')
    f.write(_bytes)
    f.close()

    print(path_file)

    pagination = {}
    reader = PdfReader(path_file)
    number_of_pages = len(reader.pages)

    for page in range(number_of_pages):
        page_object = reader.pages[page]
        page_content = page_object.extract_text()
        index_page = page + 1
        paginate = str(index_page)
        pagination[paginate] = page_content.replace('\n', ' ').strip()

    os.remove(path_file)

    return {
        "data": {
            "attributes": {
                "pages": pagination
            }
        }
    }


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)