from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import zipfile

def split_pdf(file, ranges, merge_ranges):
    reader = PdfReader(file)
    total_pages = len(reader.pages)
    
    if merge_ranges:
        writer = PdfWriter()
        for start, end in ranges:
            start_idx = max(0, start - 1)
            end_idx = min(total_pages, end)
            for i in range(start_idx, end_idx):
                writer.add_page(reader.pages[i])
        output = BytesIO()
        writer.write(output)
        return output, "merged_ranges.pdf"
    else:
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for idx, (start, end) in enumerate(ranges):
                writer = PdfWriter()
                start_idx = max(0, start - 1)
                end_idx = min(total_pages, end)
                for i in range(start_idx, end_idx):
                    writer.add_page(reader.pages[i])
                
                pdf_buffer = BytesIO()
                writer.write(pdf_buffer)
                zip_file.writestr(f"range_{idx + 1}.pdf", pdf_buffer.getvalue())
        
        return zip_buffer, "split_ranges.zip"
