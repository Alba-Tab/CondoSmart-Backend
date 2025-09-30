import boto3
from botocore.exceptions import ClientError
import os
rekognition = boto3.client(
    "rekognition",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="us-east-2"
)

COLLECTION_ID = "condo_faces"

def list_faces_in_collection():
    try:
        # Listar las caras de la colección
        response = rekognition.list_faces(CollectionId=COLLECTION_ID, MaxResults=100)  # Puedes ajustar MaxResults
        
        if 'Faces' in response:
            print(f"Caras en la colección {COLLECTION_ID}:")
            for face in response["Faces"]:
                face_id = face["FaceId"]
                external_id = face.get("ExternalImageId", "No ExternalId")
                print(f"FaceId: {face_id}, ExternalImageId: {external_id}")
        else:
            print(f"No se encontraron caras en la colección {COLLECTION_ID}.")
    
    except ClientError as e:
        print(f"Error al listar las caras: {e}")

def delete_collection():
    try:
        # Eliminar la colección
        response = rekognition.delete_collection(CollectionId=COLLECTION_ID)
        print(f"Colección {COLLECTION_ID} eliminada correctamente.")
    except ClientError as e:
        print(f"Error al eliminar la colección: {e}")

def create_collection():
    try:
        # Crear la colección nuevamente
        response = rekognition.create_collection(CollectionId=COLLECTION_ID)
        print(f"Colección {COLLECTION_ID} creada correctamente.")
    except ClientError as e:
        print(f"Error al crear la colección: {e}")

# Ejecutar para eliminar la colección
delete_collection()

# Ejecutar para crear la colección
create_collection()

# Ejecutar para revisar las caras
list_faces_in_collection()
