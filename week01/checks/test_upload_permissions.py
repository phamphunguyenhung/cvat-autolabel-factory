import os
import requests
import zipfile
import io

SERVER = "https://cvat.edufun.ai"
TOKEN = os.environ["CVAT_PAT"]  # đọc từ biến môi trường

headers_auth = {
    "Authorization": f"Bearer {TOKEN}"
}

print("=== TEST UPLOAD ANNOTATIONS WITH CORRECT FORMAT NAMES ===")

# Check exact importer format names:
# 'Ultralytics YOLO Segmentation 1.0', 'CVAT 1.1', 'COCO 1.0'
for fmt in ['Ultralytics YOLO Segmentation 1.0', 'CVAT 1.1', 'COCO 1.0']:
    url = f"{SERVER}/api/jobs/987/annotations?format={fmt}"
    
    # We pass a minimal dummy zip or json
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        zf.writestr("test.txt", "dummy")
    zip_buffer.seek(0)
    
    files = {"annotation_file": ("test.zip", zip_buffer, "application/zip")}
    r = requests.post(url, headers=headers_auth, files=files)
    print(f"POST {fmt} -> Status: {r.status_code}")
    print(f"Response: {r.text[:250]}\n")
