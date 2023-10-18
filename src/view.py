import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError
import os
from dotenv import load_dotenv
import urllib.request


# Configura las credenciales de AWS
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY'),
aws_session_token = os.getenv('AWS_SESSION_TOKEN')
s3_bucket_name = 'bucket-test-ai'

# Directorio en el bucket de S3 que contiene las imágenes
s3_directory = 'images/'


# Ruta al directorio local que contiene las imágenes
local_directory = 'tmp'


def load_images():

    # Inicializa el cliente de S3
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      aws_session_token=aws_session_token)

    # Crear el directorio local si no existe
    if not os.path.exists(local_directory):
        os.makedirs(local_directory)

    # Obtiene una lista de objetos en el directorio del bucket de S3
    objects = s3.list_objects(Bucket=s3_bucket_name, Prefix=s3_directory)
    object_list = objects.get('Contents', [])

    # Descargar las imágenes en el directorio local
    for object in object_list:
        if object['Key'].endswith(('.jpg', '.jpeg', '.png')):
            image_filename = os.path.basename(object['Key'])
            local_image_path = os.path.join(local_directory, image_filename)
            s3.download_file(s3_bucket_name, object['Key'], local_image_path)


def main():

    # Obtén la lista de archivos de imágenes en el directorio local
    image_files = [f for f in os.listdir(
        local_directory) if f.endswith(('.jpg', '.jpeg', '.png'))]

    # Título de la aplicación
    st.title("Galería de Imágenes")

    # Verificar si hay imágenes en el directorio
    if not image_files:
        st.warning("No se encontraron imágenes en el directorio local.")
    else:
        # Mostrar las imágenes en una galería
        for image_file in image_files:
            image_path = os.path.join(local_directory, image_file)
            st.image(image_path, caption=image_file, use_column_width="auto")


if __name__ == "__main__":
    load_images()
    main()
