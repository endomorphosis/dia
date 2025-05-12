import React, { useEffect, useState } from 'react';
import { sendMessage, receiveMessage } from '../services/websocket-client';

const Conversation: React.FC = () => {
    const [messages, setMessages] = useState<string[]>([]);
    const [input, setInput] = useState<string>('');

    useEffect(() => {
        const handleIncomingMessage = (message: string) => {
            setMessages(prevMessages => [...prevMessages, message]);
        };

        const unsubscribe = receiveMessage(handleIncomingMessage);
        return () => unsubscribe();
    }, []);

    const handleSendMessage = () => {
        if (input.trim()) {
            sendMessage(input);
            setMessages(prevMessages => [...prevMessages, `You: ${input}`]);
            setInput('');
        }
    };

    return (
        <div>
            <div>
                {messages.map((msg, index) => (
                    <div key={index}>{msg}</div>
                ))}
            </div>
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            />
            <button onClick={handleSendMessage}>Send</button>
        </div>
    );
};

export default Conversation;