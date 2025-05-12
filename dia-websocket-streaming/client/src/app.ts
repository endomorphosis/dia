import React from 'react';
import ReactDOM from 'react-dom';
import AudioPlayer from './components/AudioPlayer';
import Conversation from './components/Conversation';
import RecordButton from './components/RecordButton';

const App = () => {
    return (
        <div>
            <h1>Dia WebSocket Streaming</h1>
            <RecordButton />
            <AudioPlayer />
            <Conversation />
        </div>
    );
};

ReactDOM.render(<App />, document.getElementById('root'));