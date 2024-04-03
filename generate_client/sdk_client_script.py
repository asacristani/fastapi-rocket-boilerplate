import json
from pathlib import Path

import requests

url = "http://localhost:8000/openapi.json"
script_dir = Path(__file__).parent.absolute()
destination_file = script_dir / "openapi.json"
print("HOLA")
print(destination_file)
response = requests.get(url)

if response.status_code == 200:
    with open(destination_file, "wb") as file:
        file.write(response.content)
else:
    raise Exception(
        f"Error downloading the file. Response code: {response.status_code}"
    )

file_path = Path(destination_file)
openapi_content = json.loads(file_path.read_text())

for path_data in openapi_content["paths"].values():
    for operation in path_data.values():
        tag = operation["tags"][0]
        operation_id = operation["operationId"]
        to_remove = f"{tag}-"
        new_operation_id = operation_id[len(to_remove) :]
        operation["operationId"] = new_operation_id

file_path.write_text(json.dumps(openapi_content))
