// This file manages the WebSocket connection from the client to the server, handling sending and receiving messages.

import { useEffect, useRef } from 'react';

const useWebSocket = (url: string) => {
    const socketRef = useRef<WebSocket | null>(null);

    useEffect(() => {
        socketRef.current = new WebSocket(url);

        socketRef.current.onopen = () => {
            console.log('WebSocket connection established');
        };

        socketRef.current.onmessage = (event) => {
            const message = JSON.parse(event.data);
            console.log('Message received:', message);
            // Handle incoming messages here
        };

        socketRef.current.onclose = () => {
            console.log('WebSocket connection closed');
        };

        return () => {
            socketRef.current?.close();
        };
    }, [url]);

    const sendMessage = (message: object) => {
        if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
            socketRef.current.send(JSON.stringify(message));
        } else {
            console.error('WebSocket is not open. Message not sent:', message);
        }
    };

    return { sendMessage };
};

export default useWebSocket;