# Getting Started with Dia

This guide will help you get started with Dia, a text-to-speech model for dialogue generation.

## Installation

### Using pip

```bash
# Install directly from GitHub
pip install git+https://github.com/nari-labs/dia.git
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/nari-labs/dia.git
cd dia

# Option 1: Using uv
uv run app.py

# Option 2: Using standard Python tools
python -m venv .venv
source .venv/bin/activate
pip install -e .
python app.py
```

## Basic Usage

### Simple Text to Speech

```python
from dia.model import Dia

# Load the model
model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")

# Create dialogue text with speaker tags
text = "[S1] Dia is an open weights text to dialogue model. [S2] You get full control over scripts and voices."

# Generate audio
output = model.generate(text, use_torch_compile=True, verbose=True)

# Save the generated audio
model.save_audio("output.mp3", output)
```

### Voice Cloning

```python
from dia.model import Dia

# Load the model
model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")

# Define the transcript of your reference audio
clone_from_text = "[S1] This is a sample voice I want to clone."
clone_from_audio = "reference_audio.mp3"  # Path to your reference audio file

# Text you want to generate with the cloned voice
text_to_generate = "[S1] Hello, this is text generated with a cloned voice."

# Generate audio with voice cloning
output = model.generate(
    clone_from_text + text_to_generate,
    audio_prompt=clone_from_audio,
    use_torch_compile=True,
    verbose=True
)

# Save the generated audio
model.save_audio("cloned_voice_output.mp3", output)
```

## Using the CLI

Dia provides a command-line interface for generating audio:

```bash
python cli.py "Your dialogue text here" --output output.mp3
```

For more options:

```bash
python cli.py --help
```

## Using the Gradio UI

Dia includes a Gradio-based web interface for easy interaction:

```bash
python app.py
```

This will launch a web interface where you can input text and generate audio.

## Important Notes

- The model generates different voices each time unless you:
  - Add an audio prompt for voice cloning
  - Fix the random seed
- Keep moderate text lengths for best results (≈5-20 seconds)
- Use non-verbal tags sparingly
- Always begin input text with `[S1]` and alternate between `[S1]` and `[S2]` tags

For more detailed instructions, refer to the [User Guides](./user_guides/index.md) section.
