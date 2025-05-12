// shared/src/types/messages.ts
export interface AudioStreamRequest {
    userId: string;
    audioData: ArrayBuffer;
}

export interface AudioStreamResponse {
    userId: string;
    status: 'success' | 'error';
    message?: string;
    audioData?: ArrayBuffer;
}

export interface ConversationMessage {
    userId: string;
    text: string;
    timestamp: number;
}

export interface ConversationResponse {
    userId: string;
    responses: Array<ConversationMessage>;
}