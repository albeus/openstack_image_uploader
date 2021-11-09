# Openstack images uploader

Simple Python client to upload images on Openstack.

Aims:

* Overcome some python-openstack client issues raised in old operating systems
* Proof of concept of using python to interact with Openstack APIs.

## Status

Proof of concept.

## Features

* Python >= 3.4
* [Application Credentials authentication](https://docs.openstack.org/keystone/rocky/user/application_credentials.html)


## Usage

```
usage: openstack_img_up.py [-h] -n NAME -f FILE [-t DISK_TYPE]

Upload an image to OpenStack.

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Name of the new image.
  -f FILE, --file FILE  Path of the image file to upload.
  -t DISK_TYPE, --disk_type DISK_TYPE
                        Disk format type (ami, ari, aki, vhd, vhdx, vmdk, raw, qcow2, vdi, ploop or iso).
                        Default:qcow2
```

## Quickstart

1. Install requirement:
   ```
   pip install pipenv
   cd openstack_image_uploader
   ```
   Create the virtualenv and enter it:
   ``` 
   pipenv install
   pipenv shell
   ```

1. Check the settings in config file "config.yaml".

1. Export your credentials in environment variables:

   ```
   export OS_APPLICATION_CREDENTIAL_ID="*************"
   export OS_APPLICATION_CREDENTIAL_SECRET="************"
   ```

1. Run the script:
   ```
   $ ./openstack_img_up.py -n my_image -f /tmp/my_image.qcow2
   I'm going to upload the file /tmp/my_image.qcow2 as "my_image" using this service: https://uk1.embassy.ebi.ac.uk:9292/v2/images. Continue? (y/n): 
 
   ```
