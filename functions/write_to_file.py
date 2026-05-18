import os

from google.genai import types

schema_write_to_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes given content to a file in a given path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the file to be written to. (ex: output/myfile.py)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written to a file.",
            ),
        },
    ),
)

def write_to_file(working_directory: str, file_path: str, content: str) -> str:
    """
    Write content to a given file.

    Args:
        working_directory (str): Directory the agent can work in.
        file_path (str): File to write to.
        content (str): Content to be written to given file.

    Returns:
        (str): Returns a success string
    """
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
    
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error writing to "{file_path}": {e}'

