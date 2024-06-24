# Copyright 2024 Google.
# This software is provided as-is, without warranty or representation for any use or purpose.
# Your use of it is subject to your agreement with Google.
import datetime
import hashlib
import os
import sys
from kfp.registry import RegistryClient
from sha256sum import sha256sum

# Calcualte the pipeline function signature
# It is important that the signature remains constant
# Any change to the signature will mean major update,
# hence a new release should be created (in a new directory).
def hash_signature(signature):
 # Encode the signature as bytes
 signature_bytes = signature.encode('utf-8')
 # Use SHA-256 hash function to create a hash object
 hash_object = hashlib.sha256(signature_bytes)
 # Get the hexadecimal representation of the hash
 signature_hash = hash_object.hexdigest()
 return signature_hash

# Initialise the envrionment
region = os.environ.get("_REGION", "")
repo_name = os.environ.get("REPO_NAME", "")
project_id = os.environ.get("PROJECT_ID", "")
package = os.environ.get("PACKAGE", "")
signature = os.environ.get("SIGNATURE", "")
host = "https://"+region+"-kfp.pkg.dev/"+project_id+"/"+repo_name

# Create the Vertex Registry client
client = RegistryClient(host=host)

# Initialise the settings for the pipeline source and compiled pipeline
source_name = "pipeline.py"
compiled_name = "pipeline.yaml"

source_sha256 = "source:"+sha256sum(source_name)
signature_sha256 = "signature:"+hash_signature(signature)

versions = client.list_versions(package)
firstVersion = False

if len(versions) > 0:
  # In case we have existing versions of the pipeline make sure the signature has not changed
  try:
    signature_tag = client.get_tag(package, signature_sha256)
  except:
    sys.exit("could not find signature_tag. this means the pipeline signature changed, which would break all existing clients.")
else:
  firstVersion = True

if firstVersion:
  # Upload the first version of the pipeline
  print("uploading the first version of the pipeline: "+package)
  packageName, version = client.upload_pipeline(
    file_name=compiled_name,
    tags=[os.environ.get("BRANCH_NAME").replace("/", "-")+"-"+datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")+"-"+os.environ.get("SHORT_SHA", "latest"),
          "branch:"+os.environ.get("BRANCH_NAME").replace("/", "-"),
          source_sha256,
          signature_sha256],
    extra_headers={"description":"This is an example pipeline template."})
else:
  source_tag = None
  try:
    source_tag = client.get_tag(package, source_sha256)
  except:
    print("a pipeline with this source tag does not exist yet.")
  if not source_tag:
    # Upload the updated version of the pipeline
    print("uploading an updated version of the pipeline: "+package)
    packageName, version = client.upload_pipeline(
      file_name=compiled_name,
      tags=[os.environ.get("BRANCH_NAME").replace("/", "-")+"-"+datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")+"-"+os.environ.get("SHORT_SHA", "latest"),
            source_sha256],
      extra_headers={"description":"This is an example pipeline template."})
    # Move the tags to the new version
    tag = client.update_tag(package, version, "branch:"+os.environ.get("BRANCH_NAME").replace("/", "-"))
    tag = client.update_tag(package, version, signature_sha256)
  else:
    print("just add the branch tag as we already have a version of the pipeline with the same source: "+package)
    version = source_tag["version"].rsplit('/').pop()
    tag = client_create_tag(package, verson, os.environ.get("BRANCH_NAME").replace("/", "-")+"-"+datetime.datetime.now(dddatetime.UTC).strftime("%Y%m%dT%H%M%SZ")+"-"+os.environ.get("SHORT_SHA", "latest"))
    tag = client.create_tag(package, version, "branch:"+os.environ.get("BRANCH_NAME").replace("/", "-"))
