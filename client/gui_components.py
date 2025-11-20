#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI Components Module
Tkinter GUI bileşenlerini oluşturur
"""

import tkinter as tk
from tkinter import scrolledtext
from common.config import (
    COLOR_PRIMARY, COLOR_SUCCESS, COLOR_WARNING, COLOR_DANGER,
    COLOR_BACKGROUND, COLOR_WHITE, GUI_WIDTH, GUI_HEIGHT
)


class ChatGUI:
    """Chat GUI bileşenlerini yöneten sınıf"""
    
    def __init__(self, master):
        self.master = master
        self.master.geometry(f"{GUI_WIDTH}x{GUI_HEIGHT}")
        self.master.configure(bg=COLOR_BACKGROUND)
        
        # Widget referansları
        self.header_label = None
        self.user_listbox = None
        self.chat_area = None
        self.message_entry = None
        self.send_button = None
        self.exit_button = None
        
        # Callbacks
        self.on_send_callback = None
        self.on_exit_callback = None
        self.on_user_double_click_callback = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Tüm GUI bileşenlerini oluştur"""
        # Ana container
        main_container = tk.Frame(self.master, bg=COLOR_BACKGROUND)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self._create_header(main_container)
        
        # Sol ve sağ paneller için container
        content_frame = tk.Frame(main_container, bg=COLOR_BACKGROUND)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Sol panel (User list)
        self._create_user_panel(content_frame)
        
        # Sağ panel (Chat area + input)
        self._create_chat_panel(content_frame)
    
    def _create_header(self, parent):
        """Header bölümünü oluştur"""
        header_frame = tk.Frame(parent, bg=COLOR_PRIMARY, height=40)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        header_frame.pack_propagate(False)
        
        self.header_label = tk.Label(
            header_frame,
            text="Chat Client",
            font=("Arial", 12, "bold"),
            bg=COLOR_PRIMARY,
            fg=COLOR_WHITE
        )
        self.header_label.pack(side=tk.LEFT, padx=10, pady=5)
    
    def _create_user_panel(self, parent):
        """Kullanıcı listesi panelini oluştur"""
        left_panel = tk.Frame(parent, bg=COLOR_BACKGROUND, width=200)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        
        # Başlık
        tk.Label(
            left_panel,
            text="👥 Online Users",
            font=("Arial", 10, "bold"),
            bg=COLOR_BACKGROUND
        ).pack(anchor=tk.W, pady=(0, 5))
        
        # User listbox
        user_frame = tk.Frame(left_panel)
        user_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(user_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.user_listbox = tk.Listbox(
            user_frame,
            font=("Arial", 9),
            bg=COLOR_WHITE,
            yscrollcommand=scrollbar.set
        )
        self.user_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.user_listbox.yview)
        
        # Double-click event
        self.user_listbox.bind('<Double-Button-1>', self._on_user_double_click)
        
        # İpucu
        tk.Label(
            left_panel,
            text="💡 Double-click to\nopen private chat",
            font=("Arial", 8),
            bg=COLOR_BACKGROUND,
            fg="#666"
        ).pack(pady=(5, 0))
    
    def _create_chat_panel(self, parent):
        """Chat panelini oluştur"""
        right_panel = tk.Frame(parent, bg=COLOR_BACKGROUND)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Chat başlığı
        tk.Label(
            right_panel,
            text="💬 Public Chat",
            font=("Arial", 10, "bold"),
            bg=COLOR_BACKGROUND
        ).pack(anchor=tk.W, pady=(0, 5))
        
        # Chat area
        self.chat_area = scrolledtext.ScrolledText(
            right_panel,
            font=("Arial", 9),
            bg=COLOR_WHITE,
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True)
        
        # Tag konfigürasyonları
        self._configure_chat_tags()
        
        # Alt panel (input + buttons)
        bottom_frame = tk.Frame(right_panel, bg=COLOR_BACKGROUND)
        bottom_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Message input
        tk.Label(
            bottom_frame,
            text="✏️ Message:",
            font=("Arial", 9),
            bg=COLOR_BACKGROUND
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.message_entry = tk.Entry(
            bottom_frame,
            font=("Arial", 9)
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.message_entry.bind('<Return>', lambda e: self._on_send())
        
        # Buttons
        self.exit_button = tk.Button(
            bottom_frame,
            text="Exit",
            font=("Arial", 9),
            bg=COLOR_DANGER,
            fg=COLOR_WHITE,
            command=self._on_exit
        )
        self.exit_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.send_button = tk.Button(
            bottom_frame,
            text="Send",
            font=("Arial", 9),
            bg=COLOR_SUCCESS,
            fg=COLOR_WHITE,
            command=self._on_send
        )
        self.send_button.pack(side=tk.LEFT)
    
    def _configure_chat_tags(self):
        """Chat area için text tag'lerini yapılandır"""
        self.chat_area.tag_config('system', foreground='#666666')
        self.chat_area.tag_config('join', foreground=COLOR_SUCCESS, font=("Arial", 9, "bold"))
        self.chat_area.tag_config('leave', foreground=COLOR_DANGER, font=("Arial", 9, "bold"))
        self.chat_area.tag_config('warning', foreground=COLOR_WARNING, font=("Arial", 9, "bold"))
        self.chat_area.tag_config('mute', foreground=COLOR_DANGER, font=("Arial", 9, "bold"))
        self.chat_area.tag_config('kick', foreground=COLOR_DANGER, font=("Arial", 9, "bold"))
        self.chat_area.tag_config('me', foreground=COLOR_PRIMARY, font=("Arial", 9, "bold"))
    
    def _on_send(self):
        """Send butonu callback"""
        if self.on_send_callback:
            message = self.message_entry.get().strip()
            if message:
                self.on_send_callback(message)
                self.message_entry.delete(0, tk.END)
    
    def _on_exit(self):
        """Exit butonu callback"""
        if self.on_exit_callback:
            self.on_exit_callback()
    
    def _on_user_double_click(self, event):
        """User listbox double-click callback"""
        if self.on_user_double_click_callback:
            selection = self.user_listbox.curselection()
            if selection:
                user = self.user_listbox.get(selection[0])
                self.on_user_double_click_callback(user)
    
    def set_callbacks(self, on_send=None, on_exit=None, on_user_double_click=None):
        """Callback fonksiyonlarını ayarla"""
        if on_send:
            self.on_send_callback = on_send
        if on_exit:
            self.on_exit_callback = on_exit
        if on_user_double_click:
            self.on_user_double_click_callback = on_user_double_click
    
    def update_title(self, nickname):
        """Pencere başlığını güncelle"""
        self.master.title(f"Chat Client - {nickname}")
        self.header_label.config(text=f"Chat Client - {nickname}")
    
    def update_header_color(self, color):
        """Header rengini değiştir (mute durumunda)"""
        header_frame = self.header_label.master
        header_frame.config(bg=color)
        self.header_label.config(bg=color)
    
    def add_message(self, text, tag=None):
        """Chat area'ya mesaj ekle"""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, text + '\n', tag)
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)
    
    def update_user_list(self, users):
        """Kullanıcı listesini güncelle"""
        self.user_listbox.delete(0, tk.END)
        for user in users:
            self.user_listbox.insert(tk.END, user)
    
    def enable_send(self, enabled=True):
        """Send butonu ve message entry'yi aktif/pasif yap"""
        state = tk.NORMAL if enabled else tk.DISABLED
        self.send_button.config(state=state)
        self.message_entry.config(state=state)
    
    def clear_chat(self):
        """Chat area'yı temizle"""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.delete(1.0, tk.END)
        self.chat_area.config(state=tk.DISABLED)