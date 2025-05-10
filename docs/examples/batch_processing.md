# Batch Processing Example

This example demonstrates how to efficiently generate multiple audio outputs using Dia's batch processing capabilities.

## Basic Batch Processing

```python
from dia.model import Dia

# Load the model
model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")

# Create a list of texts to generate
texts = [
    "[S1] This is the first example text for batch processing.",
    "[S1] Here's a second example with different content.",
    "[S1] And this is the third example with yet another message."
]

# Generate all texts in a single batch
outputs = model.generate_batch(
    texts=texts,
    use_torch_compile=True,
    verbose=True
)

# Save each output separately
for i, output in enumerate(outputs):
    model.save_audio(f"batch_output_{i}.mp3", output)
```

## Batch Processing with Different Parameters

Generate multiple outputs with different generation parameters:

```python
from dia.model import Dia
import torch

# Ensure reproducible results
torch.manual_seed(42)

# Load the model
model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")

# Same text but with different temperature settings
base_text = "[S1] This is an example of batch processing with different temperature settings."
texts = [base_text] * 3  # Create 3 copies of the same text

# Generate with different temperature settings
outputs = []
temperatures = [0.5, 1.0, 1.5]  # Low, medium, high temperatures

for i, temp in enumerate(temperatures):
    output = model.generate(
        text=texts[i],
        temperature=temp,
        use_torch_compile=True,
        verbose=True
    )
    outputs.append(output)
    model.save_audio(f"temp_{temp}_output.mp3", output)

print(f"Generated {len(outputs)} audio samples with different temperatures")
```

## Batch Processing with Voice Cloning

Clone multiple voices and generate content for each:

```python
from dia.model import Dia

# Load the model
model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")

# Define reference voices and their transcripts
voice_references = [
    {
        "text": "[S1] This is the first reference voice.",
        "audio": "reference_voice_1.mp3"
    },
    {
        "text": "[S1] This is the second reference voice.",
        "audio": "reference_voice_2.mp3"
    },
    {
        "text": "[S1] This is the third reference voice.",
        "audio": "reference_voice_3.mp3"
    }
]

# Text to generate with each voice
new_text = "[S1] This is a demonstration of batch voice cloning with Dia."

# Prepare inputs for batch generation
batch_texts = []
batch_audio_prompts = []

for ref in voice_references:
    # Combine reference transcript and new text
    batch_texts.append(ref["text"] + new_text)
    # Add reference audio
    batch_audio_prompts.append(ref["audio"])

# Generate all outputs in a batch
outputs = model.generate_batch(
    texts=batch_texts,
    audio_prompts=batch_audio_prompts,
    use_torch_compile=True,
    verbose=True
)

# Save each output
for i, output in enumerate(outputs):
    model.save_audio(f"voice_clone_batch_{i}.mp3", output)
```

## Processing Long Text in Batches

Split long text into chunks and process them in batches:

```python
from dia.model import Dia
import re

# Load the model
model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")

# Long text to be processed in chunks
long_text = """
[S1] This is a very long piece of text that would be better processed in chunks.
[S2] Breaking it into smaller segments will improve the quality of the generated speech.
[S1] Each chunk should be a reasonable length, approximately 5-20 seconds of audio.
[S2] We can split the text at natural boundaries like sentence endings.
[S1] Then we can process each chunk separately and combine the results if needed.
[S2] This approach helps maintain natural pacing and intonation throughout the speech.
[S1] It's especially important for long-form content like audiobooks or podcasts.
[S2] The quality will be much better than trying to generate everything at once.
"""

# Function to split text into chunks at speaker transitions
def split_into_chunks(text, max_chunks=None):
    # Split at speaker tags
    pattern = r'(\[S[12]\])'
    parts = re.split(pattern, text)
    
    # Recombine into complete chunks with speaker tags
    chunks = []
    current_chunk = ""
    
    for i in range(0, len(parts)):
        if parts[i].startswith('[S'):
            # Start of new speaker section
            if i > 0 and current_chunk:
                chunks.append(current_chunk)
                if max_chunks and len(chunks) >= max_chunks:
                    break
                current_chunk = parts[i]
            else:
                current_chunk = parts[i]
        else:
            # Content after speaker tag
            current_chunk += parts[i]
    
    # Add the last chunk if it exists
    if current_chunk and (not max_chunks or len(chunks) < max_chunks):
        chunks.append(current_chunk)
    
    return chunks

# Split the long text into chunks
text_chunks = split_into_chunks(long_text)
print(f"Split text into {len(text_chunks)} chunks")

# Process each chunk
outputs = model.generate_batch(
    texts=text_chunks,
    use_torch_compile=True,
    verbose=True
)

# Save each chunk as a separate audio file
for i, output in enumerate(outputs):
    model.save_audio(f"long_text_chunk_{i}.mp3", output)
```

## Batching with CPU/GPU Memory Optimization

Optimize batch size based on available memory:

```python
from dia.model import Dia
import torch
import gc

def determine_optimal_batch_size(model, text_example, start_size=8, min_size=1):
    """Find the largest batch size that fits in memory"""
    batch_size = start_size
    
    while batch_size >= min_size:
        try:
            # Create batch of identical texts for testing
            test_batch = [text_example] * batch_size
            
            # Try to process this batch size
            _ = model.generate_batch(
                texts=test_batch,
                max_new_tokens=128,  # Small value for testing
                use_torch_compile=False  # Skip compilation for test
            )
            
            # If we get here, the batch size works
            print(f"Determined optimal batch size: {batch_size}")
            return batch_size
            
        except RuntimeError as e:
            if "out of memory" in str(e).lower():
                # Free memory and try a smaller batch size
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                gc.collect()
                
                batch_size = batch_size // 2
                print(f"Reducing batch size to {batch_size}")
            else:
                # If error is not memory-related, raise it
                raise
    
    # If we got here, even the minimum batch size doesn't work
    raise RuntimeError("Could not find a working batch size")

# Load model
model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")

# Find optimal batch size for your hardware
sample_text = "[S1] This is a test sentence for determining batch size."
optimal_batch_size = determine_optimal_batch_size(model, sample_text)

# Your actual texts to process
all_texts = [
    f"[S1] This is text number {i} for batch processing."
    for i in range(1, 21)  # 20 texts total
]

# Process in optimal-sized batches
all_outputs = []

for i in range(0, len(all_texts), optimal_batch_size):
    batch = all_texts[i:i+optimal_batch_size]
    print(f"Processing batch {i//optimal_batch_size + 1} with {len(batch)} texts")
    
    outputs = model.generate_batch(
        texts=batch,
        use_torch_compile=True,
        verbose=True
    )
    
    all_outputs.extend(outputs)
    
    # Free memory after each batch
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    gc.collect()

# Save all outputs
for i, output in enumerate(all_outputs):
    model.save_audio(f"optimized_batch_output_{i}.mp3", output)
```
