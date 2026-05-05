import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors
from google.genai import types

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

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=messages
        )
    except errors.ServerError as e:
        match (e.code):
            case 503:
                print("Cant seem to reach the service (503), better luck next time...")
            case _:
                print(f"Got a {e.code} about:\n{e.message}")
        #if e.code = 503:
        #    print("Cant seem to reach the service (503), better luck next time...")
        #else
    
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
    print(response.text or "No response text returned...")
    
if __name__ == '__main__':
    main()
