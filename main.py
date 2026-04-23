import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import call_function, available_functions

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

#parsing user input
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]


for _ in range(20):

    # Make the API call
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature=0)
        )
    
    #Check the .candidates field and if some itterate and append the .content to the messages list
    if response.candidates is not None:
        for candidate in response.candidates:
            if candidate.content is not None:
                messages.append(candidate.content)




    # Showing the results of the response and usage metadata if verbose flag is set
    if args.verbose:

        if response.usage_metadata is None:
            raise RuntimeError("Usage metadata is not available")
        else:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            


    if response.function_calls:

        parts_list = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=args.verbose)
            if function_call_result.parts is None:
                raise RuntimeError("Error: No parts found in the function call result.")
            if function_call_result.parts[0].function_response is None:
                raise RuntimeError("Error: No function response found in the function call result.")
            if function_call_result.parts[0].function_response.response is None:
                raise RuntimeError("Error: No response found in the function call result.")
            
            parts_list.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        messages.append(types.Content(role="user", parts=parts_list))
    else:
        print(response.text)
        break
else:
    print("Reached maximum number of iterations without a final response.")
    sys.exit(1)