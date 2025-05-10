# Non-verbal Sounds Guide

This guide explains how to use non-verbal sound tags with Dia to create more expressive and natural-sounding dialogue.

## Introduction

Non-verbal sounds like laughs, sighs, and coughs add realism and emotion to speech. Dia supports generating these sounds through special tags in your input text.

## Supported Non-verbal Tags

Dia recognizes the following non-verbal tags:

| Tag | Description |
|-----|-------------|
| `(laughs)` | Laughter |
| `(clears throat)` | Throat clearing |
| `(sighs)` | Sighing |
| `(gasps)` | Gasping |
| `(coughs)` | Coughing |
| `(singing)` | Singing voice |
| `(sings)` | Singing voice (alternative) |
| `(mumbles)` | Mumbling/unclear speech |
| `(beep)` | Beep sound |
| `(groans)` | Groaning |
| `(sniffs)` | Sniffing |
| `(claps)` | Clapping |
| `(screams)` | Screaming |
| `(inhales)` | Audible inhalation |
| `(exhales)` | Audible exhalation |
| `(applause)` | Applause sound |
| `(burps)` | Burping |
| `(humming)` | Humming |
| `(sneezes)` | Sneezing |
| `(chuckle)` | Light laughter |
| `(whistles)` | Whistling |

## Using Non-verbal Tags

To insert a non-verbal sound, include the appropriate tag within a speaker's dialogue:

```
[S1] I can't believe you did that! (laughs) That's hilarious.
[S2] (sighs) I know, I know. I wasn't thinking.
```

## Best Practices

1. **Use sparingly**: Too many non-verbal sounds can create unnatural speech or artifacts
2. **Natural placement**: Position tags where they would naturally occur in speech
3. **Context-appropriate**: Choose sounds that match the emotional context of the dialogue
4. **Use exact tags**: Stick to the supported tags listed above; variations may cause unexpected results

## Examples

### Emotional Expression
```python
text = "[S1] That's the funniest story I've ever heard! (laughs) I can't believe it!"
```

### Expression Mixed with Speech
```python
text = "[S1] I've been working all day (sighs) and I'm completely exhausted."
```

### Multiple Non-verbal Sounds
```python
text = "[S1] (clears throat) I'd like to make an announcement. (pauses) We've reached our goal!"
```

### Dialogue with Non-verbal Interaction
```python
text = "[S1] Did you hear about the new policy? [S2] (groans) Not another one."
```

## Troubleshooting

- **Artifacts in audio**: Reduce the number of non-verbal tags or make sure they're from the supported list
- **Missing sounds**: Ensure the tag is correctly formatted with parentheses: `(laughs)` not `[laughs]` or `laughs`
- **Unnatural sounds**: Try different positioning of the tag within the text
- **Poor integration**: Make sure non-verbal sounds fit contextually with the dialogue

## Advanced Usage

Non-verbal sounds can be combined with voice cloning for more consistent expression across generated content. When using an audio prompt that contains non-verbal sounds, the model will better learn how to reproduce those specific sounds in the speaker's voice.
