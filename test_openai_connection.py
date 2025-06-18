import os
import google.generativeai as genai

def list_available_models(api_key):
    """
    List all available models in the Gemini API.
    
    :param api_key: Your Gemini API key.
    """
    # Configure the API key
    genai.configure(api_key=api_key)
    
    # Fetch the list of models
    models = genai.list_models()
    
    # Print the available models
    print("Available Gemini Models:")
    for model in models:
        print(f"- {model.name}")  # Use 'name' instead of 'id' for Gemini models

if __name__ == "__main__":
    # Set your API key here
    API_KEY = os.environ.get("GEMINI_API_KEY")
    
    if API_KEY:
        list_available_models(API_KEY)
    else:
        print("Please set your GEMINI_API_KEY environment variable.")
