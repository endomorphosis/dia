import WebSocket from 'ws';
import { handleWebSocketMessage } from './handler';
import { WebSocketConfig } from '../config';

const wss = new WebSocket.Server({ port: WebSocketConfig.port });

wss.on('connection', (ws) => {
    console.log('New client connected');

    ws.on('message', (message) => {
        console.log(`Received message: ${message}`);
        handleWebSocketMessage(ws, message);
    });

    ws.on('close', () => {
        console.log('Client disconnected');
    });
});

console.log(`WebSocket server is running on ws://localhost:${WebSocketConfig.port}`);