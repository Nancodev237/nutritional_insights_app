from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import json
import os

# Ensure local directory exists
os.makedirs('simulated_nosql', exist_ok=True)

# Connection to Azurite
connect_str = "UseDevelopmentStorage=true"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

container_name = 'datasets'
blob_name = 'All_Diets.csv'

container_client = blob_service_client.get_container_client(container_name)
blob_client = container_client.get_blob_client(blob_name)

print("Downloading data from Azurite...")
stream = blob_client.download_blob().readall()
df = pd.read_csv(io.BytesIO(stream))

print("Calculating nutritional averages...")
avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()

# Save as JSON
result = avg_macros.reset_index().to_dict(orient='records')
with open('simulated_nosql/results.json', 'w') as f:
    json.dump(result, f, indent=4)

print("Data processed and stored successfully in simulated_nosql/results.json.")