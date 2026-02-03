import streamlit as st
import fitz  # PyMuPDF

def apply_custom_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&display=swap');

        /* DARK LIVE BACKGROUND */
        .stApp {
            background: linear-gradient(-45deg, #020024, #090979, #00d4ff, #000000);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            font-family: 'Outfit', sans-serif;
            color: #ffffff;
        }
        
        /* Simpler Dark Gradient Option if the above is too blue: */
        /* background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e); */
         .stApp {
            background: linear-gradient(-45deg, #000000, #130f40, #000000, #130f40);
            background-size: 400% 400%;
            animation: gradient 20s ease infinite;
        }

        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* DARK GLASSMORPHISM */
        div[data-testid="stHeader"] {
            background-color: rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
        }

        /* CARD / UPLOADER STYLING */
        .stFileUploader {
            background-color: rgba(255, 255, 255, 0.05);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease;
        }
        
        .stFileUploader:hover {
            transform: translateY(-5px);
            border-color: rgba(255, 255, 255, 0.3);
        }
        
        .stFileUploader > div > div {
             color: white; /* Text inside uploader */
        }

        /* IMAGE HOVER EFFECTS */
        img {
            border-radius: 10px;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            box-shadow: 0 5px 15px rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        img:hover {
            transform: scale(1.08) rotate(1deg);
            box-shadow: 0 15px 30px rgba(0,0,0,0.8);
            z-index: 10;
            border-color: #00d4ff;
        }

        /* BUTTONS */
        div.stButton > button {
            background: linear-gradient(90deg, #d53369 0%, #daae51 100%);
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 50px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }

        div.stButton > button:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 10px 25px rgba(213, 51, 105, 0.6);
             background: linear-gradient(90deg, #daae51 0%, #d53369 100%);
        }

        /* RADIO BUTTONS (Tool Selector) */
        div[role="radiogroup"] {
            background-color: rgba(0, 0, 0, 0.3);
            padding: 10px;
            border-radius: 15px;
            display: flex;
            justify-content: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        div[role="radiogroup"] label {
            color: white !important;
        }

        /* TEXT STYLING */
        h1, h2, h3, p, label, .stMarkdown, .stText {
            color: #e0e0e0 !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.8);
        }
        
        div[data-testid="stCaptionContainer"] {
            color: #cccccc !important;
            font-weight: 400;
        }

        /* INPUT FIELDS */
        .stNumberInput input {
            background-color: rgba(0, 0, 0, 0.5);
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.1);
            text-align: center;
            font-weight: bold;
            color: white;
        }
        
        /* DIVIDERS */
        hr {
            border-color: rgba(255,255,255,0.2);
        }
        </style>
    """, unsafe_allow_html=True)

def render_header():
    st.set_page_config(page_title="My Love PDF", page_icon="❤️", layout="centered")
    apply_custom_styles()
    st.title("My Love PDF")

def render_tool_selector():
    return st.radio("Select Tool", ["Merge PDF", "Split PDF", "Compress PDF", "PDF to Excel", "PDF to Word"], horizontal=True)

def render_merge_ui():
    st.header("Merge PDF files")
    files = st.file_uploader("Select PDF files", type="pdf", accept_multiple_files=True)
    clicked = st.button("Merge PDFs", type="primary")
    return files, clicked

def render_compress_ui():
    st.header("Compress PDF files")
    
    st.info("Compressing with Maximum Optimization (Lossless)")
        
    files = st.file_uploader("Select PDF file(s)", type="pdf", accept_multiple_files=True, key="compress_uploader")
    clicked = st.button("Compress PDF", type="primary")
    
    return files, clicked

def render_split_ui():
    st.header("Split PDF file")
    file = st.file_uploader("Select PDF file", type="pdf", accept_multiple_files=False)
    
    if "ranges" not in st.session_state:
        st.session_state.ranges = [{"from": 1, "to": 1}]
    
    ranges = []
    
    if file:
        # --- Preview Section ---
        st.subheader("File Preview")
        try:
            # Open PDF from stream
            doc = fitz.open(stream=file.read(), filetype="pdf")
            total_pages = len(doc)
            
            # Display pages in a grid
            cols = st.columns(4)
            for page_num in range(total_pages):
                page = doc[page_num]
                pix = page.get_pixmap(matrix=fitz.Matrix(0.2, 0.2)) # Thumbnail size
                img_data = pix.tobytes("png")
                
                with cols[page_num % 4]:
                    st.image(img_data, use_container_width=True)
                    st.caption(f"Page {page_num + 1}")
            
            doc.close()
        except Exception as e:
            st.error(f"Error previewing file: {e}")
        finally:
            # IMPORTANT: Reset file pointer for later use
            file.seek(0)
        
        st.divider()
        # --- End Preview Section ---

        st.subheader("Define Ranges")
        for i, range_item in enumerate(st.session_state.ranges):
            c1, c2 = st.columns(2)
            with c1:
                f = st.number_input(f"Range {i+1} From", min_value=1, max_value=total_pages if 'total_pages' in locals() else None, value=range_item["from"], key=f"from_{i}")
            with c2:
                t = st.number_input(f"Range {i+1} To", min_value=1, max_value=total_pages if 'total_pages' in locals() else None, value=range_item["to"], key=f"to_{i}")
            ranges.append((f, t))
            st.session_state.ranges[i]["from"] = f
            st.session_state.ranges[i]["to"] = t

        if st.button("Add Range"):
            st.session_state.ranges.append({"from": 1, "to": 1})
            st.rerun()
            
        merge_ranges = st.checkbox("Merge all ranges into one PDF")
        clicked = st.button("Split PDF", type="primary")
        return file, ranges, merge_ranges, clicked
    
    return None, [], False, False

def render_pdf2excel_ui():
    st.header("Convert PDF to Excel")
    file = st.file_uploader("Select PDF file", type="pdf", accept_multiple_files=False)
    
    tables_only = st.checkbox("Extract tables only")
    clicked = st.button("Convert to Excel", type="primary")
    
    return file, tables_only, clicked

def render_pdf2word_ui():
    st.header("Convert PDF to Word")
    file = st.file_uploader("Select PDF file", type="pdf", accept_multiple_files=False)
    
    use_ocr = st.checkbox("Enable OCR (for scanned PDFs)")
    clicked = st.button("Convert to Word", type="primary")
    
    return file, use_ocr, clicked

def render_download_button(data, filename):
    st.download_button(
        label=f"Download {filename}",
        data=data,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document" if filename.endswith(".docx") else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if filename.endswith(".xlsx") else "application/pdf" if filename.endswith(".pdf") else "application/zip"
    )
