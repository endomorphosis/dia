import React, { useEffect, useRef, useState } from 'react';

const AudioPlayer: React.FC<{ streamUrl: string }> = ({ streamUrl }) => {
    const audioRef = useRef<HTMLAudioElement | null>(null);
    const [isPlaying, setIsPlaying] = useState(false);

    useEffect(() => {
        if (audioRef.current) {
            audioRef.current.src = streamUrl;
            audioRef.current.load();
        }
    }, [streamUrl]);

    const handlePlayPause = () => {
        if (audioRef.current) {
            if (isPlaying) {
                audioRef.current.pause();
            } else {
                audioRef.current.play();
            }
            setIsPlaying(!isPlaying);
        }
    };

    return (
        <div>
            <audio ref={audioRef} controls={false} />
            <button onClick={handlePlayPause}>
                {isPlaying ? 'Pause' : 'Play'}
            </button>
        </div>
    );
};

export default AudioPlayer;