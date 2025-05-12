// This file contains functions for processing audio data on the client side, including encoding audio for transmission.

import { AudioData } from '../../shared/src/types/audio';

// Function to encode audio data for transmission
export function encodeAudio(audioBuffer: AudioBuffer): AudioData {
    const channelData = audioBuffer.getChannelData(0);
    const audioData: AudioData = {
        sampleRate: audioBuffer.sampleRate,
        data: new Float32Array(channelData)
    };
    return audioData;
}

// Function to decode audio data received from the server
export function decodeAudio(audioData: AudioData): AudioBuffer {
    const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
    const audioBuffer = audioContext.createBuffer(1, audioData.data.length, audioData.sampleRate);
    audioBuffer.copyToChannel(audioData.data, 0);
    return audioBuffer;
}