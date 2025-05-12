import asyncio
import websockets
import json
import logging
import numpy as np
import torch
import base64
import os
import time
from pathlib import Path

from dia.model import Dia

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioStreamer:
    """Handles streaming audio generation from Dia model"""
    
    def __init__(self):
        self.model = None
        self.sample_rate = 44100  # Default, will be updated when model loads
    
    def load_model(self):
        """Lazy loading of the model"""
        if self.model is None:
            logger.info("Loading Dia model...")
            self.model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")
            logger.info("Model loaded successfully")
            self.sample_rate = 44100  # Dia's default sample rate
    
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
            
            # Define chunk size (about 100ms of audio at 44100Hz)
            chunk_size = int(self.sample_rate * 0.1)  # 100ms chunks
            total_chunks = (len(audio) + chunk_size - 1) // chunk_size
            
            logger.info(f"Streaming {total_chunks} chunks of audio")
            
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
                if current_chunk % 10 == 0:
                    logger.info(f"Streamed chunk {current_chunk}/{total_chunks}")
                
                # Small delay to simulate real-time streaming
                await asyncio.sleep(0.05)
            
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
    
    try:
        async for message in websocket:
            try:
                # Parse the incoming message
                data = json.loads(message)
                
                if "text" not in data:
                    await websocket.send(json.dumps({"error": "Missing 'text' field"}))
                    continue
                
                text = data.get("text")
                logger.info(f"Received generation request: {text[:50]}...")
                
                # Handle voice cloning
                audio_prompt = None
                if "audio_prompt" in data and data["audio_prompt"]:
                    logger.info("Processing voice prompt...")
                    audio_data = base64.b64decode(data["audio_prompt"])
                    # Convert to numpy array
                    audio_prompt = np.frombuffer(audio_data, dtype=np.float32)
                
                # Callback to send audio chunks back to client
                async def send_chunk(chunk_data):
                    try:
                        await websocket.send(json.dumps(chunk_data))
                    except Exception as e:
                        logger.error(f"Error sending chunk: {e}")
                
                # Generate audio with streaming
                try:
                    await audio_streamer.generate_streaming(
                        text=text,
                        audio_prompt=audio_prompt,
                        callback=send_chunk
                    )
                    logger.info("Generation completed successfully")
                except Exception as e:
                    logger.error(f"Error during generation: {e}", exc_info=True)
                    await websocket.send(json.dumps({"error": f"Generation error: {str(e)}"}))
                
            except json.JSONDecodeError:
                logger.error("Invalid JSON received")
                await websocket.send(json.dumps({"error": "Invalid JSON"}))
            except Exception as e:
                logger.error(f"Error processing message: {e}", exc_info=True)
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
