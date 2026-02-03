from PyPDF2 import PdfMerger
from io import BytesIO

def merge_pdfs(files):
    merger = PdfMerger()
    for file in files:
        merger.append(file)
    output = BytesIO()
    merger.write(output)
    merger.close()
    return output
