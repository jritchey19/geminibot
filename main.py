import argparse
import os
import sys

from config import MAX_ITER, MODEL
from dotenv import load_dotenv
from functions.call_function import available_functions, call_function
from functions.generate_model_response import generate_model_response
from functions.prompts import system_prompt
from google import genai
from google.genai import errors
from google.genai import types

def main():
    """
    Geminibot, a ai agent that takes in user prompt, works the request and returns output.
    """

    # Final response and tokens used.
    FINAL_RESULTS: list[str] = []
    LOOP_COMPLETE = False
    PROMPT_TOKENS: int = 0
    RESPONSE_TOKENS: int = 0

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

    # Agent loop set to max iteration in the config.
    for _ in range(MAX_ITER):
        response = generate_model_response(client, MODEL, messages, available_functions, system_prompt)

        if response is None:
            raise RuntimeError("No usage metadata returned from Gemini API")
        
        PROMPT_TOKENS += response.usage_metadata.prompt_token_count
        RESPONSE_TOKENS += response.usage_metadata.candidates_token_count

        if response.candidates:
            for r_candidate in response.candidates:
                messages.append(r_candidate.content)
   

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
                        FINAL_RESULTS.append(f"-> {function_call_result.parts[0].function_response.response}")
                    messages.append(types.Content(role="user", parts=function_call_result.parts))

        else:
            FINAL_RESULTS.append(response.text or "No response text returned...")
            LOOP_COMPLETE = True
            break

    if LOOP_COMPLETE == False:
        print(f"Loop Failed to produce meaningful results after {MAX_ITER} tries...")
        sys.exit(1)

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {PROMPT_TOKENS}")
        print(f"Response tokens: {RESPONSE_TOKENS}")
        print("Response:")
        print("<--------------------------------------------------->")
    for line in FINAL_RESULTS:
        print(line)

    
if __name__ == '__main__':
    main()
