import argparse
import os

from config import MAX_ITER, MODEL
from dotenv import load_dotenv
from functions.call_function import available_functions, call_function
from functions.prompts import system_prompt
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

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")
    
    parser = argparse.ArgumentParser(
        description="Gemini Chatbot"
    )
    parser.add_argument("user_prompt", type=str, help="User prompt to ask the Chatbot.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")
    args = parser.parse_args()

    client = genai.Client(api_key=api_key)
    
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = generate_model_response(client, MODEL, messages, available_functions, system_prompt)

    if response.usage_metadata is None:
        raise RuntimeError("No usage metadata returned from Gemini API")
    
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
   
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
        print("Response:")
        print("<--------------------------------------------------->")

    if response.function_calls:
        for function_call in response.function_calls:
            if function_call:
                function_call_result = call_function(function_call)
                if not function_call_result.parts:
                    raise Exception(f"Function call {function_call} returned empty parts list...")
                if not function_call_result.parts[0].function_response:
                    raise Exception(f"Function call {function_call} has an empty function_response...")
                if not function_call_result.parts[0].function_response.response:
                    raise Exception(f"Function call {function_call} has a empty responce in its function_response...")
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

    else:
        print(response.text or "No response text returned...")
    
if __name__ == '__main__':
    main()
