import streamlit as st
import os
import io
from PIL import Image
from encryption_logic import encode_text_into_image
from decryption_logic import decode_text_from_image

st.set_page_config(page_title="Image Steganography", page_icon="🔐", layout="wide")

st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        padding: 10px;
    }
    .stTextArea textarea {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("🔐 Image Steganography")
st.sidebar.markdown("**Securely hide and extract text in images.**")

option = st.sidebar.radio("Choose an option:", ["🔒 Hide Text in Image", "🔓 Extract Text from Image", "📁 View Encoded Image Info"])

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🔐 Image Steganography</h1>", unsafe_allow_html=True)

if option == "🔒 Hide Text in Image":
    st.subheader("📤 Hide Secret Text in an Image")
    uploaded_image = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"], help="Upload a clear image.")
    secret_text = st.text_area("Enter your secret text below:", help="This text will be hidden inside the image.")
    
    if st.button("🔏 Hide Text"):
        if uploaded_image and secret_text:
            with st.spinner("Processing... Please wait."):
                image = Image.open(uploaded_image)
                output_path = "encoded_image.png"
                encode_text_into_image(uploaded_image, secret_text, output_path)
                
                with open(output_path, "rb") as file:
                    st.success("✅ Text successfully hidden in image!")
                    st.download_button(label="📥 Download Encoded Image", 
                                       data=file, 
                                       file_name="encoded_image.png", 
                                       mime="image/png")
        else:
            st.error("⚠️ Please upload an image and enter text.")

elif option == "🔓 Extract Text from Image":
    st.subheader("📥 Extract Hidden Text from an Image")
    uploaded_image = st.file_uploader("Upload an Encoded Image", type=["png", "jpg", "jpeg"], help="Upload an image that contains hidden text.")

    if st.button("🔍 Extract Text"):
        if uploaded_image:
            with st.spinner("Extracting text... Please wait."):
                extracted_text = decode_text_from_image(uploaded_image)
                
                if extracted_text:
                    st.success("✅ Text successfully extracted!")
                    st.text_area("🔎 Extracted Text:", extracted_text, height=150)
                else:
                    st.error("⚠️ No hidden text found in the image.")
        else:
            st.error("⚠️ Please upload an encoded image.")

elif option == "📁 View Encoded Image Info":
    st.subheader("📂 View Encoded Image Details")
    uploaded_image = st.file_uploader("Upload an Encoded Image", type=["png", "jpg", "jpeg"], help="Upload an image to view details.")
    
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        st.write("**Image Format:**", image.format)
        st.write("**Image Size:**", image.size)
        st.write("**Image Mode:**", image.mode)
    else:
        st.warning("⚠️ Please upload an image to view details.")

st.sidebar.markdown("---")
st.sidebar.info("Developed with ❤️ using Streamlit")
