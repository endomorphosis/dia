# Simple Text to Speech Example

This example shows the most basic usage of Dia for generating speech from text.

## Basic Usage

```python
from dia.model import Dia

# Load the Dia model
model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")

# Create dialogue text using speaker tags [S1] and [S2]
text = "[S1] Dia is a text to speech model for generating dialogue. [S2] It supports multiple speakers and can create natural conversations."

# Generate audio
output = model.generate(text, use_torch_compile=True, verbose=True)

# Save the generated audio to a file
model.save_audio("simple_output.mp3", output)
```

## Adding Variations

You can adjust generation parameters to change the output:

```python
# More deterministic output (lower temperature)
output_deterministic = model.generate(
    text, 
    temperature=0.5,         # Lower temperature means more deterministic output
    use_torch_compile=True, 
    verbose=True
)

# More varied output (higher temperature)
output_varied = model.generate(
    text, 
    temperature=1.2,         # Higher temperature means more varied output
    use_torch_compile=True, 
    verbose=True
)

# Save both outputs
model.save_audio("output_deterministic.mp3", output_deterministic)
model.save_audio("output_varied.mp3", output_varied)
```

## Longer Dialogue Example

Creating a more complex dialogue with multiple turn-taking:

```python
from dia.model import Dia

model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")

# A longer dialogue with multiple exchanges
text = """
[S1] Have you heard about the new text-to-speech model called Dia?
[S2] No, I haven't. What makes it special?
[S1] It's specifically designed for dialogue generation, so it can handle conversations naturally.
[S2] That sounds impressive. How realistic does it sound?
[S1] Very realistic! It can even include laughs, pauses, and other non-verbal elements.
[S2] Wow, I'd love to try it myself.
[S1] You can! It's available as an open weights model.
"""

# Generate audio 
output = model.generate(
    text,
    max_new_tokens=2048,     # Allow for longer generation
    use_torch_compile=True,
    verbose=True
)

model.save_audio("dialogue_example.mp3", output)
```

## Customizing Sampling Parameters

Fine-tune the generation process by adjusting sampling parameters:

```python
from dia.model import Dia

model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")

text = "[S1] This is an example of customized generation with Dia."

# Generate with customized parameters
output = model.generate(
    text,
    temperature=0.8,         # Controls randomness (lower = more deterministic)
    top_p=0.92,              # Controls diversity via nucleus sampling
    top_k=50,                # Limits vocabulary choices to top K tokens
    use_torch_compile=True,
    verbose=True
)

model.save_audio("customized_output.mp3", output)
```

## Using Different Devices

Specify which device to use for computation:

```python
from dia.model import Dia

# Use CPU explicitly
cpu_model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16", device="cpu")

# Use CUDA explicitly (if available)
cuda_model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16", device="cuda")

# Use MPS explicitly (if available, Apple Silicon)
mps_model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16", device="mps")

# Generate audio using the model loaded on specific device
text = "[S1] This is generated on a specific device."
output = cuda_model.generate(text, use_torch_compile=True)
cuda_model.save_audio("device_specific_output.mp3", output)
```

## Complete Example with Progress Tracking

A complete example that includes progress tracking via callback:

```python
from dia.model import Dia
import time

def progress_callback(current_step: int, total_steps: int):
    """Simple callback to track generation progress."""
    progress = (current_step / total_steps) * 100
    print(f"Generation progress: {progress:.2f}% ({current_step}/{total_steps})")

# Load model
model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")

# Create text input
text = "[S1] This example demonstrates how to track progress during speech generation."

# Start timing
start_time = time.time()

# Generate with progress tracking
output = model.generate(
    text,
    use_torch_compile=True,
    verbose=True,
    callback=progress_callback  # Pass the callback function
)

# Calculate total time
generation_time = time.time() - start_time
print(f"Generation completed in {generation_time:.2f} seconds")

# Save output
model.save_audio("tracked_output.mp3", output)
```
