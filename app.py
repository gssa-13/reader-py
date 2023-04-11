from flask import Flask, jsonify
from PyPDF2 import PdfReader

app = Flask(__name__)

@app.route("/")
def read_pdf():
    pagination = {}
    reader = PdfReader("D:\Biblioteca\Documentos\CPA\docs\sisub\s1429.pdf")
    number_of_pages = len(reader.pages)

    for page in range(number_of_pages):
        page_object = reader.pages[page]
        page_content = page_object.extract_text()
        index_page = page + 1
        paginate = "page " + str(index_page)
        pagination[paginate] = page_content

    return {
        "data": {
            "attributes": pagination
        }
    }

if __name__ == "__main__":
    app.run(debug=True)
