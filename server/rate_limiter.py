#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rate Limiter Module
Spam koruması ve rate limiting işlemlerini yönetir
"""

import time
from collections import deque
from common.config import (
    RATE_LIMIT_WINDOW, RATE_LIMIT_MAX,
    SEVERE_LIMIT_WINDOW, SEVERE_LIMIT_MAX,
    MUTE_DURATION
)


class RateLimiter:
    """Rate limiting ve spam koruması sınıfı"""
    
    def __init__(self):
        # Her client için mesaj zamanları
        self.message_times = {}  # {nickname: deque([timestamp, ...])}
        # Mute durumları
        self.muted_until = {}  # {nickname: timestamp}
        # Warning sayaçları
        self.warning_counts = {}  # {nickname: count}
        
        # İstatistikler
        self.total_warnings = 0
        self.total_mutes = 0
        self.total_kicks = 0
    
    def add_client(self, nickname):
        """Yeni client ekle"""
        self.message_times[nickname] = deque()
        self.muted_until[nickname] = None
        self.warning_counts[nickname] = 0
    
    def remove_client(self, nickname):
        """Client'ı kaldır"""
        if nickname in self.message_times:
            del self.message_times[nickname]
        if nickname in self.muted_until:
            del self.muted_until[nickname]
        if nickname in self.warning_counts:
            del self.warning_counts[nickname]
    
    def is_muted(self, nickname):
        """Client muted mi kontrol et"""
        if nickname not in self.muted_until:
            return False
        
        mute_time = self.muted_until[nickname]
        if mute_time is None:
            return False
        
        current_time = time.time()
        if current_time < mute_time:
            return True
        else:
            # Mute süresi doldu
            self.muted_until[nickname] = None
            return False
    
    def get_mute_remaining(self, nickname):
        """Kalan mute süresini döndür (saniye)"""
        if not self.is_muted(nickname):
            return 0
        
        mute_time = self.muted_until[nickname]
        current_time = time.time()
        return int(mute_time - current_time)
    
    def check_rate_limit(self, nickname):
        """
        Rate limit kontrolü yap
        Returns:
            ('OK', None) - Normal
            ('WARNING', warning_count) - Uyarı
            ('MUTE', duration) - Mute edildi
            ('KICK', None) - Kick edilmeli
        """
        current_time = time.time()
        
        # Muted ise kick
        if self.is_muted(nickname):
            self.total_kicks += 1
            return ('KICK', None)
        
        # Mesaj zamanını ekle
        if nickname not in self.message_times:
            self.add_client(nickname)
        
        self.message_times[nickname].append(current_time)
        
        # Eski mesajları temizle (SEVERE_LIMIT_WINDOW dışındakiler)
        while (self.message_times[nickname] and 
               current_time - self.message_times[nickname][0] > SEVERE_LIMIT_WINDOW):
            self.message_times[nickname].popleft()
        
        # Mesaj sayılarını hesapla
        recent_messages = list(self.message_times[nickname])
        
        # Son 5 saniyedeki mesajlar
        count_5s = sum(1 for t in recent_messages if current_time - t <= RATE_LIMIT_WINDOW)
        
        # Son 10 saniyedeki mesajlar
        count_10s = len(recent_messages)
        
        # SEVERE limit kontrolü (MUTE)
        if count_10s >= SEVERE_LIMIT_MAX:
            self.muted_until[nickname] = current_time + MUTE_DURATION
            self.total_mutes += 1
            return ('MUTE', MUTE_DURATION)
        
        # Normal limit kontrolü (WARNING)
        if count_5s >= RATE_LIMIT_MAX:
            self.warning_counts[nickname] = self.warning_counts.get(nickname, 0) + 1
            self.total_warnings += 1
            return ('WARNING', self.warning_counts[nickname])
        
        return ('OK', None)
    
    def get_statistics(self):
        """İstatistikleri döndür"""
        return {
            'total_warnings': self.total_warnings,
            'total_mutes': self.total_mutes,
            'total_kicks': self.total_kicks,
            'currently_muted': sum(1 for nick in self.muted_until.values() if nick)
        }
    
    def reset_warnings(self, nickname):
        """Bir client'ın warning sayacını sıfırla"""
        if nickname in self.warning_counts:
            self.warning_counts[nickname] = 0