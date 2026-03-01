import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# Initialize the Gemini GenAI client
# It will automatically pick up GEMINI_API_KEY from the environment
client = genai.Client()

# Define the models from the .env mapping
MODELS = {
    "Nano Banana 1": os.getenv("NANO_BANANA_1", "gemini-2.5-flash-image"),
    "Nano Banana 1 Pro": os.getenv("NANO_BANANA_1_PRO", "gemini-3-pro-image-preview"),
    "Nano Banana 2": os.getenv("NANO_BANANA_2", "gemini-3.1-flash-image-preview")
}

# Define the 10 tests from tests2.md
TESTS = {
    "1_Environmental_Integration": "Generate a close-up selfie of the man in this image on the summit of Mount Everest. He is wearing a heavy down suit, his oxygen mask is pulled down around his neck, and his beard is heavily frosted with ice. The lighting is a golden sunrise.",
    "2_Complex_Background_Depth": "Generate a vertical selfie of the man in this image waiting in a line of climbers at the Hillary Step. He is clipped to a fixed rope, with steep rock, blue ice, and other climbers fading into the blowing snow in the background.",
    "3_Material_Interaction": "Generate a selfie of the man in this image at Everest Base Camp. He is holding a steaming mug of tea, and the lenses of his glasses are slightly fogged up from the steam. Yellow tents are visible behind him.",
    "4_Extreme_Perspective": "Generate an action selfie of the man in this image crossing a metal ladder over a deep crevasse. The camera angle is an extreme high-angle shot, looking down past his face towards his crampon-clad feet and the infinite blue ice below.",
    "5_Low_Light_Fidelity": "Generate a gritty selfie of the man in this image hunched inside a dim yellow tent during a blizzard at the South Col. He is wearing a balaclava, with blowing snow visible through the partially open tent flap.",
    "6_Physiological_Alteration": "Generate a selfie of the man in this image sitting on a rock in the 'Death Zone' at 8,000 meters. Alter his face to look utterly exhausted: give him gaunt cheeks, cracked lips, and weary, bloodshot eyes, but keep him completely recognizable.",
    "7_Extreme_Lighting": "Generate a wide-angle selfie of the man in this image on the summit. The sun is cresting the horizon directly behind his head, casting harsh, directional backlighting and a lens flare, with the curvature of the Earth visible in the distance.",
    "8_Dynamic_Action_Framing": "Generate a dynamic selfie of the man in this image rappelling backwards down a vertical ice wall. The camera angle is looking slightly up at him as he leans back on the rope, with ice chips flying through the air.",
    "9_Multi_Subject_Context": "Generate a selfie of the man in this image sitting at a Puja ceremony at Base Camp. He is surrounded by three Sherpas in traditional climbing gear, with a stone altar and thick juniper smoke blending into the scene.",
    "10_Motion_Blur_Artifacting": "Generate a point-of-view selfie of the man in this image taking his final, grueling steps to the summit. The image should have a slight motion blur to simulate a shaking, freezing hand holding the camera."
}

INPUT_IMAGE_FILE = "u.jpg"
OUTPUT_DIR = "test_results2"

def main():
    if not os.path.exists(INPUT_IMAGE_FILE):
        print(f"Error: Input image '{INPUT_IMAGE_FILE}' not found.")
        return

    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Upload the input image once to be used as a reference/input
    print(f"Uploading input image {INPUT_IMAGE_FILE}...")
    source_image = client.files.upload(file=INPUT_IMAGE_FILE)
    print(f"Uploaded successfully as {source_image.name}")

    total_tests = len(MODELS) * len(TESTS)
    current_test = 1

    print(f"Starting execution of {total_tests} test cases (3 models x 5 tests)...\n")

    for model_name, model_id in MODELS.items():
        print(f"--- Testing Model: {model_name} ({model_id}) ---")
        
        for test_name, prompt in TESTS.items():
            output_filename = os.path.join(OUTPUT_DIR, f"{model_name.replace(' ', '_')}_{test_name}.jpg")
            
            if os.path.exists(output_filename):
                print(f"[{current_test}/{total_tests}] Skipping Test (Already Exists): {test_name}")
                current_test += 1
                continue
                
            print(f"[{current_test}/{total_tests}] Running Test: {test_name}")
            
            try:
                # Use generate_content for Gemini 2.5/3.0 image models
                # Provide the source image and prompt as contents
                result = client.models.generate_content(
                    model=model_id,
                    contents=[source_image, prompt],
                )

                # Search through the parts for inline image data
                image_data = None
                if result.candidates and result.candidates[0].content.parts:
                    for part in result.candidates[0].content.parts:
                        if getattr(part, 'inline_data', None):
                            image_data = part.inline_data.data
                            break
                        
                if image_data:
                    # Save the resulting image
                    with open(output_filename, 'wb') as f:
                        f.write(image_data)
                    print(f"  -> Success! Saved to {output_filename}")
                else:
                    print("  -> Failed: No image returned in the generation response. Text response was: ", result.text if hasattr(result, 'text') else 'None')
                    
            except Exception as e:
                print(f"  -> Error executing test for {model_name}: {e}")
                
            current_test += 1
            print("-" * 40)
            
    print("\nAll tests completed.")

if __name__ == "__main__":
    main()
