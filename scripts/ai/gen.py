import os
import openai
import argparse
import requests
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
model_name = os.getenv('OPENAI_MODEL_NAME')
if not model_name:
    model_name = "gpt-4o"
temperature = os.getenv('OPENAI_TEMPERATURE')
if not temperature:
    temperature = 0.7
else:
    temperature = float(temperature)
client = OpenAI()
gemini_api_key = os.getenv('GEMINI_API_KEY')

def read_file(file_path):
    """Read the content of the input file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    """Write the content to the output file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def generate_cleanup_content(content):
    """Send the prompt and content to OpenAI's API or Gemini API and get the cleaned content."""
    
    if model_name.startswith("gemini"):
        # Use Gemini API
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={gemini_api_key}"
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "contents": [{
                "parts": [{"text": content}]
            }],
            "generationConfig": {
                "temperature": temperature
            }
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response_json = response.json()
        
        if 'candidates' in response_json and len(response_json['candidates']) > 0:
            return response_json['candidates'][0]['content']['parts'][0]['text']
        else:
            # Check for specific error types
            if 'promptFeedback' in response_json and 'blockReason' in response_json['promptFeedback']:
                block_reason = response_json['promptFeedback']['blockReason']
                if block_reason == 'PROHIBITED_CONTENT':
                    raise Exception(f"Gemini API error: {response_json} - Content was blocked due to prohibited content")
            # Generic error
            raise Exception(f"Gemini API error: {response_json}")
    else:
        # Use OpenAI API
        completion = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "user", "content": content}
                    ],
                    temperature=temperature
                )

        return str(completion.choices[0].message.content)

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Generate a cleaned-up version of a text file using OpenAI's GPT-4."
    )
    parser.add_argument('input_file', help='Path to the input .txt file')
    parser.add_argument('output_file', help='Path to save the cleaned output file')

    args = parser.parse_args()

    try:
        # Read input file
        input_content = read_file(args.input_file)

        # Generate cleaned content
        cleaned_content = generate_cleanup_content(input_content)

        # Write to output file
        write_file(args.output_file, cleaned_content)

        print(f"Successfully processed '{args.input_file}' and saved to '{args.output_file}'.")

    except Exception as e:
        print(f"An error occurred: {e}")
        # Exit with non-zero status to indicate error
        exit(1)

if __name__ == "__main__":
    main()
