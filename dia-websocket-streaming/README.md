# Dia WebSocket Streaming

This project demonstrates live audio streaming from the Dia model over a WebSocket connection, designed for conversational AI applications. It consists of a server that handles WebSocket connections and clients that interact with the server to stream audio data.

## Project Structure

The project is organized as follows:

- **server/src/websocket/server.py**: Python WebSocket server implementation for streaming Dia audio
- **web-client.html**: Browser-based client with real-time audio playback
- **simple-client.py**: Python client that can save audio without requiring PortAudio
- **run_server.py**: Script to easily start the WebSocket server

## Getting Started

### Requirements

- Python 3.8+
- PyTorch
- WebSockets support
- 8GB+ RAM (Dia model is loaded into memory)
- Disk space for the Dia model (~6.5GB)

### Quick Start

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install websockets numpy torch torchaudio
   ```

3. Run the server:
   ```bash
   python run_server.py
   ```

4. Open `web-client.html` in your browser to interact with the server

### Alternative TypeScript Implementation

This repository also contains the original TypeScript implementation of the streaming server and client.

#### Prerequisites

- Node.js (version 14 or higher)
- npm (Node package manager)

#### Installation

1. Clone the repository:

   ```
   git clone <repository-url>
   cd dia-websocket-streaming
   ```

2. Install server dependencies:

   ```
   cd server
   npm install
   ```

3. Install client dependencies:

   ```
   cd client
   npm install
   ```

4. Install shared dependencies:

   ```
   cd shared
   npm install
   ```

### Running the Application

#### Python Server and Web Client

1. Run the Python server:
   ```bash
   python run_server.py
   ```

2. Open `web-client.html` in your browser

3. Or use the simple Python client:
   ```bash
   python simple-client.py
   ```

#### TypeScript Server and Client (Original Implementation)

1. Start the server:

   ```
   cd server
   npm start
   ```

2. Start the client:

   ```
   cd client
   npm start
   ```

3. Open your browser and navigate to `http://localhost:3000` to access the client application.

## Usage

### Web Client
- Enter text in the text input area
- (Optional) Upload an audio file for voice cloning
- Click "Generate Speech" to start streaming
- Audio will play in real-time as it's generated

### Simple Python Client
```bash
# Run with default settings
python simple-client.py

# Run with custom text
python simple-client.py --text "[S1] Custom text to convert to speech."

# Run with voice cloning
python simple-client.py --audio-file /path/to/reference.mp3

# Save the generated audio
python simple-client.py --save-to output.wav

# Specify a longer timeout for large generations
python simple-client.py --timeout 300
```

### TypeScript Client
- Use the **Record Button** to start recording audio input.
- The audio will be streamed to the server, processed by the Dia model, and the response will be sent back to the client.
- The **Audio Player** component will play the received audio stream.

## How It Works

1. The client sends a text request to the server (optionally with voice sample)
2. The server loads the Dia model if not already loaded
3. The server generates the complete audio using the Dia model
4. The generated audio is then chunked and streamed back to the client in small fragments
5. The client plays these audio chunks as they arrive, providing a near real-time audio experience

### Voice Cloning

The system supports voice cloning by passing audio samples:

1. In the web client, upload an audio sample before generating
2. With the Python client, use the `--audio-file` parameter
3. The model will adapt its output to match the voice characteristics

### Speaker Swapping

Dia supports multiple speaker voices in the same generation. Use [S1], [S2], etc. tags in your text:

```
[S1] Hello, I'm the first speaker. [S2] And I'm the second speaker with a different voice!
```

## Troubleshooting

- **Long First Generation**: The first audio generation after server startup will be slower as the model needs to be loaded and optimized
- **Connection Timeouts**: Increase the `--timeout` parameter if you experience connection timeouts, especially for longer texts
- **Audio Quality Issues**: Try using shorter texts or making sure your GPU has enough memory for the model
- **Python 3.12 Compatibility**: This project has been updated to work with Python 3.12's asyncio changes

## Performance Considerations

- Audio generation speed depends on your hardware (GPU recommended)
- The server can handle multiple concurrent connections, but performance may vary
- Initial model loading is memory-intensive (~8GB RAM required)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.