"""
code_pal.py: A simple script that uses the PaLM API to assist with coding queries.
"""

import os
from termcolor import colored

# Assuming google.generativeai is available and installed
import google.generativeai as palm
from google.api_core import client_options as client_options_lib
from google.api_core import retry
from google.api_core.exceptions import Forbidden

def get_api_key(filename="api_key"):
    """
    Reads the API key from a specified file.

    Args:
        filename (str): Name of the file containing the API key.

    Returns:
        str: The API key.
    """
    with open(filename, "r", encoding="utf-8") as file:
        return file.readline().strip()

# Configuration for the PaLM API
palm.configure(
    api_key=get_api_key(),
    transport="rest",
    client_options=client_options_lib.ClientOptions(
        api_endpoint=os.getenv("GOOGLE_API_BASE"),
    )
)

# Helper function to generate text
@retry.Retry()
def generate_text(prompt, model=None, temperature=0.0):
    """
    Generate text based on the provided prompt using the PaLM API.

    Args:
        prompt (str): The user's question or prompt.
        model: The PaLM model to use for text generation. Defaults to the first model
        supporting 'generateText'. temperature (float): The randomness of the model's
        output. Default is 0.0 (deterministic).

    Returns:
        str: The generated code or answer.
    """
    if model is None:
        models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
        model = models[0]
    return palm.generate_text(prompt=prompt, model=model, temperature=temperature)

def main():
    """
    The main function to initiate the CodePal application.
    """
    print(colored("Welcome to the PaLM Code Assistant!", "yellow"))
    print(colored("Ask me any coding-related question and I'll provide you the code.", "yellow"))

    while True:
        # Ask user for a coding question
        prompt = input(colored("\nEnter your question: ", "green"))

        # Special commands
        if prompt.lower() in ["exit", "quit"]:
            print(colored("Goodbye!", "red"))
            break

        try:
            # Fetch code from PaLM API
            completion = generate_text(prompt)

            # Print the generated code in blue
            print(colored("\nGenerated Code:", "cyan"))
            print(colored(completion.result, "blue"))

        except Forbidden:
            print(colored("Error: Generative Language API access is forbidden.", "red"))
            print(colored("Please ensure you've enabled the API and have the correct permissions.", "red"))
            break  # Optionally exit the script, or you can continue asking for other prompts

if __name__ == "__main__":
    main()
