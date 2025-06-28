import os
import json
import openai
import argparse
import requests
from openai import OpenAI
from dotenv import load_dotenv
import base64

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
model_name = os.getenv('OPENAI_MODEL_NAME')
if not model_name:
    model_name = "gpt-4o"
print(f"Using model: {model_name}")
temperature = os.getenv('OPENAI_TEMPERATURE')
if not temperature:
    temperature = 0.7
else:
    temperature = float(temperature)
print(f"Using temperature: {temperature}")
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

def encode_image(image_path):
    """Encode image to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_cleanup_content(content, schema, image_path=None):
    """Send the prompt and content to OpenAI's API or Gemini API and get the structured content."""
    
    if model_name.startswith("gemini"):
        # Use Gemini API
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={gemini_api_key}"
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Prepare request data
        gemini_data = {
            "contents": [{
                "parts": []
            }],
            "generationConfig": {
                "temperature": temperature
            }
        }
        
        # Add system prompt as text
        system_prompt = f"You are a helpful assistant that generates structured output based on the following JSON schema: {json.dumps(schema)}"
        gemini_data["contents"][0]["parts"].append({"text": system_prompt + "\n\n" + content})
        
        # Add image if provided
        if image_path:
            base64_image = encode_image(image_path)
            gemini_data["contents"][0]["parts"].append({
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": base64_image
                }
            })
        
        response = requests.post(url, headers=headers, data=json.dumps(gemini_data))
        response_json = response.json()
        
        if 'candidates' in response_json and len(response_json['candidates']) > 0:
            # Extract the JSON response from the text
            response_text = response_json['candidates'][0]['content']['parts'][0]['text']
            # Find JSON content in the response (it might be wrapped in markdown code blocks)
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    # If direct parsing fails, try to clean up the string
                    cleaned_json = json_str.replace('\n', '').replace('\\', '\\\\')
                    return json.loads(cleaned_json)
            raise Exception("Could not extract valid JSON from Gemini response")
        else:
            raise Exception(f"Gemini API error: {response_json}")
    else:
        # Use OpenAI API
        messages = [
            {"role": "system", "content": f"You are a helpful assistant that generates structured output based on the following JSON schema: {json.dumps(schema)}"}
        ]

        # Prepare user message with optional image
        if image_path:
            base64_image = encode_image(image_path)
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": content
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            })
        else:
            messages.append({"role": "user", "content": content})

        completion = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "response",
                    "schema": schema,
                    "strict": True
                }
            }
        )

        return json.loads(completion.choices[0].message.content)

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Generate a structured version of a text file using OpenAI's GPT-4."
    )
    parser.add_argument('input_file', help='Path to the input .txt file')
    parser.add_argument('output_file', help='Path to save the structured output file')
    parser.add_argument('schema_file', help='Path to the JSON schema file')
    parser.add_argument('--image', help='Optional path to an image file', default=None)

    args = parser.parse_args()

    try:
        # Read input file
        input_content = read_file(args.input_file)

        # Read schema file
        schema = json.loads(read_file(args.schema_file))

        # Generate structured content with optional image
        structured_content = generate_cleanup_content(input_content, schema, args.image)

        # Write to output file
        write_file(args.output_file, json.dumps(structured_content, indent=2))

        print(f"Successfully processed '{args.input_file}' and saved structured output to '{args.output_file}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
