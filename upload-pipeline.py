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
pipe_name = "hello_world_pipeline.yaml"
sha256 = sha256sum(source_name)

templateName, versionName = client.upload_pipeline(
  file_name=pipe_name,
  tags=["feat-"+datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")+"-"+os.environ.get("SHORT_SHA", "latest")+"-"+datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ"), "source:"+sha256],
  extra_headers={"description":"This is an example pipeline template."})

