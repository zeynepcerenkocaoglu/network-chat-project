#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Web Server Module
Modern, feature-rich dashboard with dark theme, charts, and user list
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
        elif self.path == '/api/users':
            # Kullanıcı listesini JSON olarak döndür
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            users = self.server.get_users()
            self.wfile.write(json.dumps(users).encode('utf-8'))
        else:
            self.send_error(404)
    
    def get_dashboard_html(self):
        """Web dashboard HTML'ini oluştur - Modern Enhanced Version"""
        return """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Chat Server Dashboard - Pro</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-primary: #0a0e27;
            --bg-secondary: #141b3d;
            --bg-card: #1a2142;
            --accent-primary: #00d9ff;
            --accent-secondary: #7b2cbf;
            --accent-success: #06ffa5;
            --accent-warning: #ffb800;
            --accent-danger: #ff006e;
            --text-primary: #ffffff;
            --text-secondary: #a0aec0;
            --border-color: rgba(0, 217, 255, 0.2);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 20px;
            position: relative;
            overflow-x: hidden;
        }
        
        body::before {
            content: '';
            position: fixed;
            top: -50%;
            right: -50%;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(0,217,255,0.1) 0%, transparent 70%);
            animation: pulse-glow 4s ease-in-out infinite;
            z-index: 0;
        }
        
        @keyframes pulse-glow {
            0%, 100% { opacity: 0.3; }
            50% { opacity: 0.6; }
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }
        
        .header {
            background: linear-gradient(135deg, rgba(0,217,255,0.1) 0%, rgba(123,44,191,0.1) 100%);
            border: 2px solid var(--border-color);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,217,255,0.2);
        }
        
        .header h1 {
            font-size: 2.8em;
            margin-bottom: 10px;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            filter: drop-shadow(0 0 20px rgba(0,217,255,0.3));
        }
        
        .header p {
            color: var(--text-secondary);
            font-size: 1.1em;
        }
        
        .status-bar {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            padding: 15px;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            margin-bottom: 30px;
        }
        
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--accent-success);
            box-shadow: 0 0 20px var(--accent-success);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.6; transform: scale(1.1); }
        }
        
        .status-text {
            color: var(--accent-success);
            font-weight: bold;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: var(--bg-card);
            border: 2px solid var(--border-color);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, transparent, rgba(0,217,255,0.1));
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            border-color: var(--accent-primary);
            box-shadow: 0 10px 40px rgba(0,217,255,0.3);
        }
        
        .stat-card:hover::before {
            opacity: 1;
        }
        
        .stat-icon {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .stat-label {
            color: var(--text-secondary);
            font-size: 0.95em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .content-grid {
            display: grid;
            grid-template-columns: 1fr 350px;
            gap: 20px;
            margin-bottom: 30px;
        }
        
        @media (max-width: 1024px) {
            .content-grid {
                grid-template-columns: 1fr;
            }
        }
        
        .card {
            background: var(--bg-card);
            border: 2px solid var(--border-color);
            border-radius: 15px;
            padding: 25px;
        }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid var(--border-color);
        }
        
        .card-title {
            font-size: 1.5em;
            color: var(--accent-primary);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .btn {
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0,217,255,0.4);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .logs {
            background: rgba(10, 14, 39, 0.8);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 15px;
            max-height: 500px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.6;
        }
        
        .logs::-webkit-scrollbar {
            width: 8px;
        }
        
        .logs::-webkit-scrollbar-track {
            background: var(--bg-secondary);
            border-radius: 4px;
        }
        
        .logs::-webkit-scrollbar-thumb {
            background: var(--accent-primary);
            border-radius: 4px;
        }
        
        .log-entry {
            padding: 8px 12px;
            margin-bottom: 5px;
            border-left: 3px solid transparent;
            border-radius: 5px;
            transition: all 0.2s;
        }
        
        .log-entry:hover {
            background: rgba(0,217,255,0.05);
        }
        
        .log-entry.public {
            border-left-color: var(--accent-success);
            background: rgba(6, 255, 165, 0.05);
        }
        
        .log-entry.private {
            border-left-color: var(--accent-warning);
            background: rgba(255, 184, 0, 0.05);
        }
        
        .log-entry.system {
            border-left-color: var(--accent-primary);
            background: rgba(0, 217, 255, 0.05);
        }
        
        .log-entry.warning {
            border-left-color: var(--accent-warning);
            background: rgba(255, 184, 0, 0.1);
        }
        
        .log-entry.error {
            border-left-color: var(--accent-danger);
            background: rgba(255, 0, 110, 0.1);
        }
        
        .log-filter {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }
        
        .filter-btn {
            padding: 8px 15px;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.3s;
            font-size: 12px;
        }
        
        .filter-btn:hover {
            border-color: var(--accent-primary);
            color: var(--accent-primary);
        }
        
        .filter-btn.active {
            background: var(--accent-primary);
            color: white;
            border-color: var(--accent-primary);
        }
        
        .search-box {
            flex: 1;
            min-width: 200px;
            padding: 8px 15px;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: white;
            font-size: 14px;
        }
        
        .search-box:focus {
            outline: none;
            border-color: var(--accent-primary);
            box-shadow: 0 0 10px rgba(0,217,255,0.3);
        }
        
        .users-list {
            max-height: 400px;
            overflow-y: auto;
        }
        
        .user-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            margin-bottom: 10px;
            transition: all 0.3s;
        }
        
        .user-item:hover {
            border-color: var(--accent-primary);
            transform: translateX(5px);
        }
        
        .user-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.2em;
        }
        
        .user-info {
            flex: 1;
        }
        
        .user-name {
            font-weight: bold;
            color: var(--text-primary);
        }
        
        .user-status {
            font-size: 0.85em;
            color: var(--text-secondary);
        }
        
        .chart-container {
            position: relative;
            height: 300px;
            margin-top: 20px;
        }
        
        .footer {
            text-align: center;
            padding: 20px;
            color: var(--text-secondary);
            border-top: 1px solid var(--border-color);
            margin-top: 30px;
        }
        
        .timestamp {
            color: var(--text-secondary);
            margin-right: 10px;
        }
        
        .log-type {
            font-weight: bold;
            margin-right: 10px;
        }
        
        .no-data {
            text-align: center;
            padding: 40px;
            color: var(--text-secondary);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Chat Server Dashboard Pro</h1>
            <p>Real-time monitoring and analytics</p>
        </div>
        
        <div class="status-bar">
            <div class="status-dot"></div>
            <span class="status-text">Server Online</span>
            <span style="color: var(--text-secondary); margin-left: 20px;">●</span>
            <span id="uptime" style="color: var(--text-secondary);">Loading...</span>
        </div>
        
        <div class="dashboard-grid">
            <div class="stat-card">
                <div class="stat-icon">👥</div>
                <div class="stat-value" id="connected-clients">0</div>
                <div class="stat-label">Online Users</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">💬</div>
                <div class="stat-value" id="total-messages">0</div>
                <div class="stat-label">Total Messages</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🔗</div>
                <div class="stat-value" id="total-connections">0</div>
                <div class="stat-label">Connections</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">⚠️</div>
                <div class="stat-value" id="warnings">0</div>
                <div class="stat-label">Warnings</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🔇</div>
                <div class="stat-value" id="mutes">0</div>
                <div class="stat-label">Mutes</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🚫</div>
                <div class="stat-value" id="kicks">0</div>
                <div class="stat-label">Kicks</div>
            </div>
        </div>
        
        <div class="content-grid">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">📋 Server Logs</h2>
                    <button class="btn" onclick="refreshLogs()">
                        🔄 Refresh
                    </button>
                </div>
                
                <div class="log-filter">
                    <button class="filter-btn active" onclick="filterLogs('ALL')" data-filter="ALL">All</button>
                    <button class="filter-btn" onclick="filterLogs('PUBLIC')" data-filter="PUBLIC">Public</button>
                    <button class="filter-btn" onclick="filterLogs('PRIVATE')" data-filter="PRIVATE">Private</button>
                    <button class="filter-btn" onclick="filterLogs('SYSTEM')" data-filter="SYSTEM">System</button>
                    <input type="text" class="search-box" placeholder="🔍 Search logs..." id="search-input" oninput="searchLogs()">
                </div>
                
                <div class="logs" id="logs">
                    <div class="no-data">⏳ Loading logs...</div>
                </div>
                
                <div class="chart-container">
                    <canvas id="messageChart"></canvas>
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">👥 Online Users</h2>
                    <span id="user-count" style="color: var(--accent-success); font-weight: bold;">0</span>
                </div>
                
                <div class="users-list" id="users-list">
                    <div class="no-data">👤 No users online</div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>💻 Chat Server Dashboard v2.0 | Enhanced Edition</p>
            <p>Auto-refresh: Every 3 seconds | Made with ❤️</p>
        </div>
    </div>
    
    <script>
        let allLogs = [];
        let currentFilter = 'ALL';
        let messageChart = null;
        let messageHistory = [];
        const maxHistoryPoints = 20;
        const startTime = Date.now();
        
        // Chart.js initialization
        function initChart() {
            const ctx = document.getElementById('messageChart').getContext('2d');
            messageChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Messages per Interval',
                        data: [],
                        borderColor: 'rgb(0, 217, 255)',
                        backgroundColor: 'rgba(0, 217, 255, 0.1)',
                        borderWidth: 2,
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: {
                                color: '#a0aec0'
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                color: '#a0aec0'
                            },
                            grid: {
                                color: 'rgba(0, 217, 255, 0.1)'
                            }
                        },
                        x: {
                            ticks: {
                                color: '#a0aec0'
                            },
                            grid: {
                                color: 'rgba(0, 217, 255, 0.1)'
                            }
                        }
                    }
                }
            });
        }
        
        function updateChart(messageCount) {
            const now = new Date();
            const timeLabel = now.toLocaleTimeString();
            
            messageHistory.push({ time: timeLabel, count: messageCount });
            
            if (messageHistory.length > maxHistoryPoints) {
                messageHistory.shift();
            }
            
            messageChart.data.labels = messageHistory.map(h => h.time);
            messageChart.data.datasets[0].data = messageHistory.map(h => h.count);
            messageChart.update();
        }
        
        function updateUptime() {
            const elapsed = Math.floor((Date.now() - startTime) / 1000);
            const hours = Math.floor(elapsed / 3600);
            const minutes = Math.floor((elapsed % 3600) / 60);
            const seconds = elapsed % 60;
            
            document.getElementById('uptime').textContent = 
                `Uptime: ${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }
        
        async function updateStats() {
            try {
                const response = await fetch('/api/stats');
                const stats = await response.json();
                
                document.getElementById('connected-clients').textContent = stats.connected_clients || 0;
                document.getElementById('total-messages').textContent = stats.total_messages || 0;
                document.getElementById('total-connections').textContent = stats.total_connections || 0;
                document.getElementById('warnings').textContent = stats.warnings || 0;
                document.getElementById('mutes').textContent = stats.mutes || 0;
                document.getElementById('kicks').textContent = stats.kicks || 0;
                
                updateChart(stats.total_messages || 0);
            } catch (error) {
                console.error('Stats fetch error:', error);
            }
        }
        
        async function updateUsers() {
            try {
                const response = await fetch('/api/users');
                const users = await response.json();
                
                const usersList = document.getElementById('users-list');
                const userCount = document.getElementById('user-count');
                
                userCount.textContent = users.length;
                
                if (users.length === 0) {
                    usersList.innerHTML = '<div class="no-data">👤 No users online</div>';
                    return;
                }
                
                usersList.innerHTML = users.map(user => `
                    <div class="user-item">
                        <div class="user-avatar">${user.charAt(0).toUpperCase()}</div>
                        <div class="user-info">
                            <div class="user-name">${user}</div>
                            <div class="user-status">🟢 Online</div>
                        </div>
                    </div>
                `).join('');
            } catch (error) {
                console.error('Users fetch error:', error);
            }
        }
        
        async function refreshLogs() {
            try {
                const response = await fetch('/api/logs');
                const logs = await response.json();
                
                allLogs = logs;
                displayLogs();
            } catch (error) {
                console.error('Logs fetch error:', error);
            }
        }
        
        function displayLogs() {
            const logsContainer = document.getElementById('logs');
            const searchTerm = document.getElementById('search-input').value.toLowerCase();
            
            let filteredLogs = allLogs;
            
            // Filter by type
            if (currentFilter !== 'ALL') {
                filteredLogs = filteredLogs.filter(log => log.type === currentFilter);
            }
            
            // Filter by search term
            if (searchTerm) {
                filteredLogs = filteredLogs.filter(log => 
                    log.message.toLowerCase().includes(searchTerm) ||
                    log.type.toLowerCase().includes(searchTerm)
                );
            }
            
            if (filteredLogs.length === 0) {
                logsContainer.innerHTML = '<div class="no-data">📭 No logs match your criteria</div>';
                return;
            }
            
            logsContainer.innerHTML = filteredLogs.reverse().map(log => `
                <div class="log-entry ${log.type.toLowerCase()}">
                    <span class="timestamp">[${log.timestamp}]</span>
                    <span class="log-type">${log.type}</span>
                    <span>${log.message}</span>
                </div>
            `).join('');
        }
        
        function filterLogs(type) {
            currentFilter = type;
            
            // Update active button
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('active');
                if (btn.dataset.filter === type) {
                    btn.classList.add('active');
                }
            });
            
            displayLogs();
        }
        
        function searchLogs() {
            displayLogs();
        }
        
        // Initialize
        initChart();
        updateStats();
        updateUsers();
        refreshLogs();
        
        // Auto-refresh
        setInterval(() => {
            updateStats();
            updateUsers();
            refreshLogs();
            updateUptime();
        }, 3000);
        
        // Update uptime every second
        setInterval(updateUptime, 1000);
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
    
    def get_users(self):
        """Aktif kullanıcı listesini al"""
        if not self.chat_server:
            return []
        
        with self.chat_server.clients_lock:
            users = list(self.chat_server.clients.keys())
        
        return users
    
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
    
    def get_users(self):
        """Kullanıcı listesini döndür"""
        return self.web_server.get_users()
    
    def get_logs(self):
        """Logları döndür"""
        return self.web_server.get_logs()
    
