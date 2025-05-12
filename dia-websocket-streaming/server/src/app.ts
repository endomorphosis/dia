import express from 'express';
import http from 'http';
import WebSocket from 'ws';
import { handleWebSocketConnection } from './websocket/handler';
import { config } from './config';

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

app.use(express.json());

wss.on('connection', (ws) => {
    console.log('New client connected');
    handleWebSocketConnection(ws);
    
    ws.on('close', () => {
        console.log('Client disconnected');
    });
});

server.listen(config.port, () => {
    console.log(`Server is listening on port ${config.port}`);
});