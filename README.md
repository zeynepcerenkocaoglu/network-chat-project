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
- [Web Dashboard](#-web-dashboard)
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

### 💻 Client Özellikleri

- **Modern GUI**: Tkinter tabanlı kullanıcı dostu arayüz
- **Renkli Mesajlar**: Mesaj tiplerine göre renklendirilmiş görünüm
- **Online User List**: Çevrimiçi kullanıcıları görüntüleme
- **Private Chat Windows**: Ayrı private chat pencereleri
- **Double-Click Private**: Kullanıcıya çift tıklayarak private chat
- **Rate Limit Handling**: Visual feedback ve otomatik unmute

### 🌐 Web Dashboard Özellikleri

- **Real-time Monitoring**: Canlı server izleme ve istatistikler
- **Beautiful UI**: Modern gradient tasarım ve koyu tema
- **Live Stats**: Anlık kullanıcı, mesaj ve bağlantı sayıları
- **Colorful Logs**: Renkli log görüntüleme
- **Auto-refresh**: Her 3 saniyede otomatik güncelleme
- **Responsive Design**: Mobil uyumlu arayüz

---

## 📁 Proje Yapısı

```text
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

### 1. Server'ı Başlat

```bash
python run_server.py
```

**Çıktı:**
```
============================================================
🚀 CHAT SERVER - MODULAR VERSION
============================================================
✅ Server listening on 127.0.0.1:5000
🌐 HTTP Server listening on http://127.0.0.1:8080
📝 Log file: logs/chat_server.log
============================================================
📊 Open web dashboard: http://localhost:8080
============================================================
```

### 2. Client'ları Başlat

```bash
# Terminal 1 - Alice
python run_client.py

# Terminal 2 - Bob
python run_client.py
```

### 3. Web Dashboard'u Aç

Tarayıcınızda:
```
http://localhost:8080
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

## 🌐 Web Dashboard

### Dashboard'a Erişim

```
http://localhost:8080
```

### Dashboard Bileşenleri

#### 1. Server Status
- 🟢 **Server Online**: Server aktif durumda
- ⏱️ **Uptime**: Server çalışma süresi

#### 2. Canlı İstatistikler
- 👥 **Online Users**: Anlık bağlı kullanıcı sayısı
- 💬 **Total Messages**: Toplam mesaj sayısı
- 🔗 **Connections**: Toplam bağlantı sayısı
- ⚠️ **Warnings**: Rate limit uyarı sayısı

#### 3. Server Logs
- 🔵 **SYSTEM**: Sistem olayları (JOIN, LEAVE)
- 🟢 **PUBLIC**: Genel mesajlar
- 🟠 **PRIVATE**: Özel mesajlar
- 🟡 **WARNING**: Rate limit uyarıları

### API Endpoint'leri

**İstatistikler:**
```http
GET /api/stats
```

Response:
```json
{
  "connected_clients": 3,
  "total_messages": 127,
  "total_connections": 15,
  "warnings": 2
}
```

**Loglar:**
```http
GET /api/logs
```

Response:
```json
[
  {
    "timestamp": "14:30:45",
    "type": "SYSTEM",
    "message": "Alice@127.0.0.1 connected"
  }
]
```

### Port Değiştirme

```bash
python run_server.py --http-port 9000
```

---

## 🧪 Test Senaryoları

### Test 1: Temel Mesajlaşma
1. Server başlat
2. Alice ve Bob bağlan
3. Alice: "Merhaba Bob!"
4. Bob mesajı görür ✅

### Test 2: Private Chat
1. Alice, Bob'a double-click
2. Private pencere açılır
3. Mesaj gönder ✅

### Test 3: Web Dashboard
1. Server başlat
2. Tarayıcıda `http://localhost:8080` aç
3. Dashboard görüntülenir ✅
4. İstatistikler: 0 / 0 / 0 / 0
5. Client bağlan → İstatistikler güncellenir ✅

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
```

### Web Dashboard Açılmıyor

**Hata**: Port 8080 kullanımda

```bash
# Windows
netstat -ano | findstr :8080

# Mac/Linux
lsof -i :8080

# Farklı port kullan
python run_server.py --http-port 9000
```

### Dashboard Verileri Güncellenmiyor

**Çözüm 1**: Cache Temizle
- Tarayıcıda: `Ctrl + Shift + Delete`
- Hard Refresh: `Ctrl + F5` (Windows) / `Cmd + Shift + R` (Mac)

**Çözüm 2**: Server Yeniden Başlat
```bash
# Ctrl+C ile durdur
python run_server.py
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
```

### Komut Satırı

```bash
# Server
python run_server.py --host 0.0.0.0 --port 8000
python run_server.py --http-port 9000

# Client
python run_client.py --host 192.168.1.100 --port 8000
```




</div>
