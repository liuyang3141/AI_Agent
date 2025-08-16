import os
from google.genai import types

def get_directory_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # Handle potential permission errors or broken symlinks gracefully
            if not os.path.islink(fp) and os.path.exists(fp):
                try:
                    total_size += os.path.getsize(fp)
                except OSError:
                    # Ignore files we cannot access
                    continue
    return total_size

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_dir = os.path.abspath(os.path.join(working_directory, directory))

    # Check if the target directory is within the working directory.
    if os.path.commonprefix([abs_target_dir, abs_working_dir]) != abs_working_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # Check if the directory argument is not a directory.
    if not os.path.isdir(abs_target_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        items_info = []

        for item_name in os.listdir(abs_target_dir):
            item_path = os.path.join(abs_target_dir, item_name)
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            items_info.append(f"- {item_name}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(items_info)

    except Exception as e:
        return f"Error listing files: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name = "get_files_info",
    description = "Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "directory": types.Schema(
                type = types.Type.STRING,
                description = "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            )
        }
    )
)
