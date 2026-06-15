from azure.storage.blob import BlobServiceClient

connect_str = "UseDevelopmentStorage=true"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

# Ensure container exists
try:
    container_client = blob_service_client.create_container("datasets")
    print("Container 'datasets' created.")
except:
    container_client = blob_service_client.get_container_client("datasets")

# Upload file
with open("All_Diets.csv", "rb") as data:
    blob_client = container_client.upload_blob(name="All_Diets.csv", data=data, overwrite=True)

print("All_Diets.csv uploaded successfully.")