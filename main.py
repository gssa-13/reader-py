from PyPDF2 import PdfReader

reader = PdfReader("/home/gssa/Documents/sisubnicsoe/sisub1007.pdf")
number_of_pages = len(reader.pages)

for page in range(number_of_pages):
    page = reader.pages[page]
    page_content = page.extract_text()
    print(page_content)
