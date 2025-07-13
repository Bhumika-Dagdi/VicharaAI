import streamlit as st
import os
from PIL import Image
import shutil
import pandas as pd
import json
import base64
from io import BytesIO
from docx import Document
from datetime import datetime, timedelta

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ADMIN_PASSWORD = "admin123"

def save_uploaded_file(uploaded_file):
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def get_file_size(path):
    return round(os.path.getsize(path) / 1024, 2)

def file_download_link(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{os.path.basename(file_path)}">📥 Download</a>'

def clean_old_files(days=7):
    cutoff = datetime.now() - timedelta(days=days)
    for root, _, files in os.walk(UPLOAD_DIR):
        for file in files:
            path = os.path.join(root, file)
            if datetime.fromtimestamp(os.path.getmtime(path)) < cutoff:
                os.remove(path)

def file_manager():
    st.markdown("""
        <style>
        .file-card {
            background-color: #f7f7f9;
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }
        .highlight {
            color: #764ba2;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("📁 Advanced File Manager")

    # Admin Login
    if "is_admin" not in st.session_state:
        st.session_state["is_admin"] = False

    if not st.session_state["is_admin"]:
        with st.expander("🔐 Admin Login", expanded=True):
            password = st.text_input("Enter Admin Password", type="password")
            if st.button("Login"):
                if password == ADMIN_PASSWORD:
                    st.session_state["is_admin"] = True
                    st.success("✅ Login Successful")
                    st.rerun()
                else:
                    st.error("❌ Incorrect Password")
        return

    # Upload + Create Folder
    col1, col2 = st.columns([3, 2])
    with col1:
        uploaded = st.file_uploader("📤 Upload File", type=None)
        if uploaded:
            saved_path = save_uploaded_file(uploaded)
            st.success(f"Uploaded to `{saved_path}`")

    with col2:
        with st.form("create_folder_form"):
            folder = st.text_input("📁 New Folder Name")
            path = st.text_input("📂 Path (relative to uploaded_files)", value="")
            submitted = st.form_submit_button("➕ Create Folder")
            if submitted:
                full_path = os.path.join(UPLOAD_DIR, path, folder)
                os.makedirs(full_path, exist_ok=True)
                st.success(f"Created folder `{folder}` at `{path or '/'} `")

    st.divider()

    # File Filter/Search Options
    with st.expander("🔎 Filter & Search"):
        file_types = ["All", "Images", "Text", "PDF", "DOCX", "JSON", "CSV"]
        selected_type = st.selectbox("Filter by Type", file_types)
        sort_by = st.selectbox("Sort by", ["Name", "Size"])
        search_term = st.text_input("Search by name")

    # Collect Files
    all_files = []
    for root, _, files in os.walk(UPLOAD_DIR):
        for file in files:
            full_path = os.path.join(root, file)
            all_files.append((file, full_path, get_file_size(full_path)))

    def filter_type(file):
        name = file[0].lower()
        return (
            selected_type == "All" or
            (selected_type == "Images" and name.endswith((".png", ".jpg", ".jpeg"))) or
            (selected_type == "Text" and name.endswith(".txt")) or
            (selected_type == "PDF" and name.endswith(".pdf")) or
            (selected_type == "DOCX" and name.endswith(".docx")) or
            (selected_type == "CSV" and name.endswith(".csv")) or
            (selected_type == "JSON" and name.endswith(".json"))
        )

    filtered = [f for f in all_files if filter_type(f) and search_term.lower() in f[0].lower()]
    filtered = sorted(filtered, key=lambda x: x[0 if sort_by == "Name" else 2])

    # File Cards
    for file, path, size in filtered:
        with st.container():
            st.markdown('<div class="file-card">', unsafe_allow_html=True)
            st.markdown(f"📄 <span class='highlight'>{file}</span> — {size} KB", unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            with col1:
                rename = st.text_input("Rename", key=f"rename_{file}")
                if st.button("✏️ Rename", key=f"rename_btn_{file}"):
                    os.rename(path, os.path.join(os.path.dirname(path), rename))
                    st.rerun()

            with col2:
                if st.button("🗑️ Delete", key=f"delete_{file}"):
                    os.remove(path)
                    st.rerun()

            with col3:
                st.markdown(file_download_link(path), unsafe_allow_html=True)

            # Preview
            ext = file.lower().split(".")[-1]
            if ext in ["png", "jpg", "jpeg"]:
                st.image(path, width=200)
            elif ext == "txt":
                st.text_area("Preview", open(path).read(), height=100)
            elif ext == "csv":
                df = pd.read_csv(path)
                st.dataframe(df.head())
            elif ext == "json":
                st.json(json.load(open(path)))
            elif ext == "docx":
                doc = Document(path)
                st.text_area("Preview", "\n".join([p.text for p in doc.paragraphs]), height=150)

            # Move/Copy
            folders = [f for f in os.listdir(UPLOAD_DIR) if os.path.isdir(os.path.join(UPLOAD_DIR, f))]
            if folders:
                dest = st.selectbox("Target Folder", folders, key=f"dest_{file}")
                mcol1, mcol2 = st.columns(2)
                with mcol1:
                    if st.button("📂 Move", key=f"move_{file}"):
                        shutil.move(path, os.path.join(UPLOAD_DIR, dest, file))
                        st.success("Moved!")
                        st.rerun()
                with mcol2:
                    if st.button("📄 Copy", key=f"copy_{file}"):
                        shutil.copy(path, os.path.join(UPLOAD_DIR, dest, file))
                        st.success("Copied!")

            st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # Cleanup Option
    with st.expander("🧹 Clean Up Old Files"):
        days = st.slider("Delete files older than (days)", 1, 30, 7)
        if st.button("🧽 Clean"):
            clean_old_files(days)
            st.success(f"Files older than {days} days removed.")
