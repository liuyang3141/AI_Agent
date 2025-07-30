import os

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

    items_info = [f"Result for {'current directory' if directory == '.' else f"'{directory}' directory:"}"]
    for item_name in os.listdir(abs_target_dir):
        item_path = os.path.join(abs_target_dir, item_name)
        if os.path.isfile(item_path):
            try:
                size = os.path.getsize(item_path)
                items_info.append(f"\t- {item_name}: file_size={size} bytes, is_dir={os.path.isdir(item_path)}")
            except FileNotFoundError:
                items_info.append("\tError: The file was not found.")
            except PermissionError:
                items_info.append("\tError: You don't have permission to access this file.")
            except OSError as e:
                # This will catch any other OSError that isn't specifically handled above
                items_info.append(f"\tError: {e}")
        elif os.path.isdir(item_path):
            try:
                size = get_directory_size(item_path)
                items_info.append(f"\t- {item_name}: file_size={size} bytes, is_dir={os.path.isdir(item_path)}")
            except FileNotFoundError:
                items_info.append("\tError: The file was not found.")
            except PermissionError:
                items_info.append("\tError: You don't have permission to access this file.")
            except OSError as e:
                # This will catch any other OSError that isn't specifically handled above
                items_info.append(f"\tError: {e}")
    return "\n".join(items_info)
