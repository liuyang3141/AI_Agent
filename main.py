import os
from dotenv import load_dotenv
from google import genai
import sys

def main():
    # Check to see if a prompt has been provided.
    if len(sys.argv) <= 1:
        raise Exception("No prompt provided.")

    # Load environmental variable .env, where the API key is stored.
    load_dotenv()

    # Create a variable to store the API key.
    api_key = os.environ.get("GEMINI_API_KEY")

    # Create a new instance of a Gemini client.
    client = genai.Client(api_key=api_key)

    # Use the client.models.generate_content() method to get a response
    # from the gemini-2.0-flash-001 model.
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=sys.argv[1])

    # Print the response.
    print(response.text)

    # Print tokens in the prompt.
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")

    # Print tokens in the response.
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
