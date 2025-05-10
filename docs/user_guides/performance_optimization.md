# Performance Optimization

This guide provides tips and techniques for optimizing the performance of the Dia model during inference.

## Hardware Recommendations

For optimal performance, Dia benefits from the following hardware:

- **GPU**: NVIDIA GPU with at least 8GB VRAM (16GB+ recommended for larger batch sizes)
- **CPU**: 8+ cores recommended for CPU-only inference
- **RAM**: 16GB+ recommended
- **Storage**: Fast SSD for model loading and audio saving

## Device Selection

By default, Dia will use the best available device:

```python
# The model will automatically select the best device (CUDA > MPS > CPU)
model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")
```

You can explicitly specify a device:

```python
# Force CPU usage
model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16", device="cpu")

# Force CUDA usage
model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16", device="cuda")

# Force MPS usage (Apple Silicon)
model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16", device="mps")
```

## PyTorch Compilation

Using PyTorch's compilation features can significantly speed up inference:

```python
# Enable torch.compile for faster inference
output = model.generate(text, use_torch_compile=True, verbose=True)
```

For even more optimization (in scripts, not necessary for standard usage):

```python
torch._inductor.config.coordinate_descent_tuning = True
torch._inductor.config.triton.unique_kernel_names = True
torch._inductor.config.fx_graph_cache = True
```

## Batch Processing

For generating multiple audio outputs, batch processing is more efficient than sequential processing:

```python
from dia.model import Dia

model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")

# List of texts to generate
texts = [
    "[S1] This is the first example.",
    "[S1] This is the second example.",
    "[S1] This is the third example."
]

# Generate all texts in a single batch
outputs = model.generate_batch(texts, use_torch_compile=True)

# Save each output
for i, output in enumerate(outputs):
    model.save_audio(f"output_{i}.mp3", output)
```

## Memory Management

To reduce memory usage:

- Use `compute_dtype="float16"` instead of full precision
- Process shorter text segments when possible
- Clear CUDA cache between large generations:

```python
# For very memory-intensive workflows
import torch
torch.cuda.empty_cache()
```

## Command-line Interface Optimization

When using the CLI, you can optimize performance with flags:

```bash
# Use the CLI with specific device
python cli.py "Your text here" --output output.mp3 --device cuda
```

## Warm-up Inference

For applications requiring low latency, consider running a warm-up inference:

```python
# Warm-up inference to compile and cache operations
_ = model.generate("[S1] Warm-up text.", use_torch_compile=True)

# Now the model is ready for faster subsequent inferences
output = model.generate(actual_text, use_torch_compile=True)
```

## Docker Environment

For consistent performance across deployments, consider using the provided Docker containers:

- `Dockerfile.gpu` - For environments with NVIDIA GPUs
- `Dockerfile.cpu` - For CPU-only environments

## Seed Setting

Setting a fixed seed can ensure reproducible results:

```python
import torch
import random
import numpy as np

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

# Set seed for reproducible results
set_seed(42)

# Now model generations will be deterministic
output = model.generate(text)
```
