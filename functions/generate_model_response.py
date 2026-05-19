from google import genai
from google.genai import errors
from google.genai import types

def generate_model_response(client: genai.Client, model: str, messages: list[types.Content], model_tools: list, system_prompt: str) -> object:
    """
    Returns a response from the given model.

    Args:
        client (genai.Client): The client object that has the user's api key in it.
        model (str): What model should be used.
        messages (list[types.content]): A list of content from the user.
        model_tools (list): A list of available tools that the model has access to.
        system_prompt (str): Instructions for the model to shape how it works.

    Returns:
        (object): Returns a response object from the model.
    """

    try:
        return client.models.generate_content(
            model=model,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[model_tools],
                system_instruction=system_prompt
            )
        )

    except errors.ServerError as e:
        match (e.code):
            case 503:
                print("Cant seem to reach the service (503), better luck next time...")
            case _:
                print(f"Got a {e.code} about:\n{e.message}")
