import os
from google import genai
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
name="get_files_info",
description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "directory": types.Schema(
            type=types.Type.STRING,
            description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
        ),
    },
),
)


def get_files_info(working_directory, directory="."):

    try:
        # first validate path to directory is in working directory
        absolute_directory = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_directory, directory))

        valid_target_dir = os.path.commonpath([absolute_directory, target_dir]) == absolute_directory
        if not valid_target_dir:
            return f"Error: Cannot list '{directory}' as it is outside the working directory."
        
        if not os.path.isdir(target_dir):
            return f"Error: '{directory}' is not a directory."
        
        # Itterate over the items in the target directory and record name file size and if it is a directory itself
        files_info = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            is_dir = os.path.isdir(item_path)
            if not is_dir:
                file_size = os.path.getsize(item_path)
            else:
                file_size = 0
            files_info.append(f" - {item}: file_size={file_size} bytes, is_dir={is_dir}")
            
        result = "\n".join(files_info)
        return result
    except Exception as e:
        return f"Error: {str(e)}"