# Copyright 2024 Google.
# This software is provided as-is, without warranty or representation for any use or purpose.
# Your use of it is subject to your agreement with Google.
from kfp import dsl
from kfp import compiler

@dsl.component()
def hello_world(text: str) -> str:
    print(text)
    return text

# --> Important: Name the pipeline the same as the directory it is stored in,
#                otherwise your build will fail.
@dsl.pipeline(name='hello-world-v3', description='A simple intro pipeline')
def pipeline_hello_world(text: str = ''):
    """Pipeline that passes small pipeline parameter string to consumer op."""

    text = 'Hi, new world.'
    consume_task = hello_world(
        text=text)  # Passing pipeline parameter as argument to consumer op

compiler.Compiler().compile(
    pipeline_func=pipeline_hello_world,
    # --> Important: Don't change the package_path value to anything else,
    #                otherwise your build will fail.
    package_path='pipeline.yaml')
