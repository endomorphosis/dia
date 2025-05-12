#!/usr/bin/env python3
"""
Simple client for Dia WebSocket streaming that doesn't require sounddevice.
This connects to the WebSocket server and saves audio to a file without playing it.
"""

import asyncio
import websockets
import json
import base64
import argparse
import os
import numpy as np
import wave
import time
from pathlib import Path

# Default parameters
DEFAULT_SERVER = "ws://localhost:8767"
DEFAULT_TEXT = "[S1] Hello, this is a streaming audio test. [S2] The audio is being generated in real-time and streamed over WebSockets."

async def stream_audio(server_url, text, audio_file=None, save_to=None, timeout=120):
    """
    Stream audio from the WebSocket server
    
    Args:
        server_url: WebSocket server URL
        text: Text to convert to speech
        audio_file: Optional path to audio file for voice cloning
        save_to: Optional path to save the complete audio
        timeout: Connection timeout in seconds
    """
    print(f"Connecting to {server_url}...")
    
    # Initialize variables for audio collection
    sample_rate = 44100  # Default, will be updated from server
    all_audio = np.array([], dtype=np.int16)
    
    # Prepare data for voice cloning if provided
    audio_prompt = None
    if audio_file and os.path.exists(audio_file):
        print(f"Loading voice sample from {audio_file}...")
        with open(audio_file, 'rb') as f:
            audio_data = f.read()
            audio_prompt = base64.b64encode(audio_data).decode('ascii')
    
    try:
        # Connect to WebSocket server with a longer ping timeout
        async with websockets.connect(
            server_url, 
            ping_timeout=timeout,  # Longer timeout for model loading/inference
            ping_interval=30,      # More frequent pings
            close_timeout=10       # Wait a bit for proper closure
        ) as websocket:
            print("Connected to WebSocket server")
            
            # Prepare request
            request = {"text": text}
            if audio_prompt:
                request["audio_prompt"] = audio_prompt
            
            # Send request
            await websocket.send(json.dumps(request))
            print(f"Sent text: {text[:50]}...")
            print("Waiting for server response (this might take a while for the first generation)...")
            
            # Receive streaming audio
            start_time = time.time()
            last_update = start_time
            
            while True:
                try:
                    # Use wait_for with a timeout to avoid hanging forever
                    response = await asyncio.wait_for(websocket.recv(), timeout=60)
                    
                    # Reset last_update time
                    last_update = time.time()
                    
                    data = json.loads(response)
                    
                    # Check for errors
                    if "error" in data:
                        print(f"Error from server: {data['error']}")
                        break
                    
                    # Check if generation is finished
                    if data.get("finished", False):
                        print("Audio generation complete")
                        break
                    
                    # Process audio chunk
                    if "audio" in data and data["audio"]:
                        # Get sample rate from server
                        sample_rate = data.get("sample_rate", 44100)
                        
                        # Decode base64 audio
                        audio_bytes = base64.b64decode(data["audio"])
                        audio_int16 = np.frombuffer(audio_bytes, dtype=np.int16)
                        
                        # Store for saving
                        all_audio = np.append(all_audio, audio_int16)
                        
                        # Show progress
                        duration = len(all_audio) / sample_rate
                        elapsed = time.time() - start_time
                        print(f"\rReceived {len(all_audio)} samples ({duration:.2f} seconds), elapsed: {elapsed:.2f}s", end="", flush=True)
                
                except asyncio.TimeoutError:
                    current_time = time.time()
                    if current_time - last_update > 90:
                        print(f"\nNo data received for 90 seconds, connection might be stalled")
                        break
                    print("\nWaiting for server response...")
                    continue
                        
                except Exception as e:
                    print(f"\nError during streaming: {e}")
                    break
            
            print("\n")
    
    except Exception as e:
        print(f"Connection error: {e}")
    
    finally:
        # Save complete audio if requested
        if len(all_audio) > 0 and (save_to is not None or len(all_audio) > 0):
            output_path = save_to or "output.wav"
            print(f"Saving audio to {output_path}")
            
            # Save as WAV file
            with wave.open(output_path, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)  # 2 bytes for int16
                wf.setframerate(sample_rate)
                wf.writeframes(all_audio.tobytes())
            
            print(f"Audio saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Dia WebSocket streaming client")
    parser.add_argument("--server", default=DEFAULT_SERVER, help=f"WebSocket server URL (default: {DEFAULT_SERVER})")
    parser.add_argument("--text", default=DEFAULT_TEXT, help="Text to convert to speech")
    parser.add_argument("--audio-file", help="Path to audio file for voice cloning")
    parser.add_argument("--save-to", help="Path to save the complete audio (default: output.wav)")
    parser.add_argument("--timeout", type=int, default=120, help="Connection timeout in seconds")
    
    args = parser.parse_args()
    
    asyncio.run(stream_audio(args.server, args.text, args.audio_file, args.save_to, args.timeout))

if __name__ == "__main__":
    main()
