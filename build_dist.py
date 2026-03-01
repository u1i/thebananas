import os
import subprocess
import re

TESTS_FILE = "tests2.md"
INPUT_DIR = "test_results2" 
OUTPUT_DIR = "docs"

MODELS = [
    {
        "id": "Nano_Banana_1",
        "label": "Nano Banana"
    },
    {
        "id": "Nano_Banana_1_Pro",
        "label": "Nano Banana Pro"
    },
    {
        "id": "Nano_Banana_2",
        "label": "Nano Banana 2 (New)"
    }
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

def parse_tests():
    with open(TESTS_FILE, "r") as f:
        content = f.read()
    
    blocks = content.split("### ")[1:]
    test_info = {}
    
    for block in blocks:
        lines = [line.strip() for line in block.strip().split("\n") if line.strip()]
        header = lines[0] # e.g. "1. The "Environmental Integration" Test"
        
        task = ""
        goal = ""
        for line in lines[1:]:
            if line.startswith("* **The Task:**"):
                task = line.replace("* **The Task:**", "").strip()
            elif line.startswith("* **The Goal:**"):
                goal = line.replace("* **The Goal:**", "").strip()
                
        # Find which test this maps to
        num_match = re.match(r"(\d+)\.", header)
        if num_match:
            num_str = num_match.group(1)
            # Find matching test string from our hardcoded array
            matching_test = next((t for t in TESTS if t.startswith(f"{num_str}_")), None)
            if matching_test:
                test_info[matching_test] = {
                    "header": header,
                    "task": task,
                    "goal": goal
                }
    return test_info

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    test_details = parse_tests()
    
    md_output = os.path.join(OUTPUT_DIR, "README.md")
    
    with open(md_output, "w") as md:
        md.write("# Nano Banana Evaluation Results\n\n")
        
        for test in TESTS:
            print(f"Building non-anonymized montage for {test}...")
            
            images = []
            labels = []
            valid = True
            
            for m in MODELS:
                img_path = os.path.join(INPUT_DIR, f"{m['id']}_{test}.jpg")
                
                # Use the cropped version for Test 7 Pro
                if test == "7_Extreme_Lighting" and m['id'] == "Nano_Banana_1_Pro":
                    img_path = os.path.join(INPUT_DIR, f"Nano_Banana_1_Pro_7_Extreme_Lighting_Cropped.jpg")
                
                if os.path.exists(img_path):
                    images.append(img_path)
                    labels.append(m['label'])
                else:
                    print(f"Warning: Missing {img_path}")
                    valid = False
            
            if not valid or len(images) != 3:
                print(f"Skipping {test} due to missing images.")
                continue
                
            montage_file = f"{test}_montage.jpg"
            output_patch = os.path.join(OUTPUT_DIR, montage_file)
            
            # Build the command
            cmd = [
                "magick", "montage",
                "-font", "Arial",
                "-pointsize", "48", # Smaller pointsize for longer names
                "-background", "white",
                "-fill", "black",
                "-label", labels[0], images[0],
                "-label", labels[1], images[1],
                "-label", labels[2], images[2],
                "-geometry", "x800+25+25", 
                "-tile", "3x1",            
                output_patch
            ]
            
            try:
                subprocess.run(cmd, check=True)
                print(f"  -> Saved {output_patch}")
                
                # Write to the markdown file
                if test in test_details:
                    info = test_details[test]
                    md.write(f"## {info['header']}\n\n")
                    md.write(f"**The Task:** {info['task']}\n\n")
                    md.write(f"**The Goal:** {info['goal']}\n\n")
                    md.write(f"![Montage of {test}]({montage_file})\n\n")
                    md.write("---\n\n")
                    
            except subprocess.CalledProcessError as e:
                print(f"  -> Error: {e}")

    print(f"\nDist bundle created successfully in {OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
