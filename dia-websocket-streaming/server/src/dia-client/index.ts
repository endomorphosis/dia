import { DiaClient } from './audio';
import { WebSocket } from 'ws';

class DiaWebSocketClient {
    private socket: WebSocket;

    constructor(url: string) {
        this.socket = new WebSocket(url);

        this.socket.onopen = () => {
            console.log('WebSocket connection established');
        };

        this.socket.onmessage = (event) => {
            this.handleMessage(event.data);
        };

        this.socket.onclose = () => {
            console.log('WebSocket connection closed');
        };

        this.socket.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    }

    public sendAudioData(audioData: ArrayBuffer) {
        const encodedData = DiaClient.encodeAudio(audioData);
        this.socket.send(encodedData);
    }

    private handleMessage(data: any) {
        const response = DiaClient.decodeAudio(data);
        // Handle the response from the Dia model
        console.log('Received response:', response);
    }
}

export default DiaWebSocketClient;