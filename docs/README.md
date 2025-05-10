# Dia Documentation

This directory contains comprehensive documentation for Dia, a 1.6B parameter text-to-speech model created by Nari Labs.

## Table of Contents

- [Overview](#overview)
- [Getting Started](./getting_started.md)
- [User Guides](#user-guides)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Overview

Dia is a specialized text-to-speech model that:

- Directly generates highly realistic dialogue from a transcript
- Supports voice cloning via audio prompts
- Produces nonverbal communications like laughter, coughing, throat clearing, etc.
- Works with multiple speakers via `[S1]` and `[S2]` tags

The model is available on [Hugging Face](https://huggingface.co/nari-labs/Dia-1.6B), and this documentation provides comprehensive guidance on using and extending it.

## User Guides

The [user_guides](./user_guides/) directory contains detailed guides on specific aspects of using Dia:

- [Text Formatting](./user_guides/text_formatting.md) - Rules for formatting input text
- [Voice Cloning](./user_guides/voice_cloning.md) - How to clone voices effectively
- [Non-verbal Sounds](./user_guides/nonverbal_sounds.md) - Working with non-verbal sound tags
- [Performance Optimization](./user_guides/performance_optimization.md) - Tips for optimizing inference speed
- [Troubleshooting](./user_guides/troubleshooting.md) - Solutions to common issues

## API Reference

The [api_reference](./api_reference/) directory contains detailed documentation for the Dia API:

- [Model](./api_reference/model.md) - Main `Dia` class and generation functions
- [Configuration](./api_reference/config.md) - Configuration classes and parameters

## Examples

The [examples](./examples/) directory contains practical code examples:

- [Simple Text to Speech](./examples/simple.md) - Basic usage examples
- [Voice Cloning](./examples/voice_cloning.md) - Voice cloning examples
- [Batch Processing](./examples/batch_processing.md) - Efficient batch generation

## Contributing

We welcome contributions to improve this documentation. Please feel free to submit pull requests for additions, corrections, or clarifications.

## License

This documentation is licensed under the Apache 2.0 License - see the [LICENSE](../LICENSE) file for details.
