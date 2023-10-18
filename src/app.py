import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de la aplicación
st.title("Cargar y Subir Imágenes a Amazon S3")

# Cargar imágenes desde el usuario
uploaded_files = st.file_uploader(
    "Selecciona una o varias imágenes", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.image(uploaded_file, caption="Imagen Cargada",
                 use_column_width=True)

        # Nombre del archivo para S3 (puede personalizarlo)
        file_name = f"images/{uploaded_file.name}"

        # Subir la imagen a S3
        s3 = boto3.client('s3',
                          aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.getenv(
                              'AWS_SECRET_ACCESS_KEY'),
                          aws_session_token=os.getenv('AWS_SESSION_TOKEN'))
        try:
            s3.upload_fileobj(
                uploaded_file, 'bucket-test-ai', file_name)
            st.success("¡Imagen subida a Amazon S3 con éxito!")
        except NoCredentialsError:
            st.error(
                "No se encontraron credenciales de AWS. Asegúrate de configurar tus credenciales.")
