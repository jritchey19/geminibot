import os

def get_files_info(working_directory, directory="."):
    """
    Gets the contents of a given directory.

    Input:
        working_directory (str): The Working directory allowed to be in.
        directory (str): Directory to target, defaults to current if not given.

    Return:
        contents (str): A strings that are the contents of the directory.
    """
    
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    if not os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    lines: list[str] = []

    try:
        for f in os.listdir(target_dir):
            f_full_path = os.path.join(target_dir,f)
            object_size = str(os.path.getsize(f_full_path)) + ' bytes'
            object_type = os.path.isdir(f_full_path)

            lines.append(f"- {f}: file_size={object_size}, is_dir={object_type}")

    except Exception as e:
        return f"Error: {e}"
    
    return "\n".join(lines)
