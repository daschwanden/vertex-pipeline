# Copyright 2024 Google.
# This software is provided as-is, without warranty or representation for any use or purpose.
# Your use of it is subject to your agreement with Google.
import os
import datetime
from kfp.registry import RegistryClient
from sha256sum import sha256sum

region = os.environ.get("_REGION", "")
repo_name = os.environ.get("REPO_NAME", "")
project_id = os.environ.get("PROJECT_ID", "")
host = "https://"+region+"-kfp.pkg.dev/"+project_id+"/"+repo_name
client = RegistryClient(host=host)

source_name = "hello-world-pipeline.py"
source_sha256 = "source:"+sha256sum(source_name)

tag = client.get_tag(package_name="hello-world", tag=source_sha256)

version = tag["version"].rsplit('/').pop()

tag = client.create_tag(package_name="hello-world", version=version, tag="dev")
tag = client.create_tag(package_name="hello-world", version=version, tag="dev-"+datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ"))
