import asyncio
import websockets
import json
import logging
import numpy as np
import torch
import base64
import os
import time
import sys
from pathlib import Path

# Add the parent directory to the Python path to find the dia module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from dia.model import Dia

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioStreamer:
    """Handles streaming audio generation from Dia model"""
    
    def __init__(self):
        self.model = None
        self.sample_rate = 24000  # Dia's default sample rate is 24kHz
    
    def load_model(self):
        """Lazy loading of the model"""
        if self.model is None:
            logger.info("Loading Dia model...")
            self.model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")
            logger.info("Model loaded successfully")
            # Dia model uses 24kHz not 44.1kHz
            self.sample_rate = 24000
    
    async def generate_streaming(self, text, audio_prompt=None, callback=None):
        """
        Generate audio from text with streaming capability
        
        Args:
            text: Input text to convert to speech
            audio_prompt: Optional audio for voice cloning (file path or array)
            callback: Async function to call with each audio chunk
        """
        self.load_model()
        
        try:
            logger.info(f"Generating audio for text: {text[:50]}...")
            
            # Send a preliminary message to let the client know the server is processing
            if callback:
                await callback({
                    "status": "Generating audio...",
                    "finished": False
                })
            
            # Generate audio (Dia doesn't support callbacks, so we need to generate the full audio first)
            logger.info("Starting audio generation")
            generate_start_time = time.time()
            output = self.model.generate(
                text,
                audio_prompt=audio_prompt,
                use_torch_compile=False,  # Try without compilation to avoid issues
                verbose=True
            )
            generate_time = time.time() - generate_start_time
            logger.info(f"Audio generation completed in {generate_time:.2f} seconds")
            
            # If no callback, just return the output
            if callback is None:
                return output
            
            # We need to manually stream the audio in chunks
            # Convert to numpy if it's a torch tensor
            if isinstance(output, torch.Tensor):
                logger.info("Converting torch tensor to numpy array")
                audio = output.squeeze().cpu().numpy()
            else:
                logger.info(f"Output is type: {type(output)}")
                audio = output
            
            logger.info(f"Audio shape: {audio.shape}, dtype: {audio.dtype}")
            
            # Define chunk size (about 50ms of audio at 24000Hz)
            chunk_size = int(self.sample_rate * 0.05)  # 50ms chunks
            total_chunks = (len(audio) + chunk_size - 1) // chunk_size
            
            logger.info(f"Streaming {total_chunks} chunks of audio")
            
            # Stream chunks immediately with minimal delay
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
                
                # Very minimal delay to prevent overwhelming the connection
                # For faster streaming, we're using a much smaller delay
                await asyncio.sleep(0.01)
            
            # Send final completion message
            await callback({
                "audio": "",
                "finished": True,
                "sample_rate": self.sample_rate
            })
            logger.info("Audio streaming completed")
            
            return output
        except Exception as e:
            logger.error(f"Error during audio generation: {e}")
            if callback:
                await callback({
                    "error": str(e),
                    "finished": True
                })
            raise

# Global audio streamer instance
audio_streamer = AudioStreamer()

async def websocket_handler(websocket):
    """Handle WebSocket connections"""
    client_address = websocket.remote_address
    logger.info(f"New connection from {client_address}")
    
    # Send immediate welcome message
    try:
        await websocket.send(json.dumps({"status": "Connected to server", "ready": True}))
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
                        "message": "Server is running"
                    }))
                    continue
                
                if "text" not in data:
                    logger.warning(f"Received request without text field from {client_address}")
                    await websocket.send(json.dumps({"error": "Missing 'text' field"}))
                    continue
                
                text = data.get("text")
                logger.info(f"Received generation request from {client_address}: {text[:50]}...")
                
                # Handle voice cloning
                audio_prompt = None
                if "audio_prompt" in data and data["audio_prompt"]:
                    logger.info(f"Processing voice prompt from {client_address}...")
                    audio_data = base64.b64decode(data["audio_prompt"])
                    # Convert to numpy array
                    audio_prompt = np.frombuffer(audio_data, dtype=np.float32)
                
                # Callback to send audio chunks back to client
                async def send_chunk(chunk_data):
                    try:
                        await websocket.send(json.dumps(chunk_data))
                    except Exception as e:
                        logger.error(f"Error sending chunk to {client_address}: {e}")
                
                # Send a message that we're starting processing
                await websocket.send(json.dumps({
                    "status": "Processing request... This may take a moment for the first request.",
                    "processing": True
                }))
                
                # Generate audio with streaming
                try:
                    await audio_streamer.generate_streaming(
                        text=text,
                        audio_prompt=audio_prompt,
                        callback=send_chunk
                    )
                    logger.info(f"Generation completed successfully for {client_address}")
                except Exception as e:
                    logger.error(f"Error during generation for {client_address}: {e}", exc_info=True)
                    await websocket.send(json.dumps({
                        "error": f"Generation error: {str(e)}",
                        "finished": True
                    }))
                
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON received from {client_address}")
                await websocket.send(json.dumps({"error": "Invalid JSON"}))
            except Exception as e:
                logger.error(f"Error processing message from {client_address}: {e}", exc_info=True)
                await websocket.send(json.dumps({"error": f"Processing error: {str(e)}"}))
    
    except websockets.exceptions.ConnectionClosed as e:
        logger.info(f"Connection closed with {client_address}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error with connection {client_address}: {e}", exc_info=True)

async def start_server(host="0.0.0.0", port=8767):
    """Start the WebSocket server"""
    server = await websockets.serve(websocket_handler, host, port)
    logger.info(f"WebSocket server running at ws://{host}:{port}")
    return server

if __name__ == "__main__":
    # Start the server with proper asyncio handling for Python 3.12
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
