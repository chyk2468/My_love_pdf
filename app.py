import streamlit as st
import ui
import merge
import splitpdf
import compresspdf
import pdf2excel
import pdf2word

def main():
    ui.render_header()
    tool = ui.render_tool_selector()
    
    if tool == "Merge PDF":
        files, clicked = ui.render_merge_ui()
        if clicked and files:
            result = merge.merge_pdfs(files)
            ui.render_download_button(result, "merged.pdf")
            
    elif tool == "Split PDF":
        file, ranges, merge_ranges, clicked = ui.render_split_ui()
        if clicked and file:
            result, filename = splitpdf.split_pdf(file, ranges, merge_ranges)
            ui.render_download_button(result, filename)
            
    elif tool == "Compress PDF":
        files, clicked = ui.render_compress_ui()
        if clicked and files:
            # Result is now (data, filename)
            result_data, filename = compresspdf.compress_pdf(files)
            st.success(f"Compressed {len(files)} file(s) successfully!")
            ui.render_download_button(result_data, filename)

    elif tool == "PDF to Excel":
        file, tables_only, clicked = ui.render_pdf2excel_ui()
        if clicked and file:
            result = pdf2excel.pdf_to_excel(file, tables_only)
            st.success("Converted successfully!")
            ui.render_download_button(result, "converted.xlsx")

    elif tool == "PDF to Word":
        file, use_ocr, clicked = ui.render_pdf2word_ui()
        if clicked and file:
            result = pdf2word.pdf_to_word(file, use_ocr)
            st.success("Converted successfully!")
            ui.render_download_button(result, "converted.docx")

if __name__ == "__main__":
    main()
