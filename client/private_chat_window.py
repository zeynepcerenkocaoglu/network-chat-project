#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Private Chat Window Module
Private chat pencerelerini yönetir
"""

import tkinter as tk
from tkinter import scrolledtext
from common.config import COLOR_PRIMARY, COLOR_SUCCESS, COLOR_WHITE


class PrivateChatWindow:
    """Tek bir private chat penceresi"""
    
    def __init__(self, target_user, send_callback):
        self.target_user = target_user
        self.send_callback = send_callback
        
        # Pencereyi oluştur
        self.window = tk.Toplevel()
        self.window.title(f"Private Chat - {target_user}")
        self.window.geometry("500x400")
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Widget'ları oluştur"""
        # Header
        header_frame = tk.Frame(self.window, bg=COLOR_PRIMARY, height=35)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text=f"🔒 Private Chat with {self.target_user}",
            font=("Arial", 10, "bold"),
            bg=COLOR_PRIMARY,
            fg=COLOR_WHITE
        ).pack(side=tk.LEFT, padx=10, pady=5)
        
        # Chat area
        self.chat_area = scrolledtext.ScrolledText(
            self.window,
            font=("Arial", 9),
            bg=COLOR_WHITE,
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tag konfigürasyonları
        self.chat_area.tag_config('me', foreground=COLOR_PRIMARY, font=("Arial", 9, "bold"))
        self.chat_area.tag_config('them', foreground="#333333")
        self.chat_area.tag_config('system', foreground="#666666", font=("Arial", 8, "italic"))
        
        # Input frame
        input_frame = tk.Frame(self.window)
        input_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        self.message_entry = tk.Entry(input_frame, font=("Arial", 9))
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.message_entry.bind('<Return>', lambda e: self._on_send())
        self.message_entry.focus()
        
        self.send_button = tk.Button(
            input_frame,
            text="Send",
            font=("Arial", 9),
            bg=COLOR_SUCCESS,
            fg=COLOR_WHITE,
            command=self._on_send
        )
        self.send_button.pack(side=tk.LEFT)
    
    def _on_send(self):
        """Mesaj gönder"""
        message = self.message_entry.get().strip()
        if message:
            # Callback'i çağır
            if self.send_callback:
                self.send_callback(self.target_user, message)
            
            # Kendi mesajını göster
            self.add_message(f"You: {message}", 'me')
            self.message_entry.delete(0, tk.END)
    
    def add_message(self, text, tag=None):
        """Chat area'ya mesaj ekle"""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, text + '\n', tag)
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)
    
    def add_received_message(self, sender, message):
        """Gelen mesajı göster"""
        self.add_message(f"{sender}: {message}", 'them')
    
    def add_system_message(self, message):
        """Sistem mesajı göster"""
        self.add_message(f"• {message}", 'system')
    
    def close(self):
        """Pencereyi kapat"""
        self.window.destroy()
    
    def focus(self):
        """Pencereyi öne getir"""
        self.window.lift()
        self.window.focus_force()


class PrivateChatManager:
    """Tüm private chat pencerelerini yöneten sınıf"""
    
    def __init__(self, send_callback):
        self.windows = {}  # {user: PrivateChatWindow}
        self.send_callback = send_callback
    
    def open_private_chat(self, target_user, my_nickname):
        """Private chat penceresi aç"""
        # Kendisiyle chat açmayı engelle
        if target_user == my_nickname:
            return None
        
        # Zaten açıksa öne getir
        if target_user in self.windows:
            self.windows[target_user].focus()
            return self.windows[target_user]
        
        # Yeni pencere oluştur
        window = PrivateChatWindow(target_user, self.send_callback)
        self.windows[target_user] = window
        
        # Pencere kapandığında listeden çıkar
        def on_close():
            if target_user in self.windows:
                del self.windows[target_user]
            window.close()
        
        window.window.protocol("WM_DELETE_WINDOW", on_close)
        
        return window
    
    def handle_incoming_message(self, sender, message):
        """Gelen private mesajı yönet"""
        # Pencere açık mı?
        if sender not in self.windows:
            # Yeni pencere aç
            window = PrivateChatWindow(sender, self.send_callback)
            self.windows[sender] = window
            
            def on_close():
                if sender in self.windows:
                    del self.windows[sender]
                window.close()
            
            window.window.protocol("WM_DELETE_WINDOW", on_close)
        
        # Mesajı ekle
        self.windows[sender].add_received_message(sender, message)
        self.windows[sender].focus()
    
    def close_all(self):
        """Tüm private chat pencerelerini kapat"""
        for window in list(self.windows.values()):
            window.close()
        self.windows.clear()
    
    def get_window(self, user):
        """Belirli bir kullanıcının penceresini getir"""
        return self.windows.get(user)