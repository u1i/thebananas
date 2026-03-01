### 1. The "Object Persistence" Test

* **The Task:** "Keep the red bus exactly where it is, but change its color to bright blue and add 'Electric Minds' branding on the side."
* **The Goal:** Does the model keep the bus's specific make and model, or does it swap it for a generic blue bus?

### 2. The "Lighting & Time" Shift

* **The Task:** "Change the lighting of this exact scene to 2:00 AM. Turn on the headlights of all cars and make the shop signs glow neon."
* **The Goal:** This tests if the model understands the geometry of the existing objects enough to cast realistic artificial light from them.

### 3. The "Historical Layer" Test

* **The Task:** "Transform the cars in this specific image into vintage 1960s vehicles, but keep the overhead concrete tracks and buildings exactly as they are."
* **The Goal:** This checks for "masking" capability—can it change one category of objects while leaving the architecture untouched?

### 4. The "Artistic Translation" (Ligne Claire)

* **The Task:** "Render this exact photo in the Hergé/Tintin 'ligne claire' style, maintaining the exact position of every car."
* **The Goal:** Testing style transfer without losing the "data" (the specific traffic layout).

### 5. The "Contextual Addition"

* **The Task:** "Add a giant, 20-foot tall 'Guybrush Threepwood' pixel-art character standing on the walkway overlooking the traffic."
* **The Goal:** Testing the blending of two different art styles (pixel art vs. photo) and proper scaling.