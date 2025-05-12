// server/src/config.ts
import dotenv from 'dotenv';

dotenv.config();

const config = {
    websocket: {
        port: process.env.WEBSOCKET_PORT || 8080,
        host: process.env.WEBSOCKET_HOST || 'localhost',
    },
    diaModel: {
        apiUrl: process.env.DIA_MODEL_API_URL || 'http://localhost:5000',
    },
};

export default config;