#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run Server
Chat server'ı çalıştırır
"""

import argparse
import signal
import sys
from server import ChatServer


def signal_handler(sig, frame):
    """Ctrl+C handler"""
    print("\n🛑 Interrupt received, shutting down...")
    sys.exit(0)


def main():
    """Ana fonksiyon"""
    # Argümanları parse et
    parser = argparse.ArgumentParser(description='Chat Server - Modular Version')
    parser.add_argument('--host', type=str, default='127.0.0.1',
                       help='Server host address (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000,
                       help='Server port (default: 5000)')
    parser.add_argument('--http-port', type=int, default=8080,
                       help='HTTP server port (default: 8080)')
    parser.add_argument('--ws-port', type=int, default=8765,
                       help='WebSocket server port (default: 8765)')
    
    args = parser.parse_args()
    
    # Signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Server'ı başlat
    try:
        server = ChatServer(
            host=args.host,
            port=args.port,
            http_port=args.http_port,
            ws_port=args.ws_port
        )
        server.start()
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()