# dia-websocket-streaming

This project demonstrates live audio streaming from the Dia model over a WebSocket connection, designed for conversational AI applications. It consists of a server that handles WebSocket connections and a client that interacts with the server to stream audio data.

## Project Structure

The project is organized into three main directories:

- **server**: Contains the backend implementation, including WebSocket handling and audio processing.
- **client**: Contains the frontend application built with React for user interaction and audio playback.
- **shared**: Contains shared types and interfaces used by both the server and client.

## Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- npm (Node package manager)

### Installation

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

- Use the **Record Button** to start recording audio input.
- The audio will be streamed to the server, processed by the Dia model, and the response will be sent back to the client.
- The **Audio Player** component will play the received audio stream.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.