import streamlit as st
import os
import PyPDF2
import io

def pdf_toolkit():
    st.subheader("📄 PDF Toolkit")

    option = st.selectbox("Choose an operation:", [
        "📎 Merge PDFs", "✂️ Split PDF", "🔄 Rotate PDF", "💧 Watermark PDF", "🔐 Protect PDF"
    ])

    if option == "📎 Merge PDFs":
        files = st.file_uploader("Upload PDF files to merge", type="pdf", accept_multiple_files=True)
        if st.button("Merge PDFs") and files:
            merger = PyPDF2.PdfMerger()
            for f in files:
                merger.append(f)
            out = io.BytesIO()
            merger.write(out)
            merger.close()
            st.download_button("📥 Download Merged PDF", out.getvalue(), "merged.pdf", mime="application/pdf")

    elif option == "✂️ Split PDF":
        file = st.file_uploader("Upload PDF to split", type="pdf", key="split_pdf")
        start = st.number_input("Start Page (0-based)", min_value=0)
        end = st.number_input("End Page (exclusive)", min_value=1)
        if st.button("Split PDF") and file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()
            for i in range(int(start), int(end)):
                writer.add_page(reader.pages[i])
            out = io.BytesIO()
            writer.write(out)
            st.download_button("📥 Download Split PDF", out.getvalue(), "split.pdf", mime="application/pdf")

    elif option == "🔄 Rotate PDF":
        file = st.file_uploader("Upload PDF to rotate", type="pdf", key="rotate_pdf")
        angle = st.selectbox("Rotation Angle", [90, 180, 270])
        if st.button("Rotate PDF") and file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()
            for page in reader.pages:
                page.rotate_clockwise(angle)
                writer.add_page(page)
            out = io.BytesIO()
            writer.write(out)
            st.download_button("📥 Download Rotated PDF", out.getvalue(), "rotated.pdf", mime="application/pdf")

    elif option == "💧 Watermark PDF":
        base = st.file_uploader("Upload Base PDF", type="pdf", key="wm_base")
        watermark = st.file_uploader("Upload Watermark PDF (one page)", type="pdf", key="wm_pdf")
        if st.button("Apply Watermark") and base and watermark:
            base_reader = PyPDF2.PdfReader(base)
            wm_reader = PyPDF2.PdfReader(watermark)
            wm_page = wm_reader.pages[0]

            writer = PyPDF2.PdfWriter()
            for page in base_reader.pages:
                page.merge_page(wm_page)
                writer.add_page(page)

            out = io.BytesIO()
            writer.write(out)
            st.download_button("📥 Download Watermarked PDF", out.getvalue(), "watermarked.pdf", mime="application/pdf")

    elif option == "🔐 Protect PDF":
        file = st.file_uploader("Upload PDF to protect", type="pdf", key="protect_pdf")
        password = st.text_input("Enter password to encrypt")
        if st.button("Encrypt PDF") and file and password:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            writer.encrypt(password)
            out = io.BytesIO()
            writer.write(out)
            st.download_button("📥 Download Encrypted PDF", out.getvalue(), "protected.pdf", mime="application/pdf")
