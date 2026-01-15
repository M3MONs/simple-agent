import argparse
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    client = genai.Client(api_key=api_key)
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
    
    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=config,
        )
        if response.usage_metadata is None:
            raise RuntimeError("API request failed or usage metadata not available.")
        
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content) # type: ignore
        
        if args.verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
        if response.function_calls:
            for call in response.function_calls:
                result = call_function(call, verbose=args.verbose)
                if not result.parts:
                    raise Exception("Function call returned no parts.")
                if result.parts[0].function_response is None:
                    raise Exception("Function response is None.")
                if result.parts[0].function_response.response is None:
                    raise Exception("Function response.response is None.")
                if args.verbose:
                    print(f"-> {result.parts[0].function_response.response}")
                messages.append(types.Content(role="user", parts=result.parts))
        else:
            print(response.text)
            break
    else:
        print("Reached maximum iterations without a final response.")
        sys.exit(1)


if __name__ == "__main__":
    main()
