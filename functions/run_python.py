import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Check if the abs_file_path is within the working directory.
    if os.path.commonprefix([abs_file_path, abs_working_dir]) != abs_working_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # Check if the file_path exists.
    if not os.path.exists(os.path.dirname(abs_file_path)):
        return f'Error: File "{abs_file_path}" not found.'

    # Check if the file exists.
    if not os.path.isfile(abs_file_path):
        return f'Error: File "{os.path.basename(abs_file_path)}" not found'

    # Check if the file ends with ".py".
    base_name, extension = os.path.splitext(abs_file_path)

    if extension.lower() != ".py":
        return f'Error: "{abs_file_path}" is not a Python file.'

    try:
        if len(args) > 0:
            result = subprocess.run(['python3', abs_file_path] + args, capture_output=True, text=True, check=True, cwd=os.path.dirname(abs_file_path), timeout=30)
        else:
            result = subprocess.run(['python3', abs_file_path], capture_output=True, text=True, check=True, cwd=os.path.dirname(abs_file_path), timeout=30)

        result_string = ""

        if result.stdout:
            result_string += f"STDOUT:\n{result.stdout}"
        if result.stderr:
            result_string += f"\nSTDERR:\n{result.stderr}"

        if not result.stdout and not result.stderr:
            result_string += "No output produced."

        if result.returncode != 0:
            result_string += f"\nProcess exited with code {result.returncode}"

        return result_string

    except subprocess.CalledProcessError as e:
        return f'Error: executing Python file: {e}'
