#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Server Module
HTTP ve WebSocket server'ı yönetir
"""

import http.server
import socketserver
import threading
import json
from datetime import datetime


class WebDashboardHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler - web dashboard için"""
    
    def do_GET(self):
        """GET request handler"""
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html_content = self.get_dashboard_html()
            self.wfile.write(html_content.encode('utf-8'))
        elif self.path == '/api/stats':
            # İstatistikleri JSON olarak döndür
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            stats = self.server.get_stats()
            self.wfile.write(json.dumps(stats).encode('utf-8'))
        elif self.path == '/api/logs':
            # Logları JSON olarak döndür
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            logs = self.server.get_logs()
            self.wfile.write(json.dumps(logs).encode('utf-8'))
        else:
            self.send_error(404)
    
    def get_dashboard_html(self):
        """Web dashboard HTML'ini oluştur"""
        return """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat Server Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        
        .stat-card h3 {
            color: #667eea;
            font-size: 2em;
            margin-bottom: 5px;
        }
        
        .stat-card p {
            color: #666;
            font-size: 0.9em;
        }
        
        .status {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 15px 30px;
            background: white;
            border-bottom: 2px solid #f0f0f0;
        }
        
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #4CAF50;
            margin-right: 10px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .logs-container {
            padding: 30px;
        }
        
        .logs-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .logs-header h2 {
            color: #333;
        }
        
        .refresh-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
        }
        
        .refresh-btn:hover {
            background: #764ba2;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .logs {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 20px;
            border-radius: 10px;
            max-height: 500px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.6;
        }
        
        .log-entry {
            padding: 8px;
            border-left: 3px solid transparent;
            margin-bottom: 5px;
            border-radius: 3px;
        }
        
        .log-entry.public {
            border-left-color: #4CAF50;
            background: rgba(76, 175, 80, 0.1);
        }
        
        .log-entry.private {
            border-left-color: #FF9800;
            background: rgba(255, 152, 0, 0.1);
        }
        
        .log-entry.system {
            border-left-color: #2196F3;
            background: rgba(33, 150, 243, 0.1);
        }
        
        .log-entry.warning {
            border-left-color: #FFC107;
            background: rgba(255, 193, 7, 0.1);
        }
        
        .log-entry.error {
            border-left-color: #F44336;
            background: rgba(244, 67, 54, 0.1);
        }
        
        .timestamp {
            color: #888;
            margin-right: 10px;
        }
        
        .log-type {
            color: #4CAF50;
            font-weight: bold;
            margin-right: 10px;
        }
        
        .footer {
            text-align: center;
            padding: 20px;
            color: #666;
            background: #f8f9fa;
            font-size: 0.9em;
        }
        
        .emoji {
            font-size: 1.2em;
            margin-right: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Chat Server Dashboard</h1>
            <p>Real-time monitoring and logs</p>
        </div>
        
        <div class="status">
            <div class="status-dot"></div>
            <span><strong>Status:</strong> Server Active</span>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <h3 id="connected-clients">0</h3>
                <p>👥 Connected Clients</p>
            </div>
            <div class="stat-card">
                <h3 id="total-messages">0</h3>
                <p>📨 Total Messages</p>
            </div>
            <div class="stat-card">
                <h3 id="total-connections">0</h3>
                <p>🔗 Total Connections</p>
            </div>
            <div class="stat-card">
                <h3 id="warnings">0</h3>
                <p>⚠️ Warnings</p>
            </div>
        </div>
        
        <div class="logs-container">
            <div class="logs-header">
                <h2>📋 Server Logs</h2>
                <button class="refresh-btn" onclick="refreshLogs()">🔄 Refresh Logs</button>
            </div>
            <div class="logs" id="logs">
                <div class="log-entry system">
                    <span class="timestamp">[--:--:--]</span>
                    <span class="log-type">SYSTEM</span>
                    <span>Waiting for logs...</span>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>💻 Chat Server Dashboard v1.0 | Made with ❤️</p>
            <p>Auto-refresh: Every 3 seconds | Real-time data</p>
        </div>
    </div>
    
    <script>
        // Gerçek verilerle çalışacak fonksiyonlar
        
        async function updateStats() {
            try {
                const response = await fetch('/api/stats');
                const stats = await response.json();
                
                document.getElementById('connected-clients').textContent = stats.connected_clients || 0;
                document.getElementById('total-messages').textContent = stats.total_messages || 0;
                document.getElementById('total-connections').textContent = stats.total_connections || 0;
                document.getElementById('warnings').textContent = stats.warnings || 0;
            } catch (error) {
                console.error('Stats fetch error:', error);
            }
        }
        
        async function refreshLogs() {
            try {
                const response = await fetch('/api/logs');
                const logs = await response.json();
                
                const logsContainer = document.getElementById('logs');
                logsContainer.innerHTML = '';
                
                if (logs.length === 0) {
                    logsContainer.innerHTML = `
                        <div class="log-entry system">
                            <span class="timestamp">[--:--:--]</span>
                            <span class="log-type">SYSTEM</span>
                            <span>No logs yet. Waiting for activity...</span>
                        </div>
                    `;
                    return;
                }
                
                // Logları ters sırada göster (en yeni üstte)
                logs.reverse().forEach(log => {
                    const logEntry = document.createElement('div');
                    const logType = log.type.toLowerCase();
                    logEntry.className = `log-entry ${logType}`;
                    
                    logEntry.innerHTML = `
                        <span class="timestamp">[${log.timestamp}]</span>
                        <span class="log-type">${log.type}</span>
                        <span>${log.message}</span>
                    `;
                    
                    logsContainer.appendChild(logEntry);
                });
            } catch (error) {
                console.error('Logs fetch error:', error);
            }
        }
        
        // İlk yükleme
        updateStats();
        refreshLogs();
        
        // Auto-refresh her 3 saniyede
        setInterval(() => {
            updateStats();
            refreshLogs();
        }, 3000);
    </script>
</body>
</html>
"""
    
    def log_message(self, format, *args):
        """Log mesajlarını sustur (console'u temiz tut)"""
        pass


class WebServer:
    """Web server yöneticisi"""
    
    def __init__(self, host='127.0.0.1', port=8080, chat_server=None):
        self.host = host
        self.port = port
        self.chat_server = chat_server
        self.server = None
        self.thread = None
        self.running = False
    
    def start(self):
        """Web server'ı başlat"""
        try:
            # Custom TCPServer oluştur
            self.server = CustomTCPServer(
                (self.host, self.port),
                WebDashboardHandler,
                self
            )
            self.server.allow_reuse_address = True
            self.running = True
            
            print(f"🌐 HTTP Server listening on http://{self.host}:{self.port}")
            
            # Thread'de çalıştır
            self.thread = threading.Thread(target=self._run_server, daemon=True)
            self.thread.start()
            
        except Exception as e:
            print(f"❌ Failed to start web server: {e}")
    
    def _run_server(self):
        """Server loop'u"""
        while self.running:
            try:
                self.server.serve_forever()
            except Exception as e:
                if self.running:
                    print(f"❌ Web server error: {e}")
                break
    
    def stop(self):
        """Web server'ı durdur"""
        self.running = False
        if self.server:
            self.server.shutdown()
            self.server.server_close()
    
    def get_stats(self):
        """Chat server'dan istatistikleri al"""
        if not self.chat_server:
            return {
                'connected_clients': 0,
                'total_messages': 0,
                'total_connections': 0,
                'warnings': 0,
                'mutes': 0,
                'kicks': 0
            }
        
        with self.chat_server.clients_lock:
            connected_clients = len(self.chat_server.clients)
        
        rate_stats = self.chat_server.rate_limiter.get_statistics()
        
        return {
            'connected_clients': connected_clients,
            'total_messages': self.chat_server.message_count,
            'total_connections': self.chat_server.total_connections,
            'warnings': rate_stats['total_warnings'],
            'mutes': rate_stats['total_mutes'],
            'kicks': rate_stats['total_kicks']
        }
    
    def get_logs(self):
        """Log dosyasından son 50 satırı oku"""
        if not self.chat_server:
            return []
        
        logs = []
        try:
            with open(self.chat_server.logger.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
                # Son 50 satırı al
                recent_lines = lines[-50:] if len(lines) > 50 else lines
                
                for line in recent_lines:
                    line = line.strip()
                    if not line or '=' in line:
                        continue
                    
                    # Parse log line
                    # Format: [2025-11-19 14:30:45] TYPE | message
                    if '[' in line and ']' in line:
                        try:
                            # Timestamp'i çıkar
                            timestamp_end = line.index(']')
                            timestamp = line[1:timestamp_end].split()[1]  # Sadece saat kısmı
                            
                            # Type ve message'ı çıkar
                            rest = line[timestamp_end+1:].strip()
                            if '|' in rest:
                                parts = rest.split('|', 1)
                                log_type = parts[0].strip()
                                message = parts[1].strip() if len(parts) > 1 else ''
                                
                                logs.append({
                                    'timestamp': timestamp,
                                    'type': log_type,
                                    'message': message
                                })
                        except:
                            continue
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"❌ Error reading logs: {e}")
        
        return logs


class CustomTCPServer(socketserver.TCPServer):
    """Custom TCPServer - web_server referansını tutar"""
    
    def __init__(self, server_address, RequestHandlerClass, web_server):
        self.web_server = web_server
        super().__init__(server_address, RequestHandlerClass)
    
    def get_stats(self):
        """İstatistikleri döndür"""
        return self.web_server.get_stats()
    
    def get_logs(self):
        """Logları döndür"""
        return self.web_server.get_logs()


