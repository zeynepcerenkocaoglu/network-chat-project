# 🚀 Modular Chat Application

Modern, ölçeklenebilir ve bakımı kolay bir Python chat uygulaması. Orijinal monolitik yapıdan modüler bir mimariye dönüştürülmüştür.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Educational-green.svg)](LICENSE)

---

## 📑 İçindekiler

- [Özellikler](#-özellikler)
- [Proje Yapısı](#-proje-yapısı)
- [Kurulum](#-kurulum)
- [Hızlı Başlangıç](#-hızlı-başlangıç)
- [Kullanım Kılavuzu](#-kullanım-kılavuzu)
- [Modül Detayları](#-modül-detayları)
- [API Dokümantasyonu](#-api-dokümantasyonu)
- [Test Senaryoları](#-test-senaryoları)
- [Sorun Giderme](#-sorun-giderme)

---

## ✨ Özellikler

### 🖥️ Server Özellikleri
- **Multi-Client Desteği**: Sınırsız sayıda client aynı anda bağlanabilir
- **Thread-Safe İşlemler**: Her client ayrı thread'de güvenli yönetilir
- **Benzersiz Nickname**: Otomatik suffix ile çakışma önlenir
- **Public Messaging**: Tüm kullanıcılara broadcast
- **Private Messaging**: 1-to-1 özel mesajlaşma
- **JOIN/LEAVE Events**: Kullanıcı bildirimleri
- **Rate Limiting**: 3 seviyeli spam koruması (WARNING/MUTE/KICK)
- **Kapsamlı Loglama**: Tüm aktivitelerin kaydı
- **Real-time İstatistikler**: 30 saniyede bir istatistik

### 💻 Client Özellikleri
- **Modern GUI**: Tkinter tabanlı kullanıcı dostu arayüz
- **Renkli Mesajlar**: Mesaj tiplerine göre renklendirilmiş görünüm
- **Online User List**: Çevrimiçi kullanıcıları görüntüleme
- **Private Chat Windows**: Ayrı private chat pencereleri
- **Double-Click Private**: Kullanıcıya çift tıklayarak private chat
- **Rate Limit Handling**: Visual feedback ve otomatik unmute
- **Timestamp Support**: Her mesajda zaman damgası

---

## 📁 Proje Yapısı

```
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
│   └── rate_limiter.py     # Spam koruması
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
```

---

## 🔧 Kurulum

### Gereksinimler
- **Python**: 3.8+
- **Ek Kütüphane**: Yok! (Sadece Python standard library)

```bash
# Python versiyonunu kontrol et
python --version

# Projeyi indir
cd chat_project
```

---

## 🚀 Hızlı Başlangıç

### Server'ı Başlat
```bash
python run_server.py
```

**Çıktı:**
```
============================================================
🚀 CHAT SERVER - MODULAR VERSION
============================================================
✅ Server listening on 127.0.0.1:5000
📝 Log file: logs/chat_server.log
⏰ Started at: 14:30:45
============================================================
```

### Client'ları Başlat
```bash
# Terminal 1 - Alice
python run_client.py

# Terminal 2 - Bob
python run_client.py
```

---

## 📖 Kullanım Kılavuzu

### Public Mesaj Gönderme
1. Message input alanına mesajını yaz
2. **Enter** veya **Send** butonuna tıkla
3. Mesaj tüm kullanıcılara gönderilir

### Private Mesaj Gönderme
1. Sol paneldeki kullanıcıya **çift tıkla**
2. Açılan pencerede mesajını yaz
3. **Enter** veya **Send**

### Rate Limit Sistemi

| Durum | Koşul | Sonuç |
|-------|-------|-------|
| Normal | < 10 mesaj/5s | ✅ Normal |
| WARNING | 10+ mesaj/5s | ⚠️ Uyarı popup |
| MUTE | 15+ mesaj/10s | 🔇 30 saniye susturma |
| KICK | Muted iken mesaj | 🚫 Bağlantı kesilir |

---

## 🔬 Modül Detayları

### Common Modülleri

#### `config.py` - Konfigürasyon
Tüm proje ayarlarını merkezi olarak yönetir.

```python
# Server Ayarları
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

# Rate Limiting
RATE_LIMIT_WINDOW = 5  # saniye
RATE_LIMIT_MAX = 10    # mesaj
MUTE_DURATION = 30     # saniye

# Renkler
COLOR_PRIMARY = "#2196F3"
COLOR_SUCCESS = "#4CAF50"
```

#### `protocol.py` - Mesaj Protokolü
JSON tabanlı mesaj iletişimi.

**Message Sınıfı:**
```python
class Message:
    def __init__(self, msg_type, sender, recipient, content, timestamp)
    def to_dict()  # JSON'a çevir
    @staticmethod from_dict(data)  # JSON'dan oluştur
```

**Mesaj Tipleri:**
- `PUBLIC`: Herkese mesaj
- `PRIVATE`: Özel mesaj
- `SYSTEM`: Sistem mesajı
- `JOIN/LEAVE`: Katılım/ayrılma
- `WARNING/MUTE/KICK`: Rate limit

#### `utils.py` - Yardımcı Fonksiyonlar
```python
get_timestamp()              # "2025-11-19 14:30:45"
generate_random_suffix()     # "123"
validate_nickname(nick)      # (True, "")
format_message_display(...)  # "[14:30] Alice: Hi"
```

### Server Modülleri

#### `chat_server.py` - Ana Server
**Sorumluluklar:**
- Client bağlantılarını kabul
- Mesaj broadcast
- Modül koordinasyonu

**Önemli Methodlar:**
```python
def start()                  # Server'ı başlat
def register_client()        # Client kaydet
def broadcast_message()      # Mesaj broadcast
def send_private_message()   # Private mesaj
```

#### `client_handler.py` - Client Yöneticisi
Her client için ayrı thread'de çalışır.

**Yaşam Döngüsü:**
```
Bağlantı → Nickname → Kayıt → JOIN → Mesaj Loop → Cleanup → LEAVE
```

#### `logger.py` - Log Sistemi
**Log Formatı:**
```
[2025-11-19 14:30:45] PUBLIC | Alice: Hello!
[2025-11-19 14:30:50] PRIVATE | Alice -> Bob: Secret
[2025-11-19 14:31:00] SYSTEM | Charlie connected
```

#### `rate_limiter.py` - Spam Koruması
**Algoritma**: Sliding Window

| Level | Süre | Mesaj | Aksiyon |
|-------|------|-------|---------|
| 1 | 5s | 10 | ⚠️ WARNING |
| 2 | 10s | 15 | 🔇 MUTE (30s) |
| 3 | Muted | 1 | 🚫 KICK |

### Client Modülleri

#### `chat_client.py` - Ana Client
Tüm client bileşenlerini koordine eder.

**Bileşenler:**
- `network`: Network işlemleri
- `gui`: GUI bileşenleri  
- `private_chat_manager`: Private chat yönetimi

#### `network_handler.py` - Network
Socket bağlantısı ve mesaj iletişimi.

```python
def connect(nickname)         # Server'a bağlan
def start_receiver(callback)  # Mesaj dinle
def send_public_message()     # Public gönder
def send_private_message()    # Private gönder
```

#### `gui_components.py` - GUI
Tkinter widget'larını yönetir.

**Widget Yapısı:**
```
Main Window
├── Header (Başlık)
├── Left Panel (User List)
└── Right Panel
    ├── Chat Area
    └── Input Area
```

#### `private_chat_window.py` - Private Chat
Her kullanıcı için ayrı pencere.

```python
class PrivateChatManager:
    windows = {'Bob': Window, 'Charlie': Window}
```

---

## 📚 API Dokümantasyonu

### Mesaj Protokolü

#### JSON Formatı
```json
{
    "type": "PUBLIC",
    "sender": "Alice",
    "recipient": null,
    "content": "Hello!",
    "timestamp": "2025-11-19 14:30:45"
}
```

#### Mesaj Tipleri

| Tip | Sender | Recipient | Content |
|-----|--------|-----------|---------|
| PUBLIC | Nickname | null | Mesaj |
| PRIVATE | Nickname | Nickname | Mesaj |
| SYSTEM | null | null | Bilgi |
| JOIN | null | null | "X joined" |
| LEAVE | null | null | "X left" |
| USER_LIST | null | null | "user1,user2" |

---

## 🧪 Test Senaryoları

### Test 1: Temel Mesajlaşma
```
1. Server başlat
2. Alice ve Bob bağlan
3. Alice: "Merhaba Bob!"
4. Bob mesajı görür ✅
```

### Test 2: Private Chat
```
1. Alice, Bob'a double-click
2. Private pencere açılır
3. Alice mesaj gönder
4. Bob'da pencere açılır
5. Mesaj görünür ✅
```

### Test 3: Rate Limit WARNING
```
1. 12 mesaj gönder (5 saniye)
2. WARNING popup görünür ⚠️
3. Mesaj gönderimi devam eder ✅
```

### Test 4: Rate Limit MUTE
```
1. 18 mesaj gönder (10 saniye)
2. MUTE olur 🔇
3. Send disabled
4. 30 saniye sonra unmute ✅
```

### Test 5: Rate Limit KICK
```
1. Muted ol
2. Mesaj göndermeye çalış
3. KICK edilir 🚫
4. Bağlantı kesilir ✅
```

---

## 🔍 Sorun Giderme

### Server Başlamıyor
**Hata**: `Address already in use`

```bash
# Port'u kullanan process'i bul
lsof -i :5000
kill -9 <PID>

# Farklı port kullan
python run_server.py --port 5001
```

### Client Bağlanamıyor
**Hata**: `Connection refused`

```bash
# Server'ın çalıştığını kontrol et
ps aux | grep run_server.py

# Doğru IP/port kullan
python run_client.py --host 127.0.0.1 --port 5000
```

### Türkçe Karakterler Bozuk
```bash
# Encoding ayarla
export LANG=tr_TR.UTF-8
export LC_ALL=tr_TR.UTF-8

# Windows
chcp 65001
```

### Log Dosyası Çok Büyük
```bash
# Yedekle ve temizle
cp logs/chat_server.log logs/backup.log
> logs/chat_server.log
```

---

## ⚙️ Konfigürasyon

### Ayarları Değiştirme
`common/config.py` dosyasını düzenle:

```python
# Port değiştir
SERVER_PORT = 8000

# Rate limit'i gevşet
RATE_LIMIT_MAX = 20
MUTE_DURATION = 60

# Renkleri değiştir
COLOR_PRIMARY = "#9C27B0"  # Mor
```

### Komut Satırı
```bash
# Server
python run_server.py --host 0.0.0.0 --port 8000

# Client
python run_client.py --host 192.168.1.100 --port 8000
```

---

## 🛠️ Geliştirme

### Yeni Özellik Ekleme

**1. Config'e ekle:**
```python
# common/config.py
MESSAGE_TYPE_FILE = "FILE"
```

**2. Protocol'e ekle:**
```python
# common/protocol.py
class FileMessage(Message):
    ...
```

**3. Server'a ekle:**
```python
# server/client_handler.py
def _handle_file_message(self, message):
    ...
```

**4. Client'a ekle:**
```python
# client/gui_components.py
def add_file_button(self):
    ...
```

---






*
