import os
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")
    
    user_prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum." 
    client = genai.Client(api_key=api_key)
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_prompt
    )
    
    if response.usage_metadata is None:
        raise RuntimeError("No usage metadata returned from Gemini API")
    
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
    print("Response:")
    print(response.text or "No response text returned...")
    
if __name__ == '__main__':
    main()
