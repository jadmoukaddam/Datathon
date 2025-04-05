import os
import zipfile
import json

# Path to your folder containing client0.zip to client9999.zip
zip_dir = "data/train"  # <-- CHANGE THIS TO YOUR FOLDER PATH

# Initialize matrix with 10,000 client entries
clients = [None] * 10000

for i in range(10000):
    zip_filename = f"client_{i}.zip"
    zip_path = zip_dir+"/"+zip_filename
    print(zip_path)
    if not os.path.exists(zip_path):
        print(f"Missing file: {zip_filename}")
        continue

    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            client_data = {}
            for file in z.namelist():
                key = os.path.splitext(os.path.basename(file))[0]
                with z.open(file) as f:
                    client_data[key] = json.load(f)
            clients[i] = client_data
    except Exception as e:
        print(f"Error processing {zip_filename}: {e}")

# Now `clients[0]` to `clients[9999]` each hold a dict of JSONs for that client

import pickle
with open("clients.pkl", "wb") as f:
    pickle.dump(clients, f)


