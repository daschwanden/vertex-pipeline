# Copyright 2024 Google.
# This software is provided as-is, without warranty or representation for any use or purpose.
# Your use of it is subject to your agreement with Google.
from kfp import dsl
from kfp import compiler

@dsl.component()
def hello_world(text: str) -> str:
    print(text)
    return text

@dsl.pipeline(name='hello-world-v1', description='A simple intro pipeline')
def pipeline_hello_world(text: str = ''):
    """Pipeline that passes small pipeline parameter string to consumer op."""

    text = 'Hi brave new world123'
    consume_task = hello_world(
        text=text)  # Passing pipeline parameter as argument to consumer op

compiler.Compiler().compile(
    pipeline_func=pipeline_hello_world,
    package_path='pipeline.yaml')
