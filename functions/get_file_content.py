import os

from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a given file up to a max char limit (10000).",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to be read.",
            ),
        },
    ),
)

def get_file_content(working_directory: str, file_path: str) -> str:
    """
    Read the contents of a given file and 
    return it to a max char limit.

    Args:
        working_directory (str): Working directory the agent can be in.
        file_path (str): Path to the file and the file name.

    Returns:
        contents (str): Returns the content of file, up to max.
    """

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_file, 'r') as f:
            contents = f.read(MAX_CHARS)
            if f.read(1):
                contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return contents
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'
    
