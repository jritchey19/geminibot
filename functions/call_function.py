from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_code_file, run_code_file
from functions.write_to_file import schema_write_to_file, write_to_file
from google.genai import types

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, 
        schema_get_file_content, 
        schema_run_code_file, 
        schema_write_to_file
    ],
)

FUNCTION_MAP = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_code_file,
    "write_file": write_to_file
}

def make_tool_response(function_name: str, response: dict[str, object]) -> types.Content:
    """
    Returns a boilerplate types.Content response.

    Args:
        function_name (str): Name of the function that is to be called.
        response (dict[str, object]): The return response in a dict.

    Returns:
        (types.Content): The generated content from the given args.
    """
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response=response,
            )
        ],
    )

def call_function(function_call: types.FunctionCall, verbose: bool = False) -> types.Content:
    """
    Calls a given types.FunctionCall to run the correct function and returns the output.

    Args:
        function_call (types.FunctionCall): A call to specify which function to call.
        verbose (bool): Show verbose messaging.

    Returns:
        (types.Content): Returns output from the function.
    """


    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    
    function_name = function_call.name or ""

    if not function_name in FUNCTION_MAP:
        return make_tool_response(function_name, {"error": f"Unknown function: {function_name}"})
    
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"

    try:
        function_result = FUNCTION_MAP[function_name](**args)
    except Exception as e:
        function_result = f"Error calling function: {e}"

    return make_tool_response(function_name, {"result": function_result})
