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
#headers = {**headers_base, **headers_auth}
#
#image_create_data = {
#    "container_format": "bare",
#    "disk_format": "qcow2",
#    "name": "test"
#}
#
#r = requests.post(images_url, headers=headers, json=image_create_data)
