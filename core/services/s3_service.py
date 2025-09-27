import boto3
from botocore.exceptions import ClientError
import os

# Cliente S3 configurado con las variables de entorno
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_S3_REGION_NAME", "us-east-2")
)

BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", "condosmart-evidencias")


def upload_file(file_path: str, key: str) -> str:
    """
    Sube un archivo local a S3.
    
    :param file_path: Ruta local al archivo (ej. 'media/foto.jpg')
    :param key: Ruta única en el bucket (ej. 'usuarios/1/foto.jpg')
    :return: La key guardada en S3
    """
    try:
        s3_client.upload_file(file_path, BUCKET_NAME, key)
        return key
    except ClientError as e:
        error_msg = f"Error al subir archivo a S3: {e}"
        print(error_msg)
        return f"ERROR: {error_msg}"


def get_presigned_url(key: str, expires_in: int = 300) -> str:
    """
    Genera una URL temporal (pre-firmada) para acceder a un archivo en S3.
    
    :param key: Ruta del archivo en S3 (ej. 'usuarios/1/foto.jpg')
    :param expires_in: Tiempo en segundos que la URL será válida
    :return: URL prefirmada o None si falla
    """
    try:
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": key},
            ExpiresIn=expires_in
        )
        return url
    except ClientError as e:
        error_msg = f"Error al generar URL prefirmada: {e}"
        print(error_msg)
        return f"ERROR: {error_msg}"
