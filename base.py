import requests
import os

# Authentication
auth_url = "https://uk1.embassy.ebi.ac.uk:5000/v3/auth/tokens"
headers_base = {'Content-Type': 'application/json'}

auth_data = {
    "auth": {
        "identity": {
            "methods": [
                "application_credential" 
            ],
            "application_credential": {
                "id": os.environ['OS_APPLICATION_CREDENTIAL_ID'],
                "secret": os.environ['OS_APPLICATION_CREDENTIAL_SECRET'] 
            }
        }
    }
}

r = requests.post(auth_url, headers=headers_base, json=auth_data)
auth_token = r.headers['X-Subject-Token']


# Operating images
images_url = "https://uk1.embassy.ebi.ac.uk:9292/v2/images"
headers_auth = {'X-Auth-Token': auth_token}

# List images
#r = requests.get(images_url, headers=headers_auth)
#r.json()['images']

# Create image
# headers = {**headers_base, **headers_auth} # Not supported in python3.4
headers = headers_base.copy()
headers.update(headers_auth)

image_name = "elk-server-data"

print("Creating image: ", image_name)

image_create_data = {
    "container_format": "bare",
    "disk_format": "qcow2",
    "name": image_name
}

r = requests.post(images_url, headers=headers, json=image_create_data)

# Get image id
r = requests.get(images_url, headers=headers_auth)
image_id = next(item for item in r.json()['images'] if item["name"] == image_name)['id']

# Upload image
image_upload_url = "{url}/{id}/file".format(url=images_url, id=image_id)

# headers = headers_auth + headers_type
# headers = {**headers_auth, **headers_type} # Not supported in python3.4
headers_type = {'Content-Type': 'application/octet-stream'}
headers = headers_auth.copy()
headers.update(headers_type)

#file_name = '/homes/albeus/sdo/extcloud05_bioexcel_images_2021-11-01/cirros.qcow2'
#file_name = '/homes/albeus/sdo/pre-backup/2020-03-10/elk-server-data_2020-03-10.raw'
file_name = '/homes/albeus/sdo/pre-backup/2020-03-09/elk-server-data_2020-03-09.raw'
print("Uploading ", file_name, " to the new image.")
with open(file_name, 'rb') as image_file_obj:
    r = requests.put(image_upload_url, headers=headers, data=image_file_obj)
