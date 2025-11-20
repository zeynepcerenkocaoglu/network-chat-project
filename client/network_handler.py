#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Network Handler Module
Client tarafında network işlemlerini yönetir
"""

import socket
import threading
from common.protocol import Message, send_message, receive_message, create_message
from common.config import MESSAGE_TYPE_SYSTEM


class NetworkHandler:
    """Client için network işlemlerini yöneten sınıf"""
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self.running = False
        self.receiver_thread = None
        self.message_callback = None  # Mesaj geldiğinde çağrılacak fonksiyon
    
    def connect(self, nickname):
        """
        Server'a bağlan
        Returns:
            (bool, str): (başarılı_mı, mesaj)
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            
            # Nickname gönder
            initial_msg = create_message(MESSAGE_TYPE_SYSTEM, content=nickname)
            if not send_message(self.socket, initial_msg):
                return False, "Failed to send nickname"
            
            # Server'dan onay bekle
            response = receive_message(self.socket)
            if not response:
                return False, "No response from server"
            
            if response.type == MESSAGE_TYPE_SYSTEM and "Connected as" in response.content:
                self.connected = True
                return True, response.content
            else:
                return False, response.content
        
        except ConnectionRefusedError:
            return False, "Connection refused. Is server running?"
        except Exception as e:
            return False, f"Connection error: {e}"
    
    def disconnect(self):
        """Server'dan ayrıl"""
        if self.connected:
            try:
                # EXIT mesajı gönder
                exit_msg = create_message(MESSAGE_TYPE_SYSTEM, content="EXIT")
                send_message(self.socket, exit_msg)
            except:
                pass
        
        self.running = False
        self.connected = False
        
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
    
    def start_receiver(self, callback):
        """
        Mesaj alma thread'ini başlat
        Args:
            callback: Mesaj geldiğinde çağrılacak fonksiyon (message)
        """
        self.message_callback = callback
        self.running = True
        self.receiver_thread = threading.Thread(target=self._receive_messages, daemon=True)
        self.receiver_thread.start()
    
    def _receive_messages(self):
        """Mesajları dinle (thread içinde çalışır)"""
        while self.running and self.connected:
            try:
                message = receive_message(self.socket)
                if not message:
                    # Bağlantı koptu
                    self.connected = False
                    if self.message_callback:
                        error_msg = create_message(MESSAGE_TYPE_SYSTEM,
                                                  content="Connection lost")
                        self.message_callback(error_msg)
                    break
                
                # Callback fonksiyonunu çağır
                if self.message_callback:
                    self.message_callback(message)
            
            except Exception as e:
                if self.running:
                    print(f"❌ Error receiving message: {e}")
                break
    
    def send_public_message(self, content):
        """Public mesaj gönder"""
        from common.config import MESSAGE_TYPE_PUBLIC
        message = create_message(MESSAGE_TYPE_PUBLIC, content=content)
        return send_message(self.socket, message)
    
    def send_private_message(self, recipient, content):
        """Private mesaj gönder"""
        from common.config import MESSAGE_TYPE_PRIVATE
        message = create_message(MESSAGE_TYPE_PRIVATE, 
                                recipient=recipient, 
                                content=content)
        return send_message(self.socket, message)
    
    def is_connected(self):
        """Bağlantı durumunu döndür"""
        return self.connected