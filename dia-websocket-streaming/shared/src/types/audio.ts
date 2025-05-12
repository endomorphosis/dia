// This file defines types related to audio data, including interfaces for audio streams and processing parameters.

export interface AudioStream {
    id: string;
    data: Float32Array; // Audio data in Float32 format
    sampleRate: number; // Sample rate of the audio stream
}

export interface AudioProcessingParams {
    volume: number; // Volume level (0.0 to 1.0)
    pitch: number; // Pitch adjustment in semitones
    speed: number; // Speed adjustment (1.0 is normal speed)
}

export interface AudioMessage {
    stream: AudioStream;
    params: AudioProcessingParams;
    timestamp: number; // Timestamp of when the audio was processed
}