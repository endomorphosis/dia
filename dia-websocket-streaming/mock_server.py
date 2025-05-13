#!/usr/bin/env python3
"""
Simple WebSocket server that can respond to pings and simulate audio streaming
for testing the web client connection without requiring the Dia model
"""

import asyncio
import websockets
import json
import logging
import numpy as np
import base64
import time
import os
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockAudioStreamer:
    """Mock audio streamer that generates sine waves"""
    
    def __init__(self):
        self.sample_rate = 24000  # Same as Dia's sample rate
    
    async def generate_streaming(self, text, audio_prompt=None, callback=None):
        """
        Generate a simple sine wave audio as a mock
        
        Args:
            text: Input text (not used for mock)
            audio_prompt: Optional audio for voice cloning (not used for mock)
            callback: Async function to call with each audio chunk
        """
        try:
            logger.info(f"Mock generating audio for text: {text[:50]}...")
            
            # Send a preliminary message to let the client know the server is processing
            if callback:
                await callback({
                    "status": "Generating mock audio...",
                    "finished": False
                })
            
            # Generate a simple sine wave
            duration = 3.0  # 3 seconds of audio
            t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
            frequency = 440.0  # A4 note
            amplitude = 0.5
            
            # Generate a sine wave with a slight fade-in and fade-out
            audio = amplitude * np.sin(2 * np.pi * frequency * t)
            
            # Apply fade-in and fade-out (first and last 0.1 seconds)
            fade_samples = int(0.1 * self.sample_rate)
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)
            
            audio[:fade_samples] *= fade_in
            audio[-fade_samples:] *= fade_out
            
            # If no callback, just return the output
            if callback is None:
                return audio
            
            # Define chunk size (about 50ms of audio)
            chunk_size = int(self.sample_rate * 0.05)  # 50ms chunks
            total_chunks = (len(audio) + chunk_size - 1) // chunk_size
            
            logger.info(f"Streaming {total_chunks} chunks of mock audio")
            
            # Stream chunks
            for i in range(0, len(audio), chunk_size):
                chunk = audio[i:i+chunk_size]
                
                # Convert to int16
                int16_audio = (chunk * 32767).astype(np.int16)
                
                # Send the chunk
                await callback({
                    "audio": base64.b64encode(int16_audio.tobytes()).decode('ascii'),
                    "finished": False,
                    "sample_rate": self.sample_rate
                })
                
                # Progress indicator
                current_chunk = i // chunk_size + 1
                if current_chunk % 10 == 0 or current_chunk == 1:
                    logger.info(f"Streamed chunk {current_chunk}/{total_chunks}")
                
                # Very minimal delay
                await asyncio.sleep(0.01)
            
            # Send final completion message
            await callback({
                "audio": "",
                "finished": True,
                "sample_rate": self.sample_rate
            })
            logger.info("Mock audio streaming completed")
            
            return audio
        except Exception as e:
            logger.error(f"Error during mock audio generation: {e}")
            if callback:
                await callback({
                    "error": str(e),
                    "finished": True
                })
            raise

# Global mock audio streamer instance
audio_streamer = MockAudioStreamer()

async def websocket_handler(websocket):
    """Handle WebSocket connections"""
    client_address = websocket.remote_address
    logger.info(f"New connection from {client_address}")
    
    # Send immediate welcome message
    try:
        await websocket.send(json.dumps({"status": "Connected to mock server", "ready": True}))
        logger.info(f"Sent welcome message to {client_address}")
    except Exception as e:
        logger.error(f"Error sending welcome message: {e}")
    
    try:
        async for message in websocket:
            try:
                # Parse the incoming message
                data = json.loads(message)
                
                # Handle ping requests
                if data.get("type") == "ping":
                    logger.info(f"Received ping from {client_address}")
                    await websocket.send(json.dumps({
                        "type": "pong",
                        "timestamp": time.time(),
                        "message": "Mock server is running"
                    }))
                    continue
                
                if "text" not in data:
                    logger.warning(f"Received request without text field from {client_address}")
                    await websocket.send(json.dumps({"error": "Missing 'text' field"}))
                    continue
                
                text = data.get("text")
                logger.info(f"Received generation request from {client_address}: {text[:50]}...")
                
                # Callback to send audio chunks back to client
                async def send_chunk(chunk_data):
                    try:
                        await websocket.send(json.dumps(chunk_data))
                    except Exception as e:
                        logger.error(f"Error sending chunk to {client_address}: {e}")
                
                # Send a message that we're starting processing
                await websocket.send(json.dumps({
                    "status": "Processing request with mock audio generator...",
                    "processing": True
                }))
                
                # Generate audio with streaming
                try:
                    await audio_streamer.generate_streaming(
                        text=text,
                        audio_prompt=None,  # No voice cloning in mock
                        callback=send_chunk
                    )
                    logger.info(f"Mock generation completed successfully for {client_address}")
                except Exception as e:
                    logger.error(f"Error during mock generation for {client_address}: {e}")
                    await websocket.send(json.dumps({
                        "error": f"Mock generation error: {str(e)}",
                        "finished": True
                    }))
                
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON received from {client_address}")
                await websocket.send(json.dumps({"error": "Invalid JSON"}))
            except Exception as e:
                logger.error(f"Error processing message from {client_address}: {e}")
                await websocket.send(json.dumps({"error": f"Processing error: {str(e)}"}))
    
    except websockets.exceptions.ConnectionClosed as e:
        logger.info(f"Connection closed with {client_address}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error with connection {client_address}: {e}")

async def start_server(host="0.0.0.0", port=8767):
    """Start the WebSocket server"""
    server = await websockets.serve(websocket_handler, host, port)
    logger.info(f"Mock WebSocket server running at ws://{host}:{port}")
    return server

if __name__ == "__main__":
    # Start the server with proper asyncio handling
    async def main():
        server = await start_server()
        try:
            # Keep the server running until Ctrl+C
            await asyncio.Future()
        except KeyboardInterrupt:
            logger.info("Server shutting down")
        finally:
            server.close()
            await server.wait_closed()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server shutting down")
