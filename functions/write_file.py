import os

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Check if the abs_file_path is within the working directory.
    if os.path.commonprefix([abs_file_path, abs_working_dir]) != abs_working_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # Check if the file_path exists. If it doesn't, create it.
    if not os.path.exists(os.path.dirname(abs_file_path)):
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)

    else:
        try:
            with open(abs_file_path, 'w') as file:
                file.write(content)
            return f'Successfully wrote to "{abs_file_path}" {len(content)} characters written'
        except Exception as e:
            return "Error: {e}"
