# Copyright 2024 Google.
# This software is provided as-is, without warranty or representation for any use or purpose.
# Your use of it is subject to your agreement with Google.
import os
import datetime
from kfp.registry import RegistryClient
from sha256sum import sha256sum
import hashlib

def hash_signature(signature):
 # Encode the signature as bytes
 signatured_bytes = signature.encode('utf-8')
 # Use SHA-256 hash function to create a hash object
 hash_object = hashlib.sha256(signature_bytes)
 # Get the hexadecimal representation of the hash
 signature_hash = hash_object.hexdigest()
 return signature_hash

region = os.environ.get("_REGION", "")
repo_name = os.environ.get("REPO_NAME", "")
project_id = os.environ.get("PROJECT_ID", "")
package = os.environ.get("PACKAGE", "")
signature = os.environ.get("SIGNATURE", "")
signature_hash = hash_signature(signature)
host = "https://"+region+"-kfp.pkg.dev/"+project_id+"/"+repo_name
client = RegistryClient(host=host)

source_name = "pipeline.py"
compiled_name = package+".yaml"
sha256 = sha256sum(source_name)

templateName, versionName = client.upload_pipeline(
  file_name=compiled_name,
  tags=[os.environ.get("BRANCH_NAME").replace("/", "-")+"-"+datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")+"-"+os.environ.get("SHORT_SHA", "latest"), "source:"+sha256, "signature:"+signature_hash],
  extra_headers={"description":"This is an example pipeline template."})

