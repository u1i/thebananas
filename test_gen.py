import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()

model_id = os.environ.get("NANO_BANANA_2")
print(f"Testing model: {model_id}")

try:
    result = client.models.generate_images(
        model='imagen-3.0-generate-002',
        prompt='Draw a car',
        config=types.GenerateImagesConfig(
            number_of_images=1,
            output_mime_type="image/jpeg"
        )
    )
    if result.generated_images:
        print("generate_images with imagen-3.0-generate-002 works!")
except Exception as e:
    print("generate_images error:", e)

try:
    print(f"Testing generate_content with {model_id}...")
    result = client.models.generate_content(
        model=model_id,
        contents="Draw a red square.",
    )
    for part in result.candidates[0].content.parts:
        if part.inline_data:
            print("Got inline_data!", part.inline_data.mime_type)
        elif part.text:
            print("Got text!", part.text)
        elif getattr(part, 'executable_code', None):
             print("Got code")
except Exception as e:
    print("generate_content error:", e)
