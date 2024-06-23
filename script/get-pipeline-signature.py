import inspect
from pipeline import *  # Import everything from the other file

# Get all objects in the module that are functions
functions = inspect.getmembers(pipeline, inspect.isfunction)

for name, func in functions:
    print(name)  # Or do something with the function object (func)
