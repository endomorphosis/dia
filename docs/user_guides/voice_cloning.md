# Voice Cloning Guide

This guide explains how to use Dia's voice cloning capabilities to generate audio that matches a specific voice.

## Overview

Voice cloning allows you to condition Dia's output to match the voice characteristics of a reference audio sample. This can help maintain consistency across multiple generations.

## Basic Voice Cloning Process

1. Provide a reference audio file (the voice to be cloned)
2. Provide the transcript of the reference audio
3. Append your new text to generate with the cloned voice

## Requirements for Voice Cloning

### Reference Audio:
- **Duration**: 5-10 seconds is optimal for best results
- **Quality**: Clear audio without background noise works best
- **Format**: MP3, WAV, or other common audio formats

### Transcript:
- Must accurately match the reference audio
- Must use correct speaker tags (`[S1]`, `[S2]`) if applicable
- Should be formatted exactly as described in the [Text Formatting Guide](./text_formatting.md)

## Example Code

```python
from dia.model import Dia

# Load the model
model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")

# Define the transcript matching your reference audio file
clone_from_text = "[S1] This is the transcript of my reference audio file."
clone_from_audio = "reference_voice.mp3"  # Path to your reference audio file

# Text you want to generate with the cloned voice
text_to_generate = "[S1] This is new text that will sound like the reference voice."

# Generate audio with voice cloning
output = model.generate(
    clone_from_text + text_to_generate,  # Concatenate reference transcript with new text
    audio_prompt=clone_from_audio,       # Provide the reference audio file
    use_torch_compile=True,
    verbose=True
)

# Save the generated audio - will only contain the new text
model.save_audio("cloned_voice_output.mp3", output)
```

## Multiple Speakers

When cloning multiple voices:

1. Make sure your reference audio contains clear examples of both speakers
2. Ensure your transcript accurately labels each speaker with the correct tag
3. Keep the same speaker order in your generation text

### Example with Multiple Speakers:

```python
# Reference audio contains two speakers
clone_from_text = "[S1] Hello, how are you? [S2] I'm doing great, thanks for asking!"
clone_from_audio = "two_speakers.mp3"

# Generation text maintains the speaker order
text_to_generate = "[S1] What are your plans for today? [S2] I'm going to the park."

output = model.generate(
    clone_from_text + text_to_generate,
    audio_prompt=clone_from_audio,
    use_torch_compile=True,
    verbose=True
)
```

## Best Practices

1. **Match transcript precisely**: The transcript must match the reference audio exactly
2. **Optimal reference length**: 5-10 seconds provides enough data without being too long
3. **Speaker consistency**: Keep speaker tags consistent between reference and generation
4. **Clear audio**: Use high-quality reference audio without background noise
5. **Varied content**: Reference audio with varied intonation provides better cloning results

## Troubleshooting

- If cloned voice doesn't match the reference, check that your transcript matches the audio precisely
- If you notice artifacts, try using a cleaner reference audio sample
- If voice style doesn't transfer, try using a longer reference sample (but not exceeding ~15 seconds)
