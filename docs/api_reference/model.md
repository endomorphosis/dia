# Dia Model API

This document describes the API for the Dia model class, which is the primary interface for generating audio from text.

## `Dia` Class

The `Dia` class is the main interface for text-to-speech generation.

### Class Methods

#### `from_pretrained`

```python
@classmethod
def from_pretrained(
    cls,
    model_id: str,
    compute_dtype: str = "float16",
    device: Optional[Union[str, torch.device]] = None,
    **kwargs
) -> "Dia"
```

Loads a pretrained Dia model from Hugging Face Hub or local files.

**Parameters:**
- `model_id`: Hugging Face repository ID (e.g., "nari-labs/Dia-1.6B") or local path
- `compute_dtype`: Computation data type for model inference ("float16", "float32", "bfloat16")
- `device`: Device to load model on (will use best available if None)
- `**kwargs`: Additional arguments passed to model initialization

**Returns:**
- Initialized `Dia` instance

**Example:**
```python
model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")
```

### Instance Methods

#### `generate`

```python
def generate(
    self,
    text: str,
    audio_prompt: Optional[Union[str, np.ndarray, torch.Tensor]] = None,
    top_p: float = 0.95,
    temperature: float = 1.0,
    top_k: Optional[int] = None,
    sample_rate: int = 44100,
    max_new_tokens: int = 2048,
    use_torch_compile: bool = False,
    cfg_scale: float = 3.0,
    verbose: bool = False,
    callback: Optional[Callable[[int, int], None]] = None
) -> np.ndarray
```

Generates audio from input text.

**Parameters:**
- `text`: Input text string with speaker tags ([S1], [S2])
- `audio_prompt`: Optional audio prompt for voice cloning (file path or array)
- `top_p`: Nucleus sampling parameter (0-1)
- `temperature`: Sampling temperature (0 = greedy, higher = more random)
- `top_k`: Limit sampling to top k tokens (None = no limit)
- `sample_rate`: Output audio sample rate in Hz
- `max_new_tokens`: Maximum number of new tokens to generate
- `use_torch_compile`: Whether to use PyTorch compilation for faster inference
- `cfg_scale`: Classifier-free guidance scale (higher = closer to prompt)
- `verbose`: Print progress information
- `callback`: Optional callback function called during generation

**Returns:**
- NumPy array containing generated audio at specified sample rate

**Example:**
```python
audio = model.generate(
    text="[S1] Hello, how are you? [S2] I'm doing great, thanks!",
    temperature=0.8,
    use_torch_compile=True
)
```

#### `generate_batch`

```python
def generate_batch(
    self,
    texts: List[str],
    audio_prompts: Optional[List[Union[str, np.ndarray, torch.Tensor]]] = None,
    top_p: float = 0.95,
    temperature: float = 1.0,
    top_k: Optional[int] = None,
    sample_rate: int = 44100,
    max_new_tokens: int = 2048,
    use_torch_compile: bool = False,
    cfg_scale: float = 3.0,
    verbose: bool = False
) -> List[np.ndarray]
```

Generates audio for multiple texts in a single batch.

**Parameters:**
- `texts`: List of input text strings
- `audio_prompts`: Optional list of audio prompts (one per text)
- Other parameters are the same as `generate`

**Returns:**
- List of NumPy arrays containing generated audio

**Example:**
```python
audios = model.generate_batch(
    texts=[
        "[S1] This is example one.",
        "[S1] This is example two."
    ],
    temperature=0.8,
    use_torch_compile=True
)
```

#### `save_audio`

```python
def save_audio(
    self,
    path: str,
    audio: np.ndarray,
    sample_rate: int = 44100
) -> None
```

Saves generated audio to a file.

**Parameters:**
- `path`: Output file path (supports .wav, .mp3, etc.)
- `audio`: NumPy array of audio samples
- `sample_rate`: Sample rate of the audio in Hz

**Example:**
```python
model.save_audio("output.mp3", audio)
```

## Utility Functions

The module also contains these utility functions:

### `_get_default_device`

```python
def _get_default_device() -> torch.device
```

Returns the best available device (CUDA > MPS > CPU).

### `_sample_next_token`

```python
def _sample_next_token(
    logits_BCxV: torch.Tensor,
    temperature: float,
    top_p: float,
    top_k: Optional[int],
    audio_eos_value: int
) -> torch.Tensor
```

Internal function that samples the next token during generation.

## Constants

- `DEFAULT_SAMPLE_RATE = 44100`: Default audio sample rate
- `SAMPLE_RATE_RATIO = 512`: Ratio between sample rate and token rate
