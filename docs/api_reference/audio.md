# Audio Processing API

This document provides details about the audio processing utilities in Dia, which are primarily responsible for handling audio token sequences and applying channel-specific delays.

## Core Functions

### `build_delay_indices`

```python
def build_delay_indices(
    B: int,
    T: int,
    C: int,
    delay_pattern: typing.List[int]
) -> typing.Tuple[torch.Tensor, torch.Tensor]
```

Creates indices for implementing audio delay pattern across channels.

**Parameters:**
- `B`: Batch size
- `T`: Sequence length
- `C`: Number of channels
- `delay_pattern`: List of delay values for each audio channel

**Returns:**
- Tuple of tensors: `(t_idx_BxTxC, indices_BTCx3)` for use with `apply_audio_delay`

### `apply_audio_delay`

```python
def apply_audio_delay(
    audio_BxTxC: torch.Tensor,
    pad_value: int,
    bos_value: int,
    precomp: typing.Tuple[torch.Tensor, torch.Tensor]
) -> torch.Tensor
```

Applies the delay pattern to batched audio tokens.

**Parameters:**
- `audio_BxTxC`: Audio token tensor of shape [batch, time, channels]
- `pad_value`: Value to use for padding
- `bos_value`: Value to use for beginning-of-sequence
- `precomp`: Precomputed indices from `build_delay_indices`

**Returns:**
- Tensor with delays applied

### `build_revert_indices`

```python
def build_revert_indices(
    B: int,
    T: int,
    C: int,
    delay_pattern: typing.List[int]
) -> typing.Tuple[torch.Tensor, torch.Tensor]
```

Creates indices for reverting the delay pattern.

**Parameters:**
- `B`: Batch size
- `T`: Sequence length
- `C`: Number of channels
- `delay_pattern`: List of delay values for each audio channel

**Returns:**
- Tuple of tensors for use with `revert_audio_delay`

### `revert_audio_delay`

```python
def revert_audio_delay(
    audio_BxTxC: torch.Tensor,
    precomp: typing.Tuple[torch.Tensor, torch.Tensor]
) -> torch.Tensor
```

Reverts the channel-specific delay pattern from audio tokens.

**Parameters:**
- `audio_BxTxC`: Audio token tensor with delays
- `precomp`: Precomputed indices from `build_revert_indices`

**Returns:**
- Tensor with delays reverted

## Usage Example

```python
import torch
from dia.audio import build_delay_indices, apply_audio_delay, build_revert_indices, revert_audio_delay

# Setup parameters
batch_size = 2
seq_length = 1024
channels = 9
delay_pattern = [0, 8, 9, 10, 11, 12, 13, 14, 15]  # Standard Dia pattern

# Create sample audio tokens
audio_tokens = torch.randint(0, 1024, (batch_size, seq_length, channels))

# Apply delay pattern
delay_indices = build_delay_indices(batch_size, seq_length, channels, delay_pattern)
delayed_audio = apply_audio_delay(
    audio_tokens,
    pad_value=1025,
    bos_value=1026,
    precomp=delay_indices
)

# Process the delayed audio (e.g., model inference)
processed_audio = delayed_audio  # Placeholder for actual processing

# Revert delay pattern
revert_indices = build_revert_indices(batch_size, seq_length, channels, delay_pattern)
original_audio = revert_audio_delay(processed_audio, precomp=revert_indices)
```

## Implementation Details

The delay pattern implementation uses a technique similar to causal convolution to offset each audio channel by a specific delay. This approach:

1. Preserves causal relationships between tokens
2. Enables the model to learn channel-specific audio features
3. Helps maintain consistency across multiple audio channels

The main workflow in Dia is:
1. Apply delay pattern before feeding audio to the model
2. Revert delay pattern after model generation to get the final result
