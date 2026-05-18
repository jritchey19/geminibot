import os
import subprocess

from google.genai import types

schema_run_code_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a given python file with optional arguments. Returns results.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to be ran by agent.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Arguments for the python file if needed. Should be as a list of strings.",
            ),
        },
    ),
)

def run_code_file(working_directory: str, file_path: str, args: list[str] = None ) -> None:
    """
    Runs Code written in a file.

    Args:
        working_directory (str): Directory that the agent can work in.
        file_path (str): Path to file that should be ran.
        args (str): Arguments for the file. Optional.

    Returns:
        None
    """
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file' 
        
        if target_file.split('.')[-1] != 'py':
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args:
            command.extend(args)

        results = subprocess.run(
            command, 
            capture_output=True, 
            cwd=os.path.dirname(target_file), 
            text=True,
            timeout=30
        )
        
        if results.returncode > 0:
            return_string = f"Process exited with code {results.returncode}"
        elif not results.stdout and not results.stderr:
            return_string = "No output produced"
        else:
            return_string = f"STDOUT: {results.stdout}\nSTDERR: {results.stderr}"

        return return_string

    except Exception as e:
        return f"Error: executing Python file: {e}"
