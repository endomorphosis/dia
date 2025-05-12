#!/usr/bin/env python3
"""
Script to run the Dia WebSocket streaming server
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    # Get the directory of this script
    script_dir = Path(__file__).parent.absolute()
    
    # Check for required packages
    try:
        import websockets
        import torch
        import torchaudio
        import numpy
    except ImportError:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "websockets", "torch", "torchaudio", "numpy"])
    
    # Run the server
    print("Starting Dia WebSocket streaming server on port 8767...")
    server_script = script_dir / "server" / "src" / "websocket" / "server.py"
    
    try:
        subprocess.run([sys.executable, str(server_script)])
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    main()
