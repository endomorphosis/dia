import { WebSocket } from 'ws';
import { DiaModel } from '../audio'; // Assuming this is the interface to interact with the Dia model
import { AudioStreamRequest, AudioStreamResponse } from '../../../shared/src/types/messages';

const diaModel = new DiaModel();

export class AudioStream {
    private ws: WebSocket;

    constructor(ws: WebSocket) {
        this.ws = ws;
        this.setupListeners();
    }

    private setupListeners() {
        this.ws.on('message', this.handleMessage.bind(this));
    }

    private async handleMessage(message: string) {
        const request: AudioStreamRequest = JSON.parse(message);
        
        if (request.type === 'start') {
            await this.startStreaming(request);
        } else if (request.type === 'stop') {
            this.stopStreaming();
        }
    }

    private async startStreaming(request: AudioStreamRequest) {
        // Logic to start streaming audio data from the Dia model
        const audioData = await diaModel.streamAudio(request.parameters);
        this.ws.send(JSON.stringify({ type: 'audio', data: audioData }));
    }

    private stopStreaming() {
        // Logic to stop streaming audio data
        diaModel.stopAudioStream();
        this.ws.send(JSON.stringify({ type: 'stop', message: 'Streaming stopped' }));
    }
}