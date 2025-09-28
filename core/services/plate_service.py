import boto3
import os
from botocore.exceptions import ClientError
import re

rekognition = boto3.client(
    "rekognition",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_S3_REGION_NAME", "us-east-2")
)

BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", "condosmart-evidencias")
PLATE_REGEX = re.compile(r"^\d{3,4}[A-Z]{3}$")
def detect_plate(key: str):
    """
    Detecta texto en una imagen (placa) usando Amazon Rekognition.
    :param key: key del archivo en S3
    :return: string de placa detectada o None
    """
    try:
        response = rekognition.detect_text(
            Image={"S3Object": {"Bucket": BUCKET_NAME, "Name": key}}
        )

        candidates = []
        for text in response["TextDetections"]:
            if text["Type"] == "WORD":  # palabra detectada
                value = text["DetectedText"].strip().upper()
                # Filtrar algo que parezca una placa: ej. 6-8 caracteres, mezcla letras y números
                if PLATE_REGEX.match(value):
                    candidates.append(value)

        if candidates:
            print("Posibles placas:", candidates)
            return candidates[0]  # tomamos la más probable
        return None

    except ClientError as e:
        print("❌ Error detectando placa:", e)
        return None
