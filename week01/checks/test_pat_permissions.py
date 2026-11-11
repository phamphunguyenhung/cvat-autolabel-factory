import os
import requests
import json

SERVER = "https://cvat.edufun.ai"
TOKEN = os.environ["CVAT_PAT"]  # đọc từ biến môi trường

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

print("=== TEST WRITE/PATCH ANNOTATIONS ON JOB 987 ===")
# 1. Test creating a test polygon shape on frame 60
test_shape = {
    "shapes": [
        {
            "type": "polygon",
            "frame": 60,
            "label_id": 943,  # 'car'
            "points": [1.0, 1.0, 5.0, 1.0, 5.0, 5.0, 1.0, 5.0],
            "occluded": False,
            "attributes": []
        }
    ]
}

url_create = f"{SERVER}/api/jobs/987/annotations?action=create"
r_create = requests.patch(url_create, headers=headers, json=test_shape)
print(f"PATCH (create polygon) -> Status {r_create.status_code}")

if r_create.status_code in [200, 201]:
    res = r_create.json()
    created_shapes = res.get("shapes", [])
    print(f"Successfully created test polygon! Shapes returned: {len(created_shapes)}")
    if created_shapes:
        shape_id = created_shapes[0].get("id")
        print(f"Created shape ID: {shape_id}")
        
        # Now immediately delete the test polygon to keep data clean
        del_payload = {
            "shapes": [
                {"id": shape_id}
            ]
        }
        url_delete = f"{SERVER}/api/jobs/987/annotations?action=delete"
        r_del = requests.patch(url_delete, headers=headers, json=del_payload)
        print(f"PATCH (delete test polygon #{shape_id}) -> Status {r_del.status_code}")
else:
    print("Failed to create polygon:", r_create.text)

# Also test mask (RLE) creation permission
print("\n=== TEST WRITE/PATCH MASK (RLE) ON JOB 987 ===")
# A tiny 2x2 mask at (0, 0, 2, 2)
# CVAT mask format: points = [xtl, ytl, xbr, ybr], rle = [...]
test_mask = {
    "shapes": [
        {
            "type": "mask",
            "frame": 60,
            "label_id": 943,
            "points": [0.0, 0.0, 2.0, 2.0],
            "mask": [1, 1, 1, 1],  # or rle depending on cvat version
            "occluded": False,
            "attributes": []
        }
    ]
}
r_mask = requests.patch(f"{SERVER}/api/jobs/987/annotations?action=create", headers=headers, json=test_mask)
print(f"PATCH (create mask) -> Status {r_mask.status_code}")
if r_mask.status_code in [200, 201]:
    res = r_mask.json()
    created_masks = res.get("shapes", [])
    print(f"Successfully created test mask! Shapes returned: {len(created_masks)}")
    if created_masks:
        m_id = created_masks[0].get("id")
        del_payload = {"shapes": [{"id": m_id}]}
        r_del = requests.patch(f"{SERVER}/api/jobs/987/annotations?action=delete", headers=headers, json=del_payload)
        print(f"PATCH (delete test mask #{m_id}) -> Status {r_del.status_code}")
else:
    print("Response for mask:", r_mask.text[:200])
