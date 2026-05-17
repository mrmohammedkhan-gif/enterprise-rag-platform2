import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("AZURE_BLOB_CONTAINER")

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

os.makedirs("data", exist_ok=True)

for blob in container_client.list_blobs():
    if blob.name.lower().endswith((".txt", ".pdf")):
        local_path = os.path.join("data", os.path.basename(blob.name))

        with open(local_path, "wb") as file:
            blob_data = container_client.download_blob(blob.name)
            file.write(blob_data.readall())

        print(f"Downloaded: {blob.name}")

print("Blob download complete")