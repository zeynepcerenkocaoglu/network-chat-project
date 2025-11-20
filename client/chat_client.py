#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chat Client Module
Ana client sınıfı - tüm client bileşenlerini koordine eder
"""

import tkinter as tk
from tkinter import simpledialog, messagebox
from common.config import (
    SERVER_HOST, SERVER_PORT,
    MESSAGE_TYPE_PUBLIC, MESSAGE_TYPE_PRIVATE, MESSAGE_TYPE_SYSTEM,
    MESSAGE_TYPE_JOIN, MESSAGE_TYPE_LEAVE, MESSAGE_TYPE_USER_LIST,
    MESSAGE_TYPE_WARNING, MESSAGE_TYPE_MUTE, MESSAGE_TYPE_KICK,
    MESSAGE_TYPE_UNMUTE, COLOR_PRIMARY, COLOR_DANGER
)
from common.utils import format_message_display
from client.network_handler import NetworkHandler
from client.gui_components import ChatGUI
from client.private_chat_window import PrivateChatManager


class ChatClient:
    """Ana chat client sınıfı"""
    
    def __init__(self, master, server_host=SERVER_HOST, server_port=SERVER_PORT):
        self.master = master
        self.server_host = server_host
        self.server_port = server_port
        
        # Bileşenler
        self.network = NetworkHandler(server_host, server_port)
        self.gui = ChatGUI(master)
        self.private_chat_manager = PrivateChatManager(self._send_private_message)
        
        # Durum
        self.nickname = None
        self.is_muted = False
        self.mute_timer_id = None
        
        # Window close handler
        self.master.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # GUI callback'lerini ayarla
        self.gui.set_callbacks(
            on_send=self._handle_send,
            on_exit=self._on_closing,
            on_user_double_click=self._handle_user_double_click
        )
        
        # Bağlan
        self._connect_to_server()
    
    def _connect_to_server(self):
        """Server'a bağlan"""
        # Nickname sor
        self.nickname = simpledialog.askstring(
            "Nickname",
            "Enter your nickname:",
            parent=self.master
        )
        
        if not self.nickname:
            messagebox.showerror("Error", "Nickname is required!")
            self.master.destroy()
            return
        
        # Bağlan
        self.gui.add_message("Connecting to server...", 'system')
        success, message = self.network.connect(self.nickname)
        
        if success:
            # Bağlantı başarılı
            self.gui.add_message(f"✅ {message}", 'system')
            
            # Nickname'i başlıkta göster
            assigned_nick = message.split("Connected as ")[-1]
            self.nickname = assigned_nick
            self.gui.update_title(self.nickname)
            
            # Mesaj alıcıyı başlat
            self.network.start_receiver(self._handle_incoming_message)
        else:
            # Bağlantı başarısız
            messagebox.showerror("Connection Error", message)
            self.master.destroy()
    
    def _handle_incoming_message(self, message):
        """Gelen mesajı işle (network thread'inden çağrılır)"""
        # GUI güncellemelerini main thread'de yap
        self.master.after(0, lambda: self._process_message(message))
    
    def _process_message(self, message):
        """Mesajı işle (main thread'de çalışır)"""
        try:
            if message.type == MESSAGE_TYPE_PUBLIC:
                self._handle_public_message(message)
            elif message.type == MESSAGE_TYPE_PRIVATE:
                self._handle_private_message(message)
            elif message.type == MESSAGE_TYPE_JOIN:
                self._handle_join_event(message)
            elif message.type == MESSAGE_TYPE_LEAVE:
                self._handle_leave_event(message)
            elif message.type == MESSAGE_TYPE_USER_LIST:
                self._handle_user_list(message)
            elif message.type == MESSAGE_TYPE_WARNING:
                self._handle_warning(message)
            elif message.type == MESSAGE_TYPE_MUTE:
                self._handle_mute(message)
            elif message.type == MESSAGE_TYPE_KICK:
                self._handle_kick(message)
            elif message.type == MESSAGE_TYPE_SYSTEM:
                self._handle_system_message(message)
        except Exception as e:
            print(f"❌ Error processing message: {e}")
    
    def _handle_public_message(self, message):
        """Public mesajı göster"""
        formatted = format_message_display(
            MESSAGE_TYPE_PUBLIC,
            message.sender,
            message.content,
            message.timestamp.split()[1] if message.timestamp else None
        )
        self.gui.add_message(formatted)
    
    def _handle_private_message(self, message):
        """Private mesajı göster"""
        self.private_chat_manager.handle_incoming_message(
            message.sender,
            message.content
        )
    
    def _handle_join_event(self, message):
        """JOIN event'i göster"""
        self.gui.add_message(f"👤 {message.content}", 'join')
    
    def _handle_leave_event(self, message):
        """LEAVE event'i göster"""
        self.gui.add_message(f"🚪 {message.content}", 'leave')
    
    def _handle_user_list(self, message):
        """Kullanıcı listesini güncelle"""
        if message.content:
            users = message.content.split(',')
            # Kendini listeden çıkar
            users = [u for u in users if u != self.nickname]
            self.gui.update_user_list(users)
    
    def _handle_warning(self, message):
        """Rate limit uyarısını göster"""
        self.gui.add_message(f"⚠️ {message.content}", 'warning')
        messagebox.showwarning("Rate Limit Warning", message.content)
    
    def _handle_mute(self, message):
        """Mute durumunu işle"""
        self.is_muted = True
        self.gui.enable_send(False)
        self.gui.update_header_color(COLOR_DANGER)
        self.gui.add_message(f"🔇 {message.content}", 'mute')
        
        messagebox.showwarning("Muted", message.content)
        
        # Mute süresini parse et (örn: "30 seconds")
        try:
            duration = int(message.content.split()[5])
            # Timer başlat
            self._start_unmute_timer(duration)
        except:
            pass
    
    def _handle_kick(self, message):
        """Kick durumunu işle"""
        self.gui.add_message(f"⛔ {message.content}", 'kick')
        messagebox.showerror("Kicked", message.content)
        self.master.after(1000, self.master.destroy)
    
    def _handle_system_message(self, message):
        """Sistem mesajını göster"""
        self.gui.add_message(f"• {message.content}", 'system')
        
        # Connection lost kontrolü
        if "Connection lost" in message.content:
            messagebox.showerror("Connection Lost", "Connection to server lost!")
            self.master.after(1000, self.master.destroy)
    
    def _start_unmute_timer(self, duration):
        """Unmute timer'ını başlat"""
        if self.mute_timer_id:
            self.master.after_cancel(self.mute_timer_id)
        
        self.mute_timer_id = self.master.after(
            duration * 1000,
            self._unmute
        )
    
    def _unmute(self):
        """Mute'u kaldır"""
        self.is_muted = False
        self.gui.enable_send(True)
        self.gui.update_header_color(COLOR_PRIMARY)
        self.gui.add_message("✅ You have been unmuted", 'system')
        self.mute_timer_id = None
    
    def _handle_send(self, message):
        """Send butonu basıldığında"""
        if self.is_muted:
            messagebox.showwarning("Muted", "You are currently muted!")
            return
        
        # Public mesaj gönder
        if self.network.send_public_message(message):
            # Başarılı (server broadcast edecek)
            pass
        else:
            messagebox.showerror("Error", "Failed to send message")
    
    def _handle_user_double_click(self, user):
        """User listbox'ta double-click"""
        self.private_chat_manager.open_private_chat(user, self.nickname)
    
    def _send_private_message(self, recipient, message):
        """Private mesaj gönder"""
        if self.is_muted:
            messagebox.showwarning("Muted", "You are currently muted!")
            return
        
        if self.network.send_private_message(recipient, message):
            # Başarılı
            pass
        else:
            messagebox.showerror("Error", "Failed to send private message")
    
    def _on_closing(self):
        """Pencere kapatıldığında"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.network.disconnect()
            self.private_chat_manager.close_all()
            self.master.destroy()
    
    def run(self):
        """Client'ı çalıştır"""
        self.master.mainloop()