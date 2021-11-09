#!/bin/env python
""" openstack_img_up - Upload an image file to OpenStack.

Author: Alberto Eusebi <albeus@ebi.ac.uk>
"""

import requests
import os
import argparse
import sys
import yaml

config_file = "./config.yaml"

def yes_or_no(question):
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[:1] == 'y':
            return True
            import sys
        if reply[:1] == 'n':
            return False

def get_auth_token(auth_url, app_credential_id, app_credential_secret):
    """ Authenticate using application credential.
        Retrieve an authentication token.
    """
    headers = {'Content-Type': 'application/json'}
    auth_data = {
        "auth": {
            "identity": {
                "methods": [
                    "application_credential" 
                ],
                "application_credential": {
                    "id": app_credential_id,
                    "secret": app_credential_secret
                }
            }
        }
    }
    r = requests.post(auth_url, headers=headers, json=auth_data)
    auth_token = r.headers['X-Subject-Token']
    return auth_token


def main():
    """ Main routine.
    """
    parser = argparse.ArgumentParser(description='Upload an image to OpenStack.')
    parser.add_argument('-n', '--name', required=True, help="Name of the new image.")
    parser.add_argument('-f', '--file', required=True, help="Path of the image file to upload.")
    parser.add_argument('-t', '--disk_type', help="Disk format type (ami, ari, aki, vhd, vhdx, vmdk, raw, qcow2, vdi, ploop or iso). Default:qcow2",
                        default="qcow2")
    args = parser.parse_args()
    image_name = args.name
    file_name = args.file

    # Check credentials in environent variables
    try:
        app_credential_id = os.environ['OS_APPLICATION_CREDENTIAL_ID']
        app_credential_secret = os.environ['OS_APPLICATION_CREDENTIAL_SECRET'] 
    except KeyError:
        print("Environment varioable not found: ", sys.exc_info()[1])
        sys.exit(1)

    # Load config file
    with open(config_file, "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    auth_url = config['auth_url']
    images_url = config['images_url']

    # Print summary and ask for confirmation
    question = "I'm going to upload the file {file} as \"{name}\" using this service: {url}. Continue?".\
               format(file=file_name, name=image_name, url=images_url)
    if not yes_or_no(question):
        sys.exit(0)

    # Authenticate to OpenStack server.
    auth_token = get_auth_token(auth_url, app_credential_id, app_credential_secret)
    headers_auth = {'X-Auth-Token': auth_token}
    headers_base = {'Content-Type': 'application/json'}

    # Create image
    # headers = {**headers_base, **headers_auth} # Not supported in python3.4
    headers = headers_base.copy()
    headers.update(headers_auth)

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

    print("Uploading ", file_name, " to the new image.")
    with open(file_name, 'rb') as image_file_obj:
        r = requests.put(image_upload_url, headers=headers, data=image_file_obj)

if __name__ == "__main__":
    main()
