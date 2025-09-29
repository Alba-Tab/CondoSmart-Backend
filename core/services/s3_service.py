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
    Sube un archivo desde el disco local a S3.
    Útil para pruebas o migraciones.
    """
    try:
        s3_client.upload_file(file_path, BUCKET_NAME, key)
        return key
    except ClientError as e:
        print(f"Error al subir archivo a S3: {e}")
        return None #type: ignore


def upload_fileobj(file_obj, key: str) -> str:
    """
    Sube un archivo recibido en memoria
    """
    try:
        s3_client.upload_fileobj(file_obj, BUCKET_NAME, key)
        return key
    except ClientError as e:
        print(f"Error al subir archivo a S3: {e}")
        return None #type: ignore


def get_presigned_url(key: str, expires_in: int = 300) -> str:
    """
    Genera una URL temporal para acceder a un archivo en S3
    """
    try:
        return s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": key},
            ExpiresIn=expires_in
        )
    except ClientError as e:
        print(f"Error al generar URL prefirmada: {e}")
        return None #type: ignore
