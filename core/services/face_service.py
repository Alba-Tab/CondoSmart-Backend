import boto3
import os
from botocore.exceptions import ClientError

rekognition = boto3.client(
    "rekognition",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="us-east-2"
)

BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", "condosmart-evidencias")
COLLECTION_ID = "condo_faces"

def ensure_collection():
    try:
        rekognition.create_collection(CollectionId=COLLECTION_ID)
        print(f"✅ Colección {COLLECTION_ID} creada.")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceAlreadyExistsException":
            print(f"ℹ️ Colección {COLLECTION_ID} ya existe.")
        else:
            raise

def index_face(photo_key: str, external_id: str):
    """
    Indexa una cara en la colección de Rekognition.
    photo_key → key en S3 (ej. usuarios/5/foto.jpg)
    external_id → identificador único (ej. 'user_5' o 'visita_10')
    """
    try:
        response = rekognition.index_faces(
            CollectionId=COLLECTION_ID,
            Image={"S3Object": {"Bucket": BUCKET_NAME, "Name": photo_key}},
            ExternalImageId=external_id,
            DetectionAttributes=["DEFAULT"]
        )
        return response.get("FaceRecords", [])
    except ClientError as e:
        print(f"❌ Error al indexar cara: {e}")
        return None

def search_face(photo_key: str, threshold=85, max_faces=1):
    """
    Busca una cara en la colección de Rekognition.
    Devuelve external_id si hay match.
    """
    try:
        response = rekognition.search_faces_by_image(
            CollectionId=COLLECTION_ID,
            Image={"S3Object": {"Bucket": BUCKET_NAME, "Name": photo_key}},
            FaceMatchThreshold=threshold,
            MaxFaces=1
        )
        matches = response.get("FaceMatches", [])
        if matches:
            face = matches[0]
            return {
                "similarity": face["Similarity"],
                "face_id": face["Face"]["FaceId"],
                "external_id": face["Face"].get("ExternalImageId")
            }
        return None
    except ClientError as e:
        print(f"❌ Error al buscar cara: {e}")
        return None

def delete_faces_by_external_id(external_id: str):
    """
    Borra todas las caras en Rekognition con un ExternalImageId específico.
    """
    try:
        # Listar caras con ese external_id
        response = rekognition.list_faces(CollectionId=COLLECTION_ID)
        face_ids = [
            f["FaceId"]
            for f in response.get("Faces", [])
            if f.get("ExternalImageId") == external_id
        ]
        if face_ids:
            rekognition.delete_faces(CollectionId=COLLECTION_ID, FaceIds=face_ids)
            print(f"✅ Caras eliminadas para {external_id}")
        return face_ids
    except ClientError as e:
        print(f"❌ Error al borrar caras: {e}")
        return None