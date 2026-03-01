import os
import subprocess
import random
import csv

# We use the raw images without the model names written on them!
INPUT_DIR = "test_results2" 
OUTPUT_DIR = "eval_montages2"

# The 3 models we want to compare blindly
MODELS = [
    "Nano_Banana_1",
    "Nano_Banana_1_Pro",
    "Nano_Banana_2"
]

TESTS = [
    "1_Environmental_Integration",
    "2_Complex_Background_Depth",
    "3_Material_Interaction",
    "4_Extreme_Perspective",
    "5_Low_Light_Fidelity",
    "6_Physiological_Alteration",
    "7_Extreme_Lighting",
    "8_Dynamic_Action_Framing",
    "9_Multi_Subject_Context",
    "10_Motion_Blur_Artifacting"
]

def main():
    if not os.path.exists(INPUT_DIR):
        print(f"Error: {INPUT_DIR} not found.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Keep track of which model is 1, 2, and 3 for each test to create an answer key
    answer_key = []
    
    for test in TESTS:
        print(f"Creating blind evaluation montage for {test}...")
        
        # Shuffle the models around so "1" is not always the same model
        shuffled_models = MODELS.copy()
        random.shuffle(shuffled_models)
        
        images = []
        for model in shuffled_models:
            img_path = os.path.join(INPUT_DIR, f"{model}_{test}.jpg")
            if os.path.exists(img_path):
                images.append(img_path)
            else:
                print(f"Warning: Missing {img_path}")
                
        if len(images) != 3:
            print(f"Skipping {test} due to missing images.")
            continue
            
        output_path = os.path.join(OUTPUT_DIR, f"Eval_{test}.jpg")
        
        # Record the mapping for this test
        # Model 1, Model 2, Model 3
        answer_key.append({
            "Test": test,
            "1": shuffled_models[0],
            "2": shuffled_models[1],
            "3": shuffled_models[2]
        })
        
        cmd = [
            "magick", "montage",
            "-font", "Arial",
            "-pointsize", "72",
            "-background", "white",
            "-fill", "black",
            "-label", "1", images[0],
            "-label", "2", images[1],
            "-label", "3", images[2],
            "-geometry", "x800+25+25", 
            "-tile", "3x1",            
            output_path
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"  -> Saved {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"  -> Error: {e}")

    # Write the answer key so the user can de-anonymize the results later!
    answer_key_path = os.path.join(OUTPUT_DIR, "answer_key.csv")
    with open(answer_key_path, "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Test", "1", "2", "3"])
        writer.writeheader()
        writer.writerows(answer_key)
        
    print(f"\nDone! Answer key saved to {answer_key_path}")

if __name__ == "__main__":
    main()
