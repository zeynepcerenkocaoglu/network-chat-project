#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chat Server Module
Ana server sınıfı - tüm bileşenleri koordine eder
"""

import socket
import threading
import time
from datetime import datetime
from common.protocol import Message
from common.config import (
    SERVER_HOST, SERVER_PORT, HTTP_PORT, WEBSOCKET_PORT,
    MESSAGE_TYPE_JOIN, MESSAGE_TYPE_LEAVE, MESSAGE_TYPE_USER_LIST,
    MESSAGE_TYPE_SYSTEM
)
from common.utils import generate_random_suffix
from server.logger import ChatLogger
from server.rate_limiter import RateLimiter
from server.client_handler import ClientHandler
from server.web_server import WebServer


class ChatServer:
    """Ana chat server sınıfı"""
    
    def __init__(self, host=SERVER_HOST, port=SERVER_PORT, 
                 http_port=HTTP_PORT, ws_port=WEBSOCKET_PORT):
        self.host = host
        self.port = port
        self.http_port = http_port
        self.ws_port = ws_port
        
        # Server socket
        self.server_socket = None
        self.running = False
        
        # Client yönetimi
        self.clients = {}  # {nickname: ClientHandler}
        self.clients_lock = threading.Lock()
        
        # Modüller
        self.logger = ChatLogger()
        self.rate_limiter = RateLimiter()
        self.web_server = WebServer(host=host, port=http_port, chat_server=self)
        
        # İstatistikler
        self.total_connections = 0
        self.message_count = 0
        self.start_time = datetime.now()
    
    def start(self):
        """Server'ı başlat"""
        try:
            # Socket oluştur
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            self._print_welcome_banner()
            
            # Web server'ı başlat
            self.web_server.start()
            
            # İstatistik thread'ini başlat
            stats_thread = threading.Thread(target=self._stats_printer, daemon=True)
            stats_thread.start()
            
            # Client'ları kabul et
            self._accept_clients()
        
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            self.stop()
    
    def stop(self):
        """Server'ı durdur"""
        print("\n🛑 Shutting down server...")
        self.running = False
        
        # Web server'ı durdur
        self.web_server.stop()
        
        # Tüm client'ları kapat
        with self.clients_lock:
            for handler in list(self.clients.values()):
                handler.stop()
        
        # Server socket'i kapat
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        print("✅ Server stopped")
    
    def _accept_clients(self):
        """Client bağlantılarını kabul et"""
        print("🔄 Waiting for connections...\n")
        
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                self.total_connections += 1
                
                print(f"📥 New connection from {address}")
                
                # ClientHandler oluştur ve başlat
                handler = ClientHandler(client_socket, address, self)
                handler.start()
            
            except OSError:
                if not self.running:
                    break
            except Exception as e:
                print(f"❌ Error accepting client: {e}")
    
    def register_client(self, handler, requested_nickname):
        """
        Client'ı kaydet ve benzersiz nickname ata
        Returns:
            str: Atanan nickname veya None (hata durumunda)
        """
        # '*' ile başlayan nickname'leri reddet
        if requested_nickname.startswith('*'):
            print(f"❌ Rejected nickname '{requested_nickname}' (reserved)")
            return None
        
        with self.clients_lock:
            # Nickname benzersiz mi kontrol et
            nickname = requested_nickname
            while nickname in self.clients:
                # Random suffix ekle
                nickname = f"{requested_nickname}{generate_random_suffix()}"
            
            # Client'ı kaydet
            handler.nickname = nickname
            self.clients[nickname] = handler
            self.rate_limiter.add_client(nickname)
            
            print(f"✅ Client registered: {nickname} from {handler.address}")
            self.logger.log_user_join(nickname, handler.address[0])
            
            return nickname
    
    def unregister_client(self, handler):
        """Client'ı kayıttan çıkar"""
        nickname = handler.nickname
        if not nickname:
            return
        
        with self.clients_lock:
            if nickname in self.clients:
                del self.clients[nickname]
                self.rate_limiter.remove_client(nickname)
                
                print(f"👋 Client disconnected: {nickname}")
                self.logger.log_user_leave(nickname, handler.address[0])
    
    def broadcast_message(self, message, exclude_sender=False, exclude_client=None):
        """Tüm client'lara mesaj gönder"""
        with self.clients_lock:
            for nickname, handler in list(self.clients.items()):
                # Exclude kontrolü
                if exclude_sender and message.sender == nickname:
                    continue
                if exclude_client and handler == exclude_client:
                    continue
                
                handler.send_message(message)
        
        self.message_count += 1
    
    def send_private_message(self, message):
        """Özel mesaj gönder"""
        with self.clients_lock:
            if message.recipient in self.clients:
                handler = self.clients[message.recipient]
                handler.send_message(message)
                self.message_count += 1
                return True
            return False
    
    def broadcast_join(self, nickname):
        """JOIN event'i broadcast et"""
        join_msg = Message(MESSAGE_TYPE_JOIN,
                          content=f"{nickname} joined the chat")
        self.broadcast_message(join_msg)
        self.logger.log_system_event(f"{nickname} joined")
        
        # User list'i güncelle
        self._broadcast_user_list()
    
    def broadcast_leave(self, nickname):
        """LEAVE event'i broadcast et"""
        leave_msg = Message(MESSAGE_TYPE_LEAVE,
                           content=f"{nickname} left the chat")
        self.broadcast_message(leave_msg)
        self.logger.log_system_event(f"{nickname} left")
        
        # User list'i güncelle
        self._broadcast_user_list()
    
    def send_user_list(self, handler):
        """Belirli bir client'a kullanıcı listesi gönder"""
        with self.clients_lock:
            users = list(self.clients.keys())
        
        user_list_msg = Message(MESSAGE_TYPE_USER_LIST,
                               content=','.join(users))
        handler.send_message(user_list_msg)
    
    def _broadcast_user_list(self):
        """Tüm client'lara kullanıcı listesi gönder"""
        with self.clients_lock:
            users = list(self.clients.keys())
        
        user_list_msg = Message(MESSAGE_TYPE_USER_LIST,
                               content=','.join(users))
        self.broadcast_message(user_list_msg)
    
    def _stats_printer(self):
        """Periyodik istatistik yazdır"""
        while self.running:
            time.sleep(30)  # Her 30 saniyede bir
            self._print_statistics()
    
    def _print_statistics(self):
        """İstatistikleri yazdır"""
        with self.clients_lock:
            client_count = len(self.clients)
        
        rate_stats = self.rate_limiter.get_statistics()
        uptime = datetime.now() - self.start_time
        
        print("\n" + "="*60)
        print("📊 SERVER STATISTICS")
        print("="*60)
        print(f"⏱️  Uptime: {uptime}")
        print(f"👥 Connected Clients: {client_count}")
        print(f"📨 Total Messages: {self.message_count}")
        print(f"🔗 Total Connections: {self.total_connections}")
        print(f"⚠️  Rate Limit Warnings: {rate_stats['total_warnings']}")
        print(f"🔇 Mutes: {rate_stats['total_mutes']}")
        print(f"🚫 Kicks: {rate_stats['total_kicks']}")
        print("="*60 + "\n")
    
    def _print_welcome_banner(self):
        """Karşılama banner'ını yazdır"""
        print("\n" + "="*60)
        print("🚀 CHAT SERVER - MODULAR VERSION")
        print("="*60)
        print(f"✅ Server listening on {self.host}:{self.port}")
        print(f"🌐 HTTP Server listening on http://{self.host}:{self.http_port}")
        print(f"📝 Log file: {self.logger.log_file}")
        print(f"⏰ Started at: {datetime.now().strftime('%H:%M:%S')}")
        print("="*60)
        print(f"📊 Open web dashboard: http://localhost:{self.http_port}")
        print("="*60)
        print()


