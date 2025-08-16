from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys # Check for arguments in the command line.
import argparse # Check if specific arguments were entered in the command line.
import os # Check environmental variable .env for API key.
from call_function import *

def main():
    # Load environmental variable .env, where the API key is stored.
    load_dotenv()

    # Check to see if a prompt has been provided.
    if len(sys.argv) <= 1:
        raise Exception("No prompt provided.")

    verbose_flag = False

    # Check if there are 3 or more elements in sys.argv.
    if len(sys.argv) >= 3:
        # Create an ArgumentParser object.
        parser = argparse.ArgumentParser(description="Get a response from the Gemini API")

        # Define the "prompt" as a required positional argument.
        parser.add_argument('prompt', type=str, help='The prompt to send to the Gemini API.')

        # Add a check for the --verbose argument. Use action='store_true' to automatically
        # set the variable to True if the flag is present, and False otherwise.
        parser.add_argument('--verbose', action='store_true', help='Enable verbose output.')

        # Check if --verbose is present.
        args = parser.parse_args()
        verbose_flag = args.verbose
        user_prompt = args.prompt
    else:
        user_prompt = sys.argv[1]

    # Create a variable to store the API key.
    api_key = os.environ.get("GEMINI_API_KEY")

    # Create a new instance of a Gemini client.
    client = genai.Client(api_key=api_key)

    # Create a new list of types.Content, and set the user's prompt as the only message.
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    generate_content(client, messages, verbose_flag)

def generate_content(client, messages, verbose_flag):
    # Use the client.models.generate_content() method to get a response
    # from the gemini-2.0-flash-001 model.
    response = client.models.generate_content(model = 'gemini-2.0-flash-001',
        contents = messages,
        config = types.GenerateContentConfig(
            tools = [available_functions], system_instruction = system_prompt
        ),
    )

    if verbose_flag:
        # Print the following if verbose_flag = True
        # Print tokens in the prompt.
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        # Print tokens in the response.
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # Get a list of the functions called by the LLM.
    function_responses = list()

    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose_flag)
        if (
            not function_call_result.parts or not function_call_result.parts[0].function_response
        ):
            raise Exception("Empty function call result.")
        if verbose_flag:
            print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("No function responses generated, exiting.")



if __name__ == "__main__":
    main()
