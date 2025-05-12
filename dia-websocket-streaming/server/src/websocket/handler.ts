import { WebSocket } from 'ws';
import { AudioRequest, AudioResponse } from '../../shared/src/types/messages';
import { processAudioStream } from '../dia-client/audio';

const audioHandlers: { [key: string]: (ws: WebSocket, data: any) => void } = {};

audioHandlers['audio-stream'] = (ws: WebSocket, data: AudioRequest) => {
    const audioStream = data.audioStream;

    // Process the audio stream using Dia model
    processAudioStream(audioStream)
        .then((response: AudioResponse) => {
            ws.send(JSON.stringify(response));
        })
        .catch((error) => {
            console.error('Error processing audio stream:', error);
            ws.send(JSON.stringify({ error: 'Failed to process audio stream' }));
        });
};

export const handleWebSocketMessage = (ws: WebSocket, message: string) => {
    const parsedMessage = JSON.parse(message);
    const handler = audioHandlers[parsedMessage.type];

    if (handler) {
        handler(ws, parsedMessage.data);
    } else {
        console.warn('No handler for message type:', parsedMessage.type);
    }
};