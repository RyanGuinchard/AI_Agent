import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
name="get_file_content",
description="Retrieves the content of a specified file relative to the working directory",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type=types.Type.STRING,
            description="Path to the file to retrieve content from, relative to the working directory",
        ),
    },
),
)


def get_file_content(working_directory, file_path):
    try:
        # first validate path to file is in working directory
        absolute_directory = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_directory, file_path))

        valid_target_file = os.path.commonpath([absolute_directory, target_file]) == absolute_directory
        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # read file and return its contents as a string
        with open(target_file, 'r') as f:
            max_chars = 10000
            content = f.read(max_chars)

            if f.read(1):
                content += f'[...File "{file_path}" truncated at {max_chars} characters]'
            return content

    except Exception as e:
        return f"Error: {str(e)}"
        