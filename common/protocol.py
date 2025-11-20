#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protocol Module
Mesaj gönderme/alma ve protokol fonksiyonları
"""

import json
import socket
from datetime import datetime


class Message:
    """Mesaj sınıfı - tüm mesaj tiplerini temsil eder"""
    
    def __init__(self, msg_type, sender=None, recipient=None, content=None, timestamp=None):
        self.type = msg_type
        self.sender = sender
        self.recipient = recipient
        self.content = content
        self.timestamp = timestamp or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def to_dict(self):
        """Mesajı dictionary'e çevir"""
        return {
            'type': self.type,
            'sender': self.sender,
            'recipient': self.recipient,
            'content': self.content,
            'timestamp': self.timestamp
        }
    
    @staticmethod
    def from_dict(data):
        """Dictionary'den mesaj oluştur"""
        return Message(
            msg_type=data.get('type'),
            sender=data.get('sender'),
            recipient=data.get('recipient'),
            content=data.get('content'),
            timestamp=data.get('timestamp')
        )
    
    def __str__(self):
        return f"Message({self.type}, {self.sender} -> {self.recipient}: {self.content})"


def send_message(sock, message):
    """
    Socket üzerinden mesaj gönder
    Args:
        sock: Socket nesnesi
        message: Message nesnesi veya dict
    """
    try:
        if isinstance(message, Message):
            data = message.to_dict()
        else:
            data = message
        
        json_data = json.dumps(data, ensure_ascii=False)
        sock.sendall(json_data.encode('utf-8') + b'\n')
        return True
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False


def receive_message(sock):
    """
    Socket'ten mesaj al
    Args:
        sock: Socket nesnesi
    Returns:
        Message nesnesi veya None
    """
    try:
        data = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                return None
            data += chunk
            if b'\n' in data:
                break
        
        # Sadece ilk satırı al (ilk \n'e kadar)
        first_line = data.split(b'\n')[0]
        json_str = first_line.decode('utf-8').strip()
        
        if not json_str:
            return None
        
        message_dict = json.loads(json_str)
        return Message.from_dict(message_dict)
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        print(f"❌ Received data: {data[:200]}")  # İlk 200 byte'ı göster
        return None
    except Exception as e:
        print(f"❌ Error receiving message: {e}")
        return None


def create_message(msg_type, sender=None, recipient=None, content=None):
    """
    Hızlı mesaj oluşturma helper fonksiyonu
    """
    return Message(msg_type, sender, recipient, content)


