import os, csv
import pymysql
import boto3

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3307"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "utec")
DB_NAME = os.getenv("DB_NAME", "tienda")
TABLA = os.getenv("TABLA", "clientes")

nombreBucket = "den-output-01"
ficheroUpload = f"{TABLA}.csv"

# 1. Leer todos los registros de la tabla
conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER,
                       password=DB_PASS, database=DB_NAME)
with conn.cursor() as cur:
    cur.execute(f"SELECT * FROM {TABLA}")
    filas = cur.fetchall()
    columnas = [d[0] for d in cur.description]
conn.close()
print(f"{len(filas)} registros leidos de {DB_NAME}.{TABLA}")

# 2. Guardar en CSV
with open(ficheroUpload, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(columnas)
    w.writerows(filas)

# 3. Subir a S3
s3 = boto3.client("s3")
s3.upload_file(ficheroUpload, nombreBucket, ficheroUpload)
print("Ingesta completada")
