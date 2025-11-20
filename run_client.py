#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run Client
Chat client'ı çalıştırır
"""

import argparse
import tkinter as tk
from client import ChatClient


def main():
    """Ana fonksiyon"""
    # Argümanları parse et
    parser = argparse.ArgumentParser(description='Chat Client - Modular Version')
    parser.add_argument('--host', type=str, default='127.0.0.1',
                       help='Server host address (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000,
                       help='Server port (default: 5000)')
    
    args = parser.parse_args()
    
    # Tkinter root
    root = tk.Tk()
    
    # Client'ı başlat
    client = ChatClient(root, server_host=args.host, server_port=args.port)
    
    # GUI loop
    root.mainloop()


if __name__ == "__main__":
    main()