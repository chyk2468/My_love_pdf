import fitz
from io import BytesIO
import zipfile

import fitz
from io import BytesIO
import zipfile

def compress_single_file(file_stream):
    # Maximum Optimization settings for PyMuPDF
    # garbage=4: Eliminate duplicate objects, unused streams, etc.
    # deflate=True: Compress all streams
    # clean=True: Standardize syntax
    doc = fitz.open(stream=file_stream.read(), filetype="pdf")
    output = BytesIO()
    
    doc.save(output, garbage=4, deflate=True, clean=True)
    
    doc.close()
    file_stream.seek(0) # Reset pointer
    return output.getvalue()

def compress_pdf(files):
    # If single file
    if len(files) == 1:
        compressed_data = compress_single_file(files[0])
        return BytesIO(compressed_data), "compressed.pdf"
    
    # If multiple files -> ZIP
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file in files:
            compressed_data = compress_single_file(file)
            zip_file.writestr(file.name, compressed_data)
            
    return zip_buffer, "compressed_files.zip"
