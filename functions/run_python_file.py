import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
name="run_python_file",
description="Executes a Python file and returns its output",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type=types.Type.STRING,
            description="Path to the Python file to execute, relative to the working directory",
        ),
        "args": types.Schema(
            type=types.Type.ARRAY,
            items=types.Schema(type=types.Type.STRING),
            description="Optional list of string arguments to pass to the Python file when executing",
        ),
    },

),
)

def run_python_file(working_directory, file_path, args=None):
    try:
         # first validate path to file is in working directory
        absolute_directory = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_directory, file_path))

        valid_target_file = os.path.commonpath([absolute_directory, target_file]) == absolute_directory
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        #Check if file exists
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        #Check if file is a python file
        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        

        command =["python", target_file]
        if args:
            command.extend(args)
        
        result = subprocess.run(command, cwd=absolute_directory, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"
        
        #Check if stdout and stderr contained no output and return a message if so
        if not result.stdout and not result.stderr:
            return f"No output produced"
        
        output = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

        return output


    except Exception as e:
        return f"Error: {str(e)}"