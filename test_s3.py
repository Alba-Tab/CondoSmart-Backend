import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os
# Configuración
BUCKET_NAME = "condosmart-evidencias"
TEST_FILE = "test_upload.txt"

# Crear archivo local de prueba
with open(TEST_FILE, "w") as f:
    f.write("Hola desde CondoSmart Backend pruebas locales!")

# Crear cliente S3 usando credenciales del .env (o variables de entorno)
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="us-east-2"
)
try:
    # Subir archivo
    s3.upload_file(TEST_FILE, BUCKET_NAME, "pruebas/test_upload.txt")
    print("✅ Archivo subido correctamente a S3.")

    # Generar URL prefirmada para verificar acceso
    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET_NAME, "Key": "pruebas/test_upload.txt"},
        ExpiresIn=60  # válido por 1 minuto
    )
    print("✅ URL prefirmada generada:")
    print(url)

except FileNotFoundError:
    print("❌ Archivo local no encontrado.")
except NoCredentialsError:
    print("❌ Credenciales AWS no encontradas.")
except ClientError as e:
    print(f"❌ Error al interactuar con S3: {e}")
