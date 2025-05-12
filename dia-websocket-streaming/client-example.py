#!/usr/bin/env python3
"""
Example client for Dia WebSocket streaming.
This connects to the WebSocket server and streams audio in real-time.
"""

import asyncio
import websockets
import json
import base64
import argparse
import os
import numpy as np
import sounddevice as sd
from pathlib import Path

# Default parameters
DEFAULT_SERVER = "ws://localhost:8765"
DEFAULT_TEXT = "[S1] Hello, this is a streaming audio test. [S2] The audio is being generated in real-time and streamed over WebSockets."

async def stream_audio(server_url, text, audio_file=None, save_to=None):
    """
    Stream audio from the WebSocket server
    
    Args:
        server_url: WebSocket server URL
        text: Text to convert to speech
        audio_file: Optional path to audio file for voice cloning
        save_to: Optional path to save the complete audio
    """
    print(f"Connecting to {server_url}...")
    
    # Prepare data for voice cloning if provided
    audio_prompt = None
    if audio_file and os.path.exists(audio_file):
        print(f"Loading voice sample from {audio_file}...")
        with open(audio_file, 'rb') as f:
            audio_data = f.read()
            audio_prompt = base64.b64encode(audio_data).decode('ascii')
    
    # Connect to WebSocket server
    async with websockets.connect(server_url) as websocket:
        print("Connected to WebSocket server")
        
        # Prepare request
        request = {"text": text}
        if audio_prompt:
            request["audio_prompt"] = audio_prompt
        
        # Send request
        await websocket.send(json.dumps(request))
        print(f"Sent text: {text[:50]}...")
        
        # Initialize variables for audio playback
        sample_rate = 44100  # Default, will be updated from server
        all_audio = np.array([], dtype=np.float32)
        stream = None
        
        # Receive streaming audio
        while True:
            try:
                response = await websocket.recv()
                data = json.loads(response)
                
                # Check for errors
                if "error" in data:
                    print(f"Error: {data['error']}")
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
                    
                    # Convert to float32 for playback
                    audio_float32 = audio_int16.astype(np.float32) / 32767.0
                    
                    # Initialize audio stream if not already done
                    if stream is None:
                        stream = sd.OutputStream(
                            samplerate=sample_rate,
                            channels=1,
                            dtype='float32',
                            callback=lambda *args: None
                        )
                        stream.start()
                    
                    # Play the audio chunk
                    sd.play(audio_float32, sample_rate, blocking=False)
                    
                    # Store for saving if needed
                    all_audio = np.append(all_audio, audio_float32)
            
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed")
                break
            except Exception as e:
                print(f"Error: {e}")
                break
        
        # Close the audio stream
        if stream:
            stream.stop()
            stream.close()
        
        # Save complete audio if requested
        if save_to and len(all_audio) > 0:
            try:
                import soundfile as sf
                sf.write(save_to, all_audio, sample_rate)
                print(f"Saved complete audio to {save_to}")
            except Exception as e:
                print(f"Error saving audio: {e}")

def main():
    parser = argparse.ArgumentParser(description="Dia WebSocket Streaming Client")
    parser.add_argument("--server", default=DEFAULT_SERVER, help=f"WebSocket server URL (default: {DEFAULT_SERVER})")
    parser.add_argument("--text", default=DEFAULT_TEXT, help="Text to convert to speech")
    parser.add_argument("--voice", help="Path to audio file for voice cloning")
    parser.add_argument("--save", help="Path to save the complete audio")
    args = parser.parse_args()
    
    try:
        # Install required packages if needed
        try:
            import sounddevice
            import soundfile
        except ImportError:
            print("Installing required packages...")
            import pip
            pip.main(["install", "sounddevice", "soundfile"])
        
        # Run the async client
        asyncio.run(stream_audio(args.server, args.text, args.voice, args.save))
    
    except KeyboardInterrupt:
        print("\nClient stopped")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
