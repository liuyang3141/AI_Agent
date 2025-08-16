import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Check if the target directory is within the working directory.
    if os.path.commonprefix([abs_file_path, abs_working_dir]) != abs_working_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # Check if the file_path is not a file.
    if os.path.isdir(abs_file_path) or not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    # Open the file.
    try:
        with open(abs_file_path, 'r') as file:
            content = file.read()
            if len(content) > MAX_CHARS:
                content = content[:MAX_CHARS] + f'''[...File "{abs_file_path}" truncated at 10000 characters]'''

        return content
    except Exception as e:
        return f'Error: {e}'

schema_get_file_content = types.FunctionDeclaration(
    name = "get_file_content",
    description = "Read the content of the file specified, up to the first 10000 characters and constrained to the working directory.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The path to the file where the contents can be read from, relative to the working directory."
            )
        }
    )
)
