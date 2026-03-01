import os
import re
from dotenv import load_dotenv
from google import genai
import csv

load_dotenv()
client = genai.Client()

TESTS_FILE = "tests2.md"
MONTAGE_DIR = "eval_montages2"
ANSWER_KEY_FILE = os.path.join(MONTAGE_DIR, "answer_key.csv")
OUTPUT_REPORT = "test_evaluations_report.md"
EVAL_MODEL = "gemini-3.1-pro-preview" # Using the latest pro model as our high-end judge

def parse_tests():
    with open(TESTS_FILE, "r") as f:
        content = f.read()
    
    # Split by ### 
    blocks = content.split("### ")[1:]
    tests = {}
    for block in blocks:
        lines = block.strip().split("\n")
        header = lines[0].strip()
        
        # Match e.g. "1. The "Environmental Integration" Test" -> 1_Environmental_Integration
        match = re.match(r"(\d+)\.\s+The\s+\"([^\"]+)\"", header)
        if match:
            num = match.group(1)
            name = match.group(2).replace(" ", "_").replace("&", "").replace("-", "_")
            # Cleanup the name to match our file names
            test_key = f"{num}_{name}"
            # Quick hack since some names don't map perfectly from the regex
            pass
            
        # Instead of strict regex, let's just use the exact list we used in creation
        # to ensure it matches
        pass
        
    return content

# The exact list used to generate the images
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
    if not os.path.exists(MONTAGE_DIR):
        print("Montages not found!")
        return

    print("Uploading Original Image Context...")
    user_image = client.files.upload(file="u.jpg")
    
    # Read the goal for context
    with open(TESTS_FILE, "r") as f:
        tests_md = f.read()

    # Load the answer key to decode afterwards
    answer_key = {}
    if os.path.exists(ANSWER_KEY_FILE):
        with open(ANSWER_KEY_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                answer_key[row["Test"]] = row
                
    with open(OUTPUT_REPORT, "w") as out:
        out.write("# Automated Blind Model Evaluation\n\n")
        out.write("Using `gemini-2.5-pro` as the judge. The models were evaluated completely blindly based on the original goals.\n\n")
        
    for test in TESTS:
        img_path = os.path.join(MONTAGE_DIR, f"Eval_{test}.jpg")
        if not os.path.exists(img_path):
            print(f"Skipping {test}, montage not found.")
            continue
            
        print(f"\nEvaluating {test}...")
        montage_file = client.files.upload(file=img_path)
        
        prompt = f"""
You are an expert AI image evaluator. 
I have uploaded the INITIAL original image (the man climbing), and a MONTAGE of 3 different AI generations attempting to edit that original image based on a specific prompt.
The 3 generated images are labeled 1, 2, and 3 below them in the montage.

Here is the exact test description from our evaluation suite:

---
{tests_md}
---

Your job is to evaluate ONLY the test matching "{test}". Look at the original image, read the "Task" and "Goal" for this specific test, and then analyze the montage.

Provide:
1. **Analysis**: A short critical analysis of how well Image 1, Image 2, and Image 3 followed the prompt, maintained the original subject's identity, and executed the specific "Goal".
2. **Ranking**: Rank them from 1st (Best) to 3rd (Worst).

Format your response strictly as:
### Analysis
(your analysis here)

### Ranking
1st: Image [X]
2nd: Image [Y]
3rd: Image [Z]
"""

        try:
            response = client.models.generate_content(
                model=EVAL_MODEL,
                contents=[user_image, montage_file, prompt]
            )
            
            evaluation = response.text
            print(f"  -> Evaluated!")
            
            # Write to report
            with open(OUTPUT_REPORT, "a") as out:
                out.write(f"## Test: {test}\n\n")
                out.write(evaluation + "\n\n")
                
                # Reveal the key!
                if test in answer_key:
                    out.write("### 🔑 The Reveal (Answer Key)\n")
                    out.write(f"- **Image 1**: {answer_key[test]['1']}\n")
                    out.write(f"- **Image 2**: {answer_key[test]['2']}\n")
                    out.write(f"- **Image 3**: {answer_key[test]['3']}\n\n")
                
                out.write("---\n\n")
                
        except Exception as e:
            print(f"  -> Error evaluating {test}: {e}")

    print(f"\nEvaluation complete! Report saved to {OUTPUT_REPORT}")

if __name__ == "__main__":
    main()
