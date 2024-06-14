import streamlit as st
import fitz  # PyMuPDF
from main import make_output_pdf, make_output_json

TYPE = 1

# 페이지 레이아웃 설정
st.set_page_config(layout="wide")

st.title("PDF CompareX")

uploaded_file1 = st.file_uploader("Choose a PDF file for Column 1", type="pdf")
uploaded_file2 = st.file_uploader("Choose a PDF file for Column 2", type="pdf")
col1, col2 = st.columns(2)
if TYPE==1:
    output1, output2 =  make_output_pdf(uploaded_file1, uploaded_file2)

    if output1 and output2:

        with col1:
            if output1 is not None:
                with fitz.open(output1) as pdf:
                    num_pages = pdf.page_count
                    for page_num in range(num_pages):
                        page = pdf.load_page(page_num)
                        image = page.get_pixmap()
                        st.image(image.tobytes(), caption=f"Page {page_num + 1}", use_column_width=True)

        with col2:
            if output2 is not None:
                with fitz.open(output2) as pdf:
                    num_pages = pdf.page_count
                    for page_num in range(num_pages):
                        page = pdf.load_page(page_num)
                        image = page.get_pixmap()
                        st.image(image.tobytes(), caption=f"Page {page_num + 1}", use_column_width=True)
elif TYPE==2:
    output , unmatched_left, unmatched_right = make_output_json(uploaded_file1, uploaded_file2)
    print("itsworking")
    print(output)
    if output:
        st.json(output)