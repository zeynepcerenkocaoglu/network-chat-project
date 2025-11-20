🚀 Modular Chat Application
Modern, ölçeklenebilir ve bakımı kolay bir Python chat uygulaması. Orijinal monolitik yapıdan modüler bir mimariye dönüştürülmüştür.
Show Image
Show Image

📑 İçindekiler

Özellikler
Proje Yapısı
Kurulum
Hızlı Başlangıç
Kullanım Kılavuzu
Modül Detayları
API Dokümantasyonu
Test Senaryoları
Sorun Giderme


✨ Özellikler
🖥️ Server Özellikleri

Multi-Client Desteği: Sınırsız sayıda client aynı anda bağlanabilir
Thread-Safe İşlemler: Her client ayrı thread'de güvenli yönetilir
Benzersiz Nickname: Otomatik suffix ile çakışma önlenir
Public Messaging: Tüm kullanıcılara broadcast
Private Messaging: 1-to-1 özel mesajlaşma
JOIN/LEAVE Events: Kullanıcı bildirimleri
Rate Limiting: 3 seviyeli spam koruması (WARNING/MUTE/KICK)
Kapsamlı Loglama: Tüm aktivitelerin kaydı
Real-time İstatistikler: 30 saniyede bir istatistik

💻 Client Özellikleri

Modern GUI: Tkinter tabanlı kullanıcı dostu arayüz
Renkli Mesajlar: Mesaj tiplerine göre renklendirilmiş görünüm
Online User List: Çevrimiçi kullanıcıları görüntüleme
Private Chat Windows: Ayrı private chat pencereleri
Double-Click Private: Kullanıcıya çift tıklayarak private chat
Rate Limit Handling: Visual feedback ve otomatik unmute
Timestamp Support: Her mesajda zaman damgası

🌐 Web Dashboard Özellikleri

Real-time Monitoring: Canlı server izleme ve istatistikler
Beautiful UI: Modern gradient tasarım ve koyu tema
Live Stats: Anlık kullanıcı, mesaj ve bağlantı sayıları
Colorful Logs: Renkli log görüntüleme (PUBLIC/PRIVATE/SYSTEM/WARNING)
Auto-refresh: Her 3 saniyede otomatik güncelleme
Responsive Design: Mobil uyumlu arayüz
Server Uptime: Server çalışma süresi gösterimi


📁 Proje Yapısı
chat_project/
│
├── 📂 common/              # Ortak Modüller
│   ├── config.py           # Konfigürasyon ayarları
│   ├── protocol.py         # Mesaj protokolü
│   └── utils.py            # Yardımcı fonksiyonlar
│
├── 📂 server/              # Server Modülleri
│   ├── chat_server.py      # Ana server sınıfı
│   ├── client_handler.py   # Client yönetimi
│   ├── logger.py           # Log sistemi
│   ├── rate_limiter.py     # Spam koruması
│   └── web_server.py       # Web dashboard server
│
├── 📂 client/              # Client Modülleri
│   ├── chat_client.py      # Ana client sınıfı
│   ├── network_handler.py  # Network işlemleri
│   ├── gui_components.py   # GUI bileşenleri
│   └── private_chat_window.py  # Private chat
│
├── 📂 logs/                # Log dosyaları (otomatik)
│
├── run_server.py           # Server başlatma
├── run_client.py           # Client başlatma
└── requirements.txt        # Gereksinimler

🔧 Kurulum
Gereksinimler

Python: 3.8+
Ek Kütüphane: Yok! (Sadece Python standard library)

bash# Python versiyonunu kontrol et
python --version

# Projeyi indir
cd chat_project

🚀 Hızlı Başlangıç
Server'ı Başlat
bashpython run_server.py
Çıktı:
============================================================
🚀 CHAT SERVER - MODULAR VERSION
============================================================
✅ Server listening on 127.0.0.1:5000
🌐 HTTP Server listening on http://127.0.0.1:8080
📝 Log file: logs/chat_server.log
⏰ Started at: 14:30:45
============================================================
📊 Open web dashboard: http://localhost:8080
============================================================
Client'ları Başlat
bash# Terminal 1 - Alice
python run_client.py

# Terminal 2 - Bob
python run_client.py
🌐 Web Dashboard'u Aç
Tarayıcınızda:
http://localhost:8080
veya
http://127.0.0.1:8080
Dashboard Özellikleri:

📊 Canlı istatistikler
📋 Renkli log görüntüleme
🔄 Otomatik yenileme (3 saniye)
🎨 Modern gradient tasarım


📖 Kullanım Kılavuzu
Public Mesaj Gönderme

Message input alanına mesajını yaz
Enter veya Send butonuna tıkla
Mesaj tüm kullanıcılara gönderilir

Private Mesaj Gönderme

Sol paneldeki kullanıcıya çift tıkla
Açılan pencerede mesajını yaz
Enter veya Send

Rate Limit Sistemi
DurumKoşulSonuçNormal< 10 mesaj/5s✅ NormalWARNING10+ mesaj/5s⚠️ Uyarı popupMUTE15+ mesaj/10s🔇 30 saniye susturmaKICKMuted iken mesaj🚫 Bağlantı kesilir
🌐 Web Dashboard Kullanımı
Dashboard'a Erişim
http://localhost:8080
Dashboard Bileşenleri
1. Server Status

🟢 Server Online: Server aktif durumda
⏱️ Uptime: Server çalışma süresi (hh:mm:ss)

2. Canlı İstatistikler

👥 Online Users: Anlık bağlı kullanıcı sayısı
💬 Total Messages: Toplam gönderilen mesaj sayısı
🔗 Connections: Toplam bağlantı sayısı
⚠️ Warnings: Rate limit uyarı sayısı

3. Server Logs

🔵 SYSTEM: Sistem olayları (bağlantı, JOIN, LEAVE)
🟢 PUBLIC: Genel mesajlar
🟠 PRIVATE: Özel mesajlar
🟡 WARNING: Rate limit uyarıları
🔴 ERROR: Hata mesajları

4. Otomatik Yenileme

Her 3 saniyede otomatik güncelleme
🔄 Refresh Logs butonu ile manuel yenileme

Dashboard API Endpoint'leri
İstatistikler:
GET /api/stats
Response:
json{
  "connected_clients": 3,
  "total_messages": 127,
  "total_connections": 15,
  "warnings": 2,
  "mutes": 0,
  "kicks": 0
}
Loglar:
GET /api/logs
Response:
json[
  {
    "timestamp": "14:30:45",
    "type": "SYSTEM",
    "message": "Alice@127.0.0.1 connected"
  },
  {
    "timestamp": "14:31:00",
    "type": "PUBLIC",
    "message": "Alice: Hello everyone!"
  }
]
Port Değiştirme
Farklı port kullanmak için:
bashpython run_server.py --http-port 9000
Sonra tarayıcıda:
http://localhost:9000

🔬 Modül Detayları
Common Modülleri
config.py - Konfigürasyon
Tüm proje ayarlarını merkezi olarak yönetir.
python# Server Ayarları
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

# Rate Limiting
RATE_LIMIT_WINDOW = 5  # saniye
RATE_LIMIT_MAX = 10    # mesaj
MUTE_DURATION = 30     # saniye

# Renkler
COLOR_PRIMARY = "#2196F3"
COLOR_SUCCESS = "#4CAF50"
protocol.py - Mesaj Protokolü
JSON tabanlı mesaj iletişimi.
Message Sınıfı:
pythonclass Message:
    def __init__(self, msg_type, sender, recipient, content, timestamp)
    def to_dict()  # JSON'a çevir
    @staticmethod from_dict(data)  # JSON'dan oluştur
Mesaj Tipleri:

PUBLIC: Herkese mesaj
PRIVATE: Özel mesaj
SYSTEM: Sistem mesajı
JOIN/LEAVE: Katılım/ayrılma
WARNING/MUTE/KICK: Rate limit

utils.py - Yardımcı Fonksiyonlar
pythonget_timestamp()              # "2025-11-19 14:30:45"
generate_random_suffix()     # "123"
validate_nickname(nick)      # (True, "")
format_message_display(...)  # "[14:30] Alice: Hi"
Server Modülleri
chat_server.py - Ana Server
Sorumluluklar:

Client bağlantılarını kabul
Mesaj broadcast
Modül koordinasyonu

Önemli Methodlar:
pythondef start()                  # Server'ı başlat
def register_client()        # Client kaydet
def broadcast_message()      # Mesaj broadcast
def send_private_message()   # Private mesaj
client_handler.py - Client Yöneticisi
Her client için ayrı thread'de çalışır.
Yaşam Döngüsü:
Bağlantı → Nickname → Kayıt → JOIN → Mesaj Loop → Cleanup → LEAVE
logger.py - Log Sistemi
Log Formatı:
[2025-11-19 14:30:45] PUBLIC | Alice: Hello!
[2025-11-19 14:30:50] PRIVATE | Alice -> Bob: Secret
[2025-11-19 14:31:00] SYSTEM | Charlie connected
rate_limiter.py - Spam Koruması
Algoritma: Sliding Window
LevelSüreMesajAksiyon15s10⚠️ WARNING210s15🔇 MUTE (30s)3Muted1🚫 KICK
web_server.py - Web Dashboard
Sorumluluklar:

HTTP server yönetimi
Dashboard HTML rendering
Real-time istatistik API
Log dosyası okuma ve parsing

Önemli Sınıflar:
pythonclass WebServer:
    def start()           # Web server başlat
    def get_stats()       # İstatistikleri al
    def get_logs()        # Log dosyasından oku
    
class WebDashboardHandler:
    def do_GET()          # HTTP GET request handler
API Endpoint'leri:

GET / → Dashboard HTML
GET /api/stats → İstatistikler (JSON)
GET /api/logs → Loglar (JSON)

Özellikler:

Modern gradient tasarım
Real-time data fetching
Auto-refresh her 3 saniyede
Renkli log görüntüleme
Responsive design

Client Modülleri
chat_client.py - Ana Client
Tüm client bileşenlerini koordine eder.
Bileşenler:

network: Network işlemleri
gui: GUI bileşenleri
private_chat_manager: Private chat yönetimi

network_handler.py - Network
Socket bağlantısı ve mesaj iletişimi.
pythondef connect(nickname)         # Server'a bağlan
def start_receiver(callback)  # Mesaj dinle
def send_public_message()     # Public gönder
def send_private_message()    # Private gönder
gui_components.py - GUI
Tkinter widget'larını yönetir.
Widget Yapısı:
Main Window
├── Header (Başlık)
├── Left Panel (User List)
└── Right Panel
    ├── Chat Area
    └── Input Area
private_chat_window.py - Private Chat
Her kullanıcı için ayrı pencere.
pythonclass PrivateChatManager:
    windows = {'Bob': Window, 'Charlie': Window}

📚 API Dokümantasyonu
Mesaj Protokolü
JSON Formatı
json{
    "type": "PUBLIC",
    "sender": "Alice",
    "recipient": null,
    "content": "Hello!",
    "timestamp": "2025-11-19 14:30:45"
}
Mesaj Tipleri
TipSenderRecipientContentPUBLICNicknamenullMesajPRIVATENicknameNicknameMesajSYSTEMnullnullBilgiJOINnullnull"X joined"LEAVEnullnull"X left"USER_LISTnullnull"user1,user2"

🧪 Test Senaryoları
Test 1: Temel Mesajlaşma
1. Server başlat
2. Alice ve Bob bağlan
3. Alice: "Merhaba Bob!"
4. Bob mesajı görür ✅
Test 2: Private Chat
1. Alice, Bob'a double-click
2. Private pencere açılır
3. Alice mesaj gönder
4. Bob'da pencere açılır
5. Mesaj görünür ✅
Test 3: Rate Limit WARNING
1. 12 mesaj gönder (5 saniye)
2. WARNING popup görünür ⚠️
3. Mesaj gönderimi devam eder ✅
Test 4: Rate Limit MUTE
1. 18 mesaj gönder (10 saniye)
2. MUTE olur 🔇
3. Send disabled
4. 30 saniye sonra unmute ✅
Test 5: Rate Limit KICK
1. Muted ol
2. Mesaj göndermeye çalış
3. KICK edilir 🚫
4. Bağlantı kesilir ✅
Test 6: Web Dashboard
1. Server başlat
2. Tarayıcıda http://localhost:8080 aç
3. Dashboard görüntülenir ✅
4. İstatistikler: 0 / 0 / 0 / 0
5. Client bağlan (Alice)
6. Dashboard'da: 1 / 0 / 1 / 0 ✅
7. Alice mesaj gönder
8. Dashboard'da: 1 / 1 / 1 / 0 ✅
9. Log'larda mesaj görünür ✅

🔍 Sorun Giderme
Server Başlamıyor
Hata: Address already in use
bash# Port'u kullanan process'i bul
lsof -i :5000
kill -9 <PID>

# Farklı port kullan
python run_server.py --port 5001
Client Bağlanamıyor
Hata: Connection refused
bash# Server'ın çalıştığını kontrol et
ps aux | grep run_server.py

# Doğru IP/port kullan
python run_client.py --host 127.0.0.1 --port 5000
Türkçe Karakterler Bozuk
bash# Encoding ayarla
export LANG=tr_TR.UTF-8
export LC_ALL=tr_TR.UTF-8

# Windows
chcp 65001
Log Dosyası Çok Büyük
bash# Yedekle ve temizle
cp logs/chat_server.log logs/backup.log
> logs/chat_server.log
Web Dashboard Açılmıyor
Hata: Port 8080 kullanımda
bash# Hangi process kullanıyor bul
netstat -ano | findstr :8080    # Windows
lsof -i :8080                   # Mac/Linux

# Process'i kapat veya farklı port kullan
python run_server.py --http-port 9000
Dashboard Verileri Güncellenmiyor
Çözüm 1: Cache Temizle
Tarayıcıda: Ctrl + Shift + Delete
Hard Refresh: Ctrl + F5 (Windows) / Cmd + Shift + R (Mac)
Çözüm 2: Console Kontrol Et
F12 → Console → Hata var mı kontrol et
Çözüm 3: Server Yeniden Başlat
bashCtrl+C  # Server'ı durdur
python run_server.py  # Tekrar başlat
Dashboard'da Türkçe Karakterler Bozuk
Log dosyasında encoding sorunu. Normal - log dosyası UTF-8 ama bazı karakterler kaçış karakteri olarak görünebilir. Tarayıcıda düzgün görünmeli.

⚙️ Konfigürasyon
Ayarları Değiştirme
common/config.py dosyasını düzenle:
python# Port değiştir
SERVER_PORT = 8000

# Rate limit'i gevşet
RATE_LIMIT_MAX = 20
MUTE_DURATION = 60

# Renkleri değiştir
COLOR_PRIMARY = "#9C27B0"  # Mor
Komut Satırı
bash# Server
python run_server.py --host 0.0.0.0 --port 8000
python run_server.py --http-port 9000  # Web dashboard port

# Client
python run_client.py --host 192.168.1.100 --port 8000
Web Dashboard Özelleştirme
server/web_server.py dosyasında:
python# Renk şeması değiştir
# HTML içinde CSS bölümünde:

# Gradient değiştir
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# Şu şekilde değiştirebilirsin:
background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);

# Auto-refresh süresini değiştir
setInterval(() => {
    updateStats();
    refreshLogs();
}, 3000);  # 3000ms = 3 saniye, değiştirebilirsin

🛠️ Geliştirme
Yeni Özellik Ekleme
1. Config'e ekle:
python# common/config.py
MESSAGE_TYPE_FILE = "FILE"
2. Protocol'e ekle:
python# common/protocol.py
class FileMessage(Message):
    ...
3. Server'a ekle:
python# server/client_handler.py
def _handle_file_message(self, message):
    ...
4. Client'a ekle:
python# client/gui_components.py
def add_file_button(self):
    ...



📸 Screenshots
💬 Chat Client
┌─────────────────────────────────────────┐
│ Chat Client - Alice          [─][□][×] │
├───────────────┬─────────────────────────┤
│ 👥 Online     │ 💬 Public Chat          │
│ Users         │                         │
│ ┌───────────┐ │ ┌─────────────────────┐ │
│ │ Bob       │ │ │[23:37] Alice: Hi!   │ │
│ │ Charlie   │ │ │[23:38] Bob: Hello!  │ │
│ └───────────┘ │ └─────────────────────┘ │
│               │                         │
│ 💡 Double-    │ ✏️ Message: [        ] │
│ click to chat │         [Exit] [Send]  │
└───────────────┴─────────────────────────┘
🌐 Web Dashboard
╔══════════════════════════════════════════════════════╗
║  🚀 Chat Server Dashboard Pro                        ║
║  Real-time monitoring and analytics                  ║
╠══════════════════════════════════════════════════════╣
║  🟢 Server Online    ⏱️ Uptime: 00:15:32            ║
╠═════════╦══════════╦══════════╦═════════════════════╣
║  👥 3   ║  💬 127  ║  🔗 15   ║  ⚠️ 2              ║
║ Online  ║ Messages ║ Connect  ║ Warnings            ║
╠══════════════════════════════════════════════════════╣
║  📋 Server Logs              [🔄 Refresh Logs]      ║
║ ┌────────────────────────────────────────────────┐  ║
║ │ [23:59] PUBLIC  Ahmet: Selam!                 │  ║
║ │ [23:58] PRIVATE Zeynep -> Ali: Gizli mesaj    │  ║
║ │ [23:57] SYSTEM  Ali@127.0.0.1 connected       │  ║
║ └────────────────────────────────────────────────┘  ║
╚══════════════════════════════════════════════════════╝
Dashboard Highlights:

✨ Modern gradient design
📊 Live statistics
🎨 Color-coded logs
⚡ 3-second auto-refresh
📱 Responsive layout


