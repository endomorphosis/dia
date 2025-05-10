# Troubleshooting

This guide addresses common issues that users might encounter when working with Dia and provides solutions.

## Model Loading Issues

### Issue: Cannot load model from Hugging Face
```
Error: Couldn't find file xxx.pth in xxx/Dia-1.6B
```

**Solutions:**
1. Check your internet connection
2. Ensure Hugging Face Hub access is not blocked by a firewall
3. Try clearing the Hugging Face cache and redownloading:
   ```bash
   rm -rf ~/.cache/huggingface/
   ```
4. Verify you have disk space available for the model

### Issue: Out of memory when loading model

**Solutions:**
1. Use a lower precision:
   ```python
   model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")
   ```
2. Free up GPU memory before loading
3. Try CPU loading if GPU memory is insufficient:
   ```python
   model = Dia.from_pretrained("nari-labs/Dia-1.6B", device="cpu")
   ```

## Audio Generation Issues

### Issue: Generated audio is too fast or unnaturally paced

**Solutions:**
1. Reduce the length of input text (ideal length is 5-20 seconds worth of audio)
2. Add appropriate punctuation to create natural pauses
3. Balance the dialogue between speakers

### Issue: Audio has artifacts or strange sounds

**Solutions:**
1. Use fewer non-verbal tags
2. Ensure you're only using supported non-verbal tags
3. Make sure speaker tags are properly formatted and alternating
4. Try generating with a different random seed

### Issue: Voice cloning doesn't match reference voice

**Solutions:**
1. Ensure the transcript exactly matches the reference audio
2. Use a reference audio of 5-10 seconds in length
3. Provide clearer reference audio without background noise
4. Check that speaker tags in the transcript match the voices in the audio

## PyTorch Compilation Issues

### Issue: torch.compile errors or warnings

**Solutions:**
1. Update to the latest version of PyTorch
2. Try without compilation first:
   ```python
   output = model.generate(text, use_torch_compile=False)
   ```
3. If on Windows, compilation may have more issues - try CPU inference

### Issue: Slow first-time compilation

**Solution:**
- This is expected behavior. PyTorch needs to compile the model on first use, which can take time. Subsequent runs will be faster.

## Device-Specific Issues

### Issue: MPS (Apple Silicon) errors

**Solutions:**
1. Ensure you have PyTorch 2.0+ installed with MPS support
2. Try using CPU instead if MPS is unstable:
   ```python
   model = Dia.from_pretrained("nari-labs/Dia-1.6B", device="cpu")
   ```

### Issue: CUDA out of memory errors

**Solutions:**
1. Reduce batch size if using batch processing
2. Use a shorter input text
3. Clear CUDA cache between runs:
   ```python
   import torch
   torch.cuda.empty_cache()
   ```
4. Use `compute_dtype="float16"` for reduced memory usage

## CLI and Gradio UI Issues

### Issue: Gradio UI doesn't start

**Solutions:**
1. Make sure all dependencies are installed:
   ```bash
   pip install -e .
   ```
2. Check for port conflicts and try a different port:
   ```bash
   python app.py --port 8080
   ```

### Issue: CLI errors with audio saving

**Solutions:**
1. Ensure the output directory exists and is writable
2. Check that SoundFile and its dependencies are correctly installed

## Getting Additional Help

If you continue to experience issues:

1. Check the GitHub issues page: [https://github.com/nari-labs/dia/issues](https://github.com/nari-labs/dia/issues)
2. Join the Discord community for help: [Discord Link](https://discord.gg/gcMTW7XA)
3. Create a minimal reproducible example when reporting issues
