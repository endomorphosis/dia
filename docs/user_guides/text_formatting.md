# Text Formatting Guide

Proper text formatting is essential for getting the best results from Dia. This guide covers the rules and best practices for formatting your input text.

## Speaker Tags

Dia uses speaker tags to identify different speakers in the dialogue:

- `[S1]` - First speaker
- `[S2]` - Second speaker

### Rules:

1. **Always begin** your input text with `[S1]`
2. **Always alternate** between `[S1]` and `[S2]` (incorrect example: `[S1]...` followed by `[S1]...`)
3. Speaker tags should be placed at the beginning of each speaker's part of the dialogue

### Example:

```
[S1] Hello, how are you today? 
[S2] I'm doing well, thank you for asking. How about you?
[S1] I'm great! I was wondering if you could help me with something.
[S2] Of course, what do you need help with?
```

## Text Length Guidelines

The length of your input text affects the quality of the generated audio:

- **Too short** (under 5 seconds worth of audio): May sound unnatural
- **Too long** (over 20 seconds worth of audio): May cause speech to be unnaturally fast
- **Optimal length**: Between 5 to 20 seconds worth of audio

For reference, approximately 1 second ≈ 86 tokens.

## Non-verbal Tags

Non-verbal tags allow you to add expression elements like laughing or sighing to your dialogue:

### Format:
```
[S1] That's really funny! (laughs) I didn't expect that at all.
```

### Supported Non-verbal Tags:

- (laughs)
- (clears throat)
- (sighs)
- (gasps)
- (coughs)
- (singing)
- (sings)
- (mumbles)
- (beep)
- (groans)
- (sniffs)
- (claps)
- (screams)
- (inhales)
- (exhales)
- (applause)
- (burps)
- (humming)
- (sneezes)
- (chuckle)
- (whistles)

### Best Practices:

1. Use non-verbal tags **sparingly** - overuse can lead to artifacts
2. Place them within the speaker's dialogue at natural points
3. Stick to the supported tags listed above - unlisted tags may cause unexpected results

## Final Tips

- For better audio quality at the end, place the second-to-last speaker's tag (`[S1]` or `[S2]`) at the end of your script
- Balance the amount of text between speakers for more natural-sounding conversation
- Use punctuation naturally to help guide the model's pacing and intonation
