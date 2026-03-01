import os
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define the models and their display names from .env
# The keys match the prefix of the files generated in run_tests.py
MODEL_MAPPING = {
    "Nano_Banana_1_Pro": os.getenv("NANO_BANANA_1_PRO_NAME", "Nano Banana Pro"),
    "Nano_Banana_1": os.getenv("NANO_BANANA_1_NAME", "Nano Banana"),
    "Nano_Banana_2": os.getenv("NANO_BANANA_2_NAME", "Nano Banana 2 (New)")
}

INPUT_DIR = "test_results2"
OUTPUT_DIR = "labeled_results2"

def main():
    if not os.path.exists(INPUT_DIR):
        print(f"Error: {INPUT_DIR} not found.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".jpg")]
    
    for filename in files:
        input_path = os.path.join(INPUT_DIR, filename)
        # Determine the display name and extract the test name
        display_name = "Unknown Model"
        model_key = None
        # Since Nano_Banana_1 is a prefix of Nano_Banana_1_Pro, check Pro first
        if filename.startswith("Nano_Banana_1_Pro"):
            model_key = "Nano_Banana_1_Pro"
        elif filename.startswith("Nano_Banana_1"):
            model_key = "Nano_Banana_1"
        elif filename.startswith("Nano_Banana_2"):
            model_key = "Nano_Banana_2"
            
        if model_key:
            display_name = MODEL_MAPPING[model_key]
            # filename is like: Nano_Banana_1_Pro_1_Object_Persistence.jpg
            # extract the test part by removing model_key and the underscore before it, and .jpg at the end
            test_name = filename[len(model_key)+1:-4]
            new_filename = f"{test_name}_{model_key}.jpg"
        else:
            new_filename = filename
            
        output_path = os.path.join(OUTPUT_DIR, new_filename)
            
        # Pad the display name slightly with spaces for the label
        padded_name = f"  {display_name}  "
        print(f"Processing {filename} -> Watermark: '{display_name}' -> Output: {new_filename}")
        
        # Build the ImageMagick command using the annotate method for a clean label at the bottom left
        # -undercolor provides the label background, -fill provides the text color
        cmd = [
            "magick", input_path,
            "-gravity", "SouthWest",
            "-fill", "white",
            "-undercolor", "#8B8000",
            "-font", "Arial", # Fallback font, IM will usually find a sans-serif
            "-pointsize", "48", # Large enough to be readable
            "-annotate", "+20+20", padded_name,
            output_path
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"  -> Saved to {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"  -> Error processing {filename}: {e}")

if __name__ == "__main__":
    main()
