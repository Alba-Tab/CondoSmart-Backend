import boto3
import os

rekognition = boto3.client(
    "rekognition",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="us-east-2"
)

def compare_faces(bucket, source_key, target_key, threshold=85):
    """
    Compara dos imágenes en S3 usando Rekognition
    :param bucket: nombre del bucket
    :param source_key: foto de referencia (usuario)
    :param target_key: foto capturada
    :return: True si hay match
    """
    resp = rekognition.compare_faces(
        SourceImage={"S3Object": {"Bucket": bucket, "Name": source_key}},
        TargetImage={"S3Object": {"Bucket": bucket, "Name": target_key}},
        SimilarityThreshold=threshold
    )
    return len(resp["FaceMatches"]) > 0
