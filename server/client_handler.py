#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Client Handler Module
Her client bağlantısını thread içinde yönetir
"""

import socket
import threading
from common.protocol import Message, send_message, receive_message
from common.config import (
    MESSAGE_TYPE_PUBLIC, MESSAGE_TYPE_PRIVATE, MESSAGE_TYPE_SYSTEM,
    MESSAGE_TYPE_JOIN, MESSAGE_TYPE_LEAVE, MESSAGE_TYPE_USER_LIST,
    MESSAGE_TYPE_WARNING, MESSAGE_TYPE_MUTE, MESSAGE_TYPE_KICK
)


class ClientHandler:
    """Bir client bağlantısını yöneten sınıf"""
    
    def __init__(self, client_socket, address, server):
        self.socket = client_socket
        self.address = address
        self.server = server  # ChatServer referansı
        self.nickname = None
        self.running = False
        self.thread = None
    
    def start(self):
        """Client handler'ı başlat"""
        self.running = True
        self.thread = threading.Thread(target=self._handle_client, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Client handler'ı durdur"""
        self.running = False
        try:
            self.socket.close()
        except:
            pass
    
    def _handle_client(self):
        """Client ile iletişimi yönet"""
        try:
            # İlk mesajı al (nickname)
            initial_msg = receive_message(self.socket)
            if not initial_msg or not initial_msg.content:
                print(f"❌ No nickname received from {self.address}")
                self.socket.close()
                return
            
            # Nickname'i kaydet ve benzersiz yap
            self.nickname = self.server.register_client(self, initial_msg.content)
            if not self.nickname:
                error_msg = Message(MESSAGE_TYPE_SYSTEM, 
                                  content="Nickname rejected by server")
                send_message(self.socket, error_msg)
                self.socket.close()
                return
            
            # Client'a kabul mesajı gönder
            accept_msg = Message(MESSAGE_TYPE_SYSTEM, 
                               content=f"Connected as {self.nickname}")
            send_message(self.socket, accept_msg)
            
            # JOIN event gönder
            self.server.broadcast_join(self.nickname)
            
            # Aktif kullanıcı listesini gönder
            self.server.send_user_list(self)
            
            # Mesajları dinle
            while self.running:
                message = receive_message(self.socket)
                if not message:
                    break
                
                self._process_message(message)
        
        except Exception as e:
            print(f"❌ Error handling client {self.nickname}: {e}")
        
        finally:
            self._cleanup()
    
    def _process_message(self, message):
        """Gelen mesajı işle"""
        try:
            # Rate limit kontrolü
            limit_status, limit_data = self.server.rate_limiter.check_rate_limit(self.nickname)
            
            if limit_status == 'KICK':
                self._handle_kick()
                return
            elif limit_status == 'MUTE':
                self._handle_mute(limit_data)
                return
            elif limit_status == 'WARNING':
                self._handle_warning(limit_data)
                # Warning sonrası mesajı işlemeye devam et
            
            # Mesaj tipine göre işle
            if message.type == MESSAGE_TYPE_PUBLIC:
                self._handle_public_message(message)
            elif message.type == MESSAGE_TYPE_PRIVATE:
                self._handle_private_message(message)
            elif message.type == MESSAGE_TYPE_SYSTEM:
                # EXIT komutu
                if message.content == "EXIT":
                    self.running = False
        
        except Exception as e:
            print(f"❌ Error processing message from {self.nickname}: {e}")
    
    def _handle_public_message(self, message):
        """Public mesajı işle"""
        message.sender = self.nickname
        self.server.broadcast_message(message, exclude_sender=False)
        self.server.logger.log_public_message(self.nickname, message.content)
    
    def _handle_private_message(self, message):
        """Private mesajı işle"""
        message.sender = self.nickname
        success = self.server.send_private_message(message)
        
        if success:
            # Gönderene confirmation gönder
            confirm_msg = Message(MESSAGE_TYPE_SYSTEM,
                                content=f"Private message sent to {message.recipient}")
            send_message(self.socket, confirm_msg)
            self.server.logger.log_private_message(
                self.nickname, message.recipient, message.content)
        else:
            # Kullanıcı bulunamadı
            error_msg = Message(MESSAGE_TYPE_SYSTEM,
                              content=f"User '{message.recipient}' not found")
            send_message(self.socket, error_msg)
    
    def _handle_warning(self, warning_count):
        """Rate limit uyarısını işle"""
        warning_msg = Message(MESSAGE_TYPE_WARNING,
                            content=f"WARNING: Slow down! This is warning #{warning_count}")
        send_message(self.socket, warning_msg)
        self.server.logger.log_rate_limit_warning(self.nickname, warning_count)
    
    def _handle_mute(self, duration):
        """Mute durumunu işle"""
        mute_msg = Message(MESSAGE_TYPE_MUTE,
                         content=f"You have been muted for {duration} seconds")
        send_message(self.socket, mute_msg)
        self.server.logger.log_rate_limit_mute(self.nickname, duration)
        
        # Tüm client'lara bildir
        system_msg = Message(MESSAGE_TYPE_SYSTEM,
                           content=f"{self.nickname} has been muted for spamming")
        self.server.broadcast_message(system_msg, exclude_sender=False)
    
    def _handle_kick(self):
        """Kick durumunu işle"""
        kick_msg = Message(MESSAGE_TYPE_KICK,
                         content="You have been kicked for sending messages while muted")
        send_message(self.socket, kick_msg)
        self.server.logger.log_rate_limit_kick(self.nickname)
        
        # Tüm client'lara bildir
        system_msg = Message(MESSAGE_TYPE_SYSTEM,
                           content=f"{self.nickname} has been kicked for spamming")
        self.server.broadcast_message(system_msg, exclude_sender=True, 
                                     exclude_client=self)
        
        self.running = False
    
    def _cleanup(self):
        """Temizlik işlemleri"""
        if self.nickname:
            self.server.unregister_client(self)
            self.server.broadcast_leave(self.nickname)
        
        try:
            self.socket.close()
        except:
            pass
    
    def send_message(self, message):
        """Bu client'a mesaj gönder"""
        return send_message(self.socket, message)