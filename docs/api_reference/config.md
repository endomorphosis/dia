# Dia Configuration API

This document describes the configuration classes used in Dia, which control model architecture, data processing, and inference parameters.

## Configuration Hierarchy

The configuration system in Dia follows a hierarchical structure, with `DiaConfig` as the main configuration class that contains instances of specialized configuration classes.

## `DataConfig` Class

```python
class DataConfig(BaseModel, frozen=True):
    """Configuration for data loading and preprocessing."""

    text_length: int                  # Maximum length of text sequences (multiple of 128)
    audio_length: int                 # Maximum length of audio sequences (multiple of 128)
    channels: int = 9                 # Number of audio channels
    text_pad_value: int = 0           # Value used for padding text sequences
    audio_eos_value: int = 1024       # Value representing the end of audio sequences
    audio_pad_value: int = 1025       # Value used for padding audio sequences
    audio_bos_value: int = 1026       # Value representing the beginning of audio sequences
    delay_pattern: list[int] = [0, 8, 9, 10, 11, 12, 13, 14, 15]  # Delay values for each audio channel
```

## `EncoderConfig` Class

```python
class EncoderConfig(BaseModel, frozen=True):
    """Configuration for the encoder module."""

    embedding_size: int               # Size of token embeddings
    hidden_size: int                  # Size of hidden layers
    intermediate_size: int            # Size of intermediate feed-forward layers
    num_hidden_layers: int            # Number of transformer layers
    num_attention_heads: int          # Number of attention heads
    hidden_dropout_prob: float = 0.1  # Probability of dropout in hidden layers
    attention_probs_dropout_prob: float = 0.1  # Probability of dropout in attention
    max_position_embeddings: int      # Maximum sequence length for position embeddings
    vocab_size: int                   # Size of the vocabulary
    layer_norm_eps: float = 1e-12     # Epsilon for layer normalization
    pad_token_id: int = 0             # ID of padding token
```

## `DecoderConfig` Class

```python
class DecoderConfig(BaseModel, frozen=True):
    """Configuration for the decoder module."""

    embedding_size: int               # Size of token embeddings
    hidden_size: int                  # Size of hidden layers
    intermediate_size: int            # Size of intermediate feed-forward layers
    num_hidden_layers: int            # Number of transformer layers
    num_attention_heads: int          # Number of attention heads
    hidden_dropout_prob: float = 0.1  # Probability of dropout in hidden layers
    attention_probs_dropout_prob: float = 0.1  # Probability of dropout in attention
    max_position_embeddings: int      # Maximum sequence length for position embeddings
    vocab_size: int                   # Size of the vocabulary
    layer_norm_eps: float = 1e-12     # Epsilon for layer normalization
    cross_attention: bool = True      # Whether to use cross-attention
    pad_token_id: int = 1025          # ID of padding token
```

## `ModelConfig` Class

```python
class ModelConfig(BaseModel, frozen=True):
    """Configuration combining encoder and decoder settings."""

    encoder: EncoderConfig            # Encoder configuration
    decoder: DecoderConfig            # Decoder configuration
```

## `TrainingConfig` Class

```python
class TrainingConfig(BaseModel, frozen=True):
    """Configuration for training hyperparameters."""

    learning_rate: float = 1e-4       # Learning rate
    weight_decay: float = 0.01        # Weight decay coefficient
    warmup_steps: int = 10000         # Number of warmup steps
    max_steps: int = 100000           # Maximum number of training steps
    batch_size: int = 32              # Training batch size
    gradient_accumulation_steps: int = 1  # Number of steps for gradient accumulation
    log_every: int = 10               # Log frequency (steps)
    save_every: int = 1000            # Checkpoint save frequency (steps)
    eval_every: int = 1000            # Evaluation frequency (steps)
```

## `DiaConfig` Class

```python
class DiaConfig(BaseModel, frozen=True):
    """Master configuration combining all components."""

    data: DataConfig                  # Data processing configuration
    model: ModelConfig                # Model architecture configuration
    training: TrainingConfig          # Training hyperparameters

    @classmethod
    def from_pretrained(cls, model_id: str) -> "DiaConfig":
        """
        Load configuration from a pretrained model on HuggingFace Hub or local path.
        
        Args:
            model_id: HuggingFace Hub ID or local path
            
        Returns:
            DiaConfig: Loaded configuration
        """
        pass

    @classmethod
    def load(cls, path: str) -> "DiaConfig":
        """
        Load configuration from a local file.
        
        Args:
            path: Path to config JSON file
            
        Returns:
            DiaConfig: Loaded configuration
        """
        pass

    def save(self, path: str) -> None:
        """
        Save configuration to a local file.
        
        Args:
            path: Path to save config JSON file
        """
        pass
```

## Usage Examples

### Loading Configuration from Pretrained Model

```python
from dia.config import DiaConfig

# Load configuration from HuggingFace Hub
config = DiaConfig.from_pretrained("nari-labs/Dia-1.6B")
```

### Creating Custom Configuration

```python
from dia.config import DiaConfig, DataConfig, ModelConfig, EncoderConfig, DecoderConfig, TrainingConfig

# Create encoder config
encoder_config = EncoderConfig(
    embedding_size=512,
    hidden_size=512,
    intermediate_size=2048,
    num_hidden_layers=12,
    num_attention_heads=8,
    max_position_embeddings=2048,
    vocab_size=8192
)

# Create decoder config
decoder_config = DecoderConfig(
    embedding_size=512,
    hidden_size=512,
    intermediate_size=2048,
    num_hidden_layers=12,
    num_attention_heads=8,
    max_position_embeddings=2048,
    vocab_size=1027
)

# Create model config
model_config = ModelConfig(encoder=encoder_config, decoder=decoder_config)

# Create data config
data_config = DataConfig(text_length=1024, audio_length=2048)

# Create training config
training_config = TrainingConfig()

# Create main config
config = DiaConfig(
    data=data_config,
    model=model_config,
    training=training_config
)
```
