#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logger Module
Tüm server loglarını yöneten modül
"""

import os
from datetime import datetime
from common.config import LOG_FILE, LOG_TIMESTAMP_FORMAT


class ChatLogger:
    """Chat server için loglama sınıfı"""
    
    def __init__(self, log_file=LOG_FILE):
        self.log_file = log_file
        self._ensure_log_directory()
        self._init_log_file()
    
    def _ensure_log_directory(self):
        """Log dizininin var olduğundan emin ol"""
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    def _init_log_file(self):
        """Log dosyasını başlat"""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"Server Started: {datetime.now().strftime(LOG_TIMESTAMP_FORMAT)}\n")
            f.write(f"{'='*60}\n")
    
    def log_public_message(self, sender, content):
        """Public mesajı logla"""
        self._write_log('PUBLIC', f"{sender}: {content}")
    
    def log_private_message(self, sender, recipient, content):
        """Private mesajı logla"""
        self._write_log('PRIVATE', f"{sender} -> {recipient}: {content}")
    
    def log_system_event(self, content):
        """Sistem olayını logla"""
        self._write_log('SYSTEM', content)
    
    def log_user_join(self, nickname, address):
        """Kullanıcı bağlantısını logla"""
        self._write_log('SYSTEM', f"{nickname}@{address} connected")
    
    def log_user_leave(self, nickname, address):
        """Kullanıcı ayrılmasını logla"""
        self._write_log('SYSTEM', f"{nickname}@{address} disconnected")
    
    def log_rate_limit_warning(self, nickname, warning_count):
        """Rate limit uyarısını logla"""
        self._write_log('SYSTEM', f"{nickname} received rate limit warning #{warning_count}")
    
    def log_rate_limit_mute(self, nickname, duration):
        """Mute olayını logla"""
        self._write_log('SYSTEM', f"{nickname} muted for {duration}s (sent 16 msgs)")
    
    def log_rate_limit_kick(self, nickname):
        """Kick olayını logla"""
        self._write_log('SYSTEM', f"{nickname} kicked for spamming")
    
    def log_error(self, error_msg):
        """Hata logla"""
        self._write_log('ERROR', error_msg)
    
    def _write_log(self, log_type, content):
        """Log dosyasına yaz"""
        timestamp = datetime.now().strftime(LOG_TIMESTAMP_FORMAT)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {log_type} | {content}\n")
    
    def get_recent_logs(self, count=50):
        """Son N satır logu oku"""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return lines[-count:] if len(lines) > count else lines
        except FileNotFoundError:
            return []
    
    def clear_logs(self):
        """Log dosyasını temizle"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"{'='*60}\n")
            f.write(f"Logs Cleared: {datetime.now().strftime(LOG_TIMESTAMP_FORMAT)}\n")
            f.write(f"{'='*60}\n")