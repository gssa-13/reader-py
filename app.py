from flask import Flask, jsonify, request
from PyPDF2 import PdfReader
from base64 import b64decode
from shutil import rmtree
from PIL import Image

import io
import re
import os
import uuid
import pytesseract

app = Flask(__name__)

@app.route("/pdf/reader/images", methods=['POST'])
def pdf_reader_images():
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

    str_uuid = str(uuid.uuid1())
    path_file = str_uuid + "/" + filename + '.pdf'
    output_dir = str_uuid + '/images'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Write the PDF contents to a local file
    f = open(path_file, 'wb')
    f.write(_bytes)
    f.close()

    # This module gets all images from pdf and save into a subdirectory
    with open(path_file, 'rb') as f:
        reader = PdfReader(f)
        for page_num, page in enumerate(reader.pages):
            if '/XObject' in page['/Resources']:
                xObject = page['/Resources'].get('/XObject')
                for obj in xObject:
                    obj_ref = xObject[obj]
                    if obj_ref.get('/Subtype') == '/Image':
                        size = (obj_ref['/Width'], obj_ref['/Height'])
                        data = obj_ref.get_data()
                        mode = ''
                        if obj_ref.get('/ColorSpace') == '/DeviceRGB':
                            mode = 'RGB'
                        else:
                            mode = 'P'

                        if obj_ref.get('/Filter'):
                            if obj_ref['/Filter'] == '/FlateDecode':
                                img = Image.frombytes(mode, size, data)
                            elif obj_ref['/Filter'] == '/DCTDecode':
                                img = io.BytesIO(data)
                                img = Image.open(img)
                                obj_name = re.sub(r'[^a-zA-Z0-9]', '_', obj)  # Replace invalid characters
                                file_path = os.path.join(output_dir, f"extracted_image_{page_num}_{obj_name}.png")
                                img.save(file_path)  # Save the image to the chosen directory
    # This module gets all images from pdf and save into a subdirectory

    directory_content = os.listdir(output_dir)
    images = []
    for file in directory_content:
        os_path = os.path.join(output_dir, file)
        is_file = os.path.isfile(file_path)
        file_ends_with = file.endswith('.png')

        if is_file and file_ends_with:
            img = Image.open(os_path)
            extracted_text = pytesseract.image_to_string(img, lang='spa')
            cleaned_text = extracted_text.replace('\n', ' ')
            cleaned_text = cleaned_text.replace('  ', ' ')
            images.append(extracted_text)

    rmtree(str_uuid)

    return {
        "data": {
            "attributes": {
                "content": images
            }
        }
    }

@app.route("/pdf/reader/readable", methods=['POST'])
def pdf_reader_readable():
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

    pagination = {}
    reader = PdfReader(path_file)
    number_of_pages = len(reader.pages)
    content = ' '

    for page in range(number_of_pages):
        page_object = reader.pages[page]
        page_content = page_object.extract_text()

        content = content + page_content.replace('\n', ' ')

    os.remove(path_file)

    return {
        "data": {
            "attributes": {
                "content": content.strip()
            }
        }
    }
if __name__ == "__main__":
    app.run(debug=True)
