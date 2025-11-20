#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utils Module
Yardımcı fonksiyonlar ve genel kullanım araçları
"""

from datetime import datetime
import random
import string


def get_timestamp():
    """Şu anki timestamp'i formatlanmış olarak döndür"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_time_only():
    """Sadece saat bilgisini döndür"""
    return datetime.now().strftime('%H:%M:%S')


def generate_random_suffix():
    """Rastgele 3 haneli sayı üret (nickname uniqueness için)"""
    return str(random.randint(100, 999))


def validate_nickname(nickname):
    """
    Nickname'i validate et
    Returns:
        (bool, str): (geçerli_mi, hata_mesajı)
    """
    if not nickname:
        return False, "Nickname boş olamaz"
    
    if nickname.startswith('*'):
        return False, "Nickname '*' ile başlayamaz (relay için ayrılmış)"
    
    if len(nickname) > 20:
        return False, "Nickname 20 karakterden uzun olamaz"
    
    # Geçerli karakterler kontrolü
    allowed = set(string.ascii_letters + string.digits + '_-')
    if not all(c in allowed for c in nickname):
        return False, "Nickname sadece harf, rakam, '_' ve '-' içerebilir"
    
    return True, ""


def format_message_display(message_type, sender, content, timestamp=None):
    """
    GUI'de gösterilecek mesajı formatla
    """
    time_str = timestamp or get_time_only()
    
    if message_type == "SYSTEM":
        return f"[{time_str}] • {content}"
    elif message_type == "JOIN":
        return f"[{time_str}] 👤 {content}"
    elif message_type == "LEAVE":
        return f"[{time_str}] 🚪 {content}"
    elif message_type == "PRIVATE":
        return f"[{time_str}] 🔒 {sender}: {content}"
    else:  # PUBLIC
        return f"[{time_str}] {sender}: {content}"


def truncate_text(text, max_length=100):
    """Metni belirtilen uzunlukta kes"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def parse_private_message(message):
    """
    Private mesaj komutunu parse et
    Format: /pm nickname message
    Returns:
        (bool, str, str): (başarılı_mı, hedef_nickname, mesaj)
    """
    if not message.startswith('/pm '):
        return False, None, None
    
    parts = message[4:].split(' ', 1)
    if len(parts) < 2:
        return False, None, None
    
    target = parts[0]
    msg = parts[1]
    return True, target, msg


def is_valid_ip(ip):
    """IP adresinin geçerli olup olmadığını kontrol et"""
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            num = int(part)
            if num < 0 or num > 255:
                return False
        return True
    except:
        return False


def is_valid_port(port):
    """Port numarasının geçerli olup olmadığını kontrol et"""
    try:
        port_num = int(port)
        return 1024 <= port_num <= 65535
    except:
        return False


def format_file_size(size_bytes):
    """Dosya boyutunu human-readable formata çevir"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"