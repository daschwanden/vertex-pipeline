# Copyright 2024 Google.
# This software is provided as-is, without warranty or representation for any use or purpose.
# Your use of it is subject to your agreement with Google.
import os
#import datetime
from kfp.registry import RegistryClient

region = os.environ.get("_REGION", "")
repo_name = os.environ.get("REPO_NAME", "")
project_id = os.environ.get("PROJECT_ID", "")
host = "https://"+region+"-kfp.pkg.dev/"+project_id+"/"+repo_name
client = RegistryClient(host=host)

templateName, versionName = client.upload_pipeline(
  file_name="hello_world_pipeline.yaml",
  tags=[os.environ.get("SHORT_SHA", "latest"), os.environ.get("BRANCH_NAME", "")],
  #tags=[os.environ.get("SHORT_SHA", "latest"), os.environ.get("BRANCH_NAME", ""), "feat:"+datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")],
  extra_headers={"description":"This is an example pipeline template."})

