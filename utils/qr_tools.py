import streamlit as st
import qrcode
from PIL import Image
import io

def generate_qr_code():
    st.subheader("📦 QR Code Generator")
    data = st.text_input("Enter text or URL to encode:", key="qr_input")

    if st.button("Generate QR Code"):
        if data.strip() == "":
            st.warning("Please enter some data to generate QR code.")
            return

        # Generate QR Code
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill="black", back_color="white").convert("RGB")

        # Convert to BytesIO
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        # Display the image
        st.image(img, caption="Your QR Code", use_column_width=False)

        st.download_button(
            label="Download QR Code",
            data=buf,
            file_name="qr_code.png",
            mime="image/png"
        )
