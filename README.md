# 🛒 Amazon Fiyat İzleyici

Amazon'daki ürünleri izler ve farklı satıcılar daha ucuz fiyata satarsa otomatik email uyarısı gönderir.

## ✨ Özellikler

- 🔍 **Amazon Ürün İzleme**: Herhangi bir Amazon ürününü URL ile izleme
- 💰 **Fiyat Karşılaştırma**: Farklı satıcıların fiyatlarını karşılaştırma
- 📧 **Email Uyarıları**: Fiyat düştüğünde otomatik mail gönderme
- 🎯 **Hedef Fiyat**: Belirli bir fiyata ulaştığında uyarı
- ⏰ **Otomatik İzleme**: Periyodik kontrol (6 saatte bir varsayılan)
- 📊 **Fiyat Geçmişi**: SQLite veritabanında fiyat kayıtları
- 🚀 **Kolay Kullanım**: Tek komutla ürün ekleme

## 🚀 Hızlı Başlangıç

### 1. Kurulum

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Email ayarlarını yapılandır
python setup.py
```

### 2. Ürün Ekle

```bash
# Tek komutla ürün ekle
python quick_add.py https://www.amazon.com/dp/B08N5WRWNW

# Hedef fiyat ile ekle
python quick_add.py https://www.amazon.com/dp/B08N5WRWNW 299.99
```

### 3. Monitoring Başlat

```bash
# Otomatik izlemeyi başlat
python start_monitoring.py
```

## 📋 Detaylı Kullanım

### Manuel Kontrol

```bash
# Ana program (menü ile)
python amazon_price_tracker.py
```

Menü seçenekleri:
1. ✅ Yeni ürün ekle
2. 📦 İzlenen ürünleri listele  
3. 🔍 Manuel fiyat kontrolü
4. 🚀 Monitoring başlat
5. 🚪 Çıkış

### Email Ayarları

`config.json` dosyasında email ayarlarınızı yapılandırın:

```json
{
  \"email\": {
    \"smtp_server\": \"smtp.gmail.com\",
    \"smtp_port\": 587,
    \"sender_email\": \"your_email@gmail.com\",
    \"sender_password\": \"your_app_password\",
    \"receiver_email\": \"recipient@gmail.com\"
  }
}
```

#### Gmail İçin Önemli Not

Gmail kullanıyorsanız:
1. 2FA'yı aktif edin
2. [Uygulama şifresi](https://support.google.com/accounts/answer/185833) oluşturun
3. Normal şifre yerine uygulama şifresini kullanın

### İzleme Ayarları

```json
{
  \"tracking\": {
    \"check_interval_hours\": 6,        // Kaç saatte bir kontrol
    \"price_drop_threshold\": 5.0,      // %5 düşüşte uyarı
    \"max_retries\": 3,                 // Hata durumunda tekrar sayısı
    \"delay_between_requests\": 2       // İstekler arası bekleme
  }
}
```

## 📊 Desteklenen Veriler

### Toplanan Bilgiler
- ✅ Ürün adı ve ASIN
- ✅ Farklı satıcıların fiyatları
- ✅ Stok durumu
- ✅ Prime üyelik durumu
- ✅ Kargo bilgileri
- ✅ Fiyat geçmişi

### Email Uyarıları
- 💰 Fiyat düşüşü uyarıları
- 🎯 Hedef fiyat uyarıları
- 📊 Karşılaştırmalı fiyat tablosu
- 🔗 Direkt ürün linkleri

## 🛠️ Script'ler

| Script | Açıklama |
|--------|----------|
| `amazon_price_tracker.py` | Ana program (menülü interface) |
| `quick_add.py` | Tek komutla ürün ekleme |
| `start_monitoring.py` | Otomatik monitoring başlatıcı |
| `setup.py` | Email ve ayar yapılandırması |

## 📁 Dosya Yapısı

```
amazon-price-tracker/
├── amazon_price_tracker.py    # Ana sistem
├── quick_add.py              # Hızlı ürün ekleme
├── start_monitoring.py       # Monitoring başlatıcı
├── setup.py                  # Kurulum script'i
├── config.json              # Konfigürasyon
├── requirements.txt         # Python bağımlılıkları
├── price_tracker.db         # SQLite veritabanı (otomatik)
├── price_tracker.log        # Log dosyası (otomatik)
└── README.md               # Bu dosya
```

## 💡 Örnek Kullanım Senaryoları

### Senaryo 1: Tekil Ürün İzleme
```bash
# iPhone izle, $800'ın altına düşerse uyar
python quick_add.py https://www.amazon.com/dp/B09G9FPHY6 800

# Monitoring başlat
python start_monitoring.py
```

### Senaryo 2: Çoklu Ürün İzleme
```bash
# Birden fazla ürün ekle
python quick_add.py https://www.amazon.com/dp/B08N5WRWNW 300
python quick_add.py https://www.amazon.com/dp/B09G9FPHY6 800
python quick_add.py https://www.amazon.com/dp/B08N5WRWNW 400

# Hepsini birden izle
python start_monitoring.py
```

### Senaryo 3: Manuel Kontrol
```bash
# Sadece bir kez kontrol et
python amazon_price_tracker.py
# Menüden \"3. Manuel fiyat kontrolü\" seç
```

## 🚨 Önemli Uyarılar

### Yasal Konular
- ⚖️ **Kullanım Şartları**: Amazon'ın [hizmet şartlarını](https://www.amazon.com/gp/help/customer/display.html?nodeId=508088) okuyun
- 🤖 **robots.txt**: [Amazon robots.txt](https://www.amazon.com/robots.txt) dosyasına uyun
- 📚 **Kişisel Kullanım**: Sadece kişisel amaçlar için kullanın

### Teknik Sınırlamalar
- ⏱️ **Rate Limiting**: Aşırı yük oluşturmamak için istekler arası bekleme
- 🔄 **IP Engelleme**: Çok fazla istek durumunda geçici engellenebilirsiniz
- 📱 **User-Agent**: Farklı tarayıcı kimlikler kullanılır

## 🔧 Sorun Giderme

### Yaygın Hatalar

**1. Email Gönderilmiyor**
```bash
# Email ayarlarını test et
python setup.py
# Seçenek 2: Email ayarlarını test et
```

**2. Ürün Bilgisi Alınamıyor**
```python
# Amazon'ın site yapısı değişmiş olabilir
# Log dosyasını kontrol et: price_tracker.log
```

**3. 403/429 HTTP Hataları**
```python
# Rate limit'e takılmış olabilirsiniz
# config.json'da delay_between_requests değerini artırın
```

### Debug Modu

Detaylı log için `amazon_price_tracker.py` içinde:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 🎯 Gelecek Özellikler

- [ ] 📱 Telegram bot desteği
- [ ] 📊 Web dashboard
- [ ] 🌍 Çoklu ülke desteği (.com, .co.uk, .de)
- [ ] 📈 Grafik ile fiyat analizi
- [ ] 🔔 Desktop bildirimleri
- [ ] 📲 SMS uyarıları

## 🤝 Katkıda Bulunma

1. Fork'layın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit'leyin (`git commit -m 'Add amazing feature'`)
4. Push'layın (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📜 Lisans

Bu proje MIT lisansı altındadır. 

**Copyright (c) 2025 aydinmuhammed0534**

Detaylar için `LICENSE` dosyasına bakın.

## 🙏 Teşekkürler

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing
- [Requests](https://docs.python-requests.org/) - HTTP requests
- [Schedule](https://schedule.readthedocs.io/) - Job scheduling

---

**⚠️ Sorumluluk Reddi**: Bu proje eğitim amaçlıdır. Amazon'ın hizmet şartlarına aykırı kullanımdan doğacak sorunlardan proje sahipleri sorumlu değildir.

---

🛒 **Amazon Fiyat İzleyici** ile alışverişte avantajı yakalayın! 💰