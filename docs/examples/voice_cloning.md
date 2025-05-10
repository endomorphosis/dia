# Voice Cloning Example

This example demonstrates how to use Dia's voice cloning capabilities to generate speech that matches a reference audio sample.

## Basic Voice Cloning

```python
from dia.model import Dia

# Load the model
model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")

# Transcript of the reference audio
# This must match the content of your reference audio file
clone_from_text = "[S1] This is a sample voice that I want to clone."

# Path to the reference audio file
clone_from_audio = "reference_voice.mp3"  # Replace with your audio file path

# New text to generate with the cloned voice
text_to_generate = "[S1] This is new text that will be spoken in the cloned voice."

# Generate audio with voice cloning
# Note: We concatenate the reference transcript and the new text
output = model.generate(
    clone_from_text + text_to_generate,  # Combined text
    audio_prompt=clone_from_audio,       # Reference audio
    use_torch_compile=True,
    verbose=True
)

# Save the generated audio
model.save_audio("cloned_voice_output.mp3", output)
```

## Voice Cloning with Multiple Speakers

When you want to clone multiple voices from a reference audio:

```python
from dia.model import Dia

model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")

# Transcript with two speakers - must match your reference audio
clone_from_text = "[S1] Hello, my name is Alice. [S2] And I'm Bob, nice to meet you."

# Path to audio file containing both speakers
clone_from_audio = "two_speakers.mp3"  # Replace with your audio file

# New dialogue to generate with the cloned voices
text_to_generate = """
[S1] I'm going to tell you about an interesting project.
[S2] I'm very excited to hear about it!
[S1] It's a text-to-speech system that can clone voices.
[S2] That sounds amazing. How does it work?
"""

# Generate audio with both cloned voices
output = model.generate(
    clone_from_text + text_to_generate,
    audio_prompt=clone_from_audio,
    use_torch_compile=True,
    verbose=True
)

model.save_audio("multiple_cloned_voices.mp3", output)
```

## Creating a Voice Cloning Function

A reusable function for voice cloning:

```python
from dia.model import Dia
from typing import Union, Optional
import numpy as np
import torch

def generate_with_voice_cloning(
    model: Dia,
    reference_text: str,
    reference_audio: Union[str, np.ndarray, torch.Tensor],
    new_text: str,
    temperature: float = 1.0,
    top_p: float = 0.95,
    use_compile: bool = True
) -> np.ndarray:
    """
    Generate speech using voice cloning.
    
    Args:
        model: Initialized Dia model
        reference_text: Transcript matching the reference audio
        reference_audio: Path to audio file or audio array
        new_text: New text to generate with cloned voice
        temperature: Sampling temperature
        top_p: Nucleus sampling parameter
        use_compile: Whether to use torch.compile
        
    Returns:
        np.ndarray: Generated audio array
    """
    # Combine reference and new text
    combined_text = reference_text + new_text
    
    # Generate with voice cloning
    output = model.generate(
        combined_text,
        audio_prompt=reference_audio,
        temperature=temperature,
        top_p=top_p,
        use_torch_compile=use_compile,
        verbose=True
    )
    
    return output

# Usage example
model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")

# Clone a voice and generate new speech
audio = generate_with_voice_cloning(
    model=model,
    reference_text="[S1] This is my reference voice.",
    reference_audio="my_voice.mp3",
    new_text="[S1] This is the new text I want to generate with my voice."
)

model.save_audio("cloned_output.mp3", audio)
```

## Voice Cloning with Audio Preprocessing

If your reference audio needs preprocessing:

```python
import soundfile as sf
import numpy as np
from dia.model import Dia

# Load and preprocess the reference audio
audio_data, sample_rate = sf.read("original_reference.wav")

# Example preprocessing: trim silence, normalize volume, etc.
# This is a simple example - you might want more sophisticated processing
def preprocess_audio(audio: np.ndarray) -> np.ndarray:
    # Normalize audio to [-1, 1] range
    return audio / max(abs(audio.max()), abs(audio.min()))

processed_audio = preprocess_audio(audio_data)

# Save the processed audio for reference
sf.write("processed_reference.wav", processed_audio, sample_rate)

# Load the model
model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")

# Reference transcript
reference_text = "[S1] This is my reference voice that has been preprocessed."

# New text to generate
new_text = "[S1] This new text will sound like the preprocessed reference voice."

# Generate with the preprocessed audio
output = model.generate(
    reference_text + new_text,
    audio_prompt=processed_audio,  # Pass the preprocessed audio array directly
    use_torch_compile=True,
    verbose=True
)

model.save_audio("cloned_from_processed.mp3", output)
```

## Batch Voice Cloning

When you need to generate multiple outputs using the same reference voice:

```python
from dia.model import Dia
import numpy as np

model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")

# Reference voice information
reference_text = "[S1] This is the reference voice I want to use."
reference_audio = "reference.mp3"

# Multiple new texts to generate with the cloned voice
new_texts = [
    "[S1] This is the first sentence with the cloned voice.",
    "[S1] This is the second sentence with the cloned voice.",
    "[S1] This is the third sentence with the cloned voice."
]

# Combine reference text with each new text
combined_texts = [reference_text + new_text for new_text in new_texts]

# Create a list of audio prompts (same reference for all)
audio_prompts = [reference_audio] * len(new_texts)

# Generate all outputs in a batch
batch_outputs = model.generate_batch(
    texts=combined_texts,
    audio_prompts=audio_prompts,
    use_torch_compile=True,
    verbose=True
)

# Save each output
for i, output in enumerate(batch_outputs):
    model.save_audio(f"cloned_batch_{i}.mp3", output)
```
