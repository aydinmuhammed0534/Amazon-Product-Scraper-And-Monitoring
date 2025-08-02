# Amazon Price Tracker

Monitors Amazon products and sends automatic email alerts when different sellers offer lower prices.

## Features

- **Amazon Product Monitoring**: Track any Amazon product by URL
- **Price Comparison**: Compare prices from different sellers
- **Email Alerts**: Automatic email notifications when prices drop
- **Target Price**: Set alerts for specific price points
- **Automatic Monitoring**: Periodic checks (default: every 6 hours)
- **Price History**: SQLite database with price records
- **Easy Usage**: Add products with a single command

## Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Configure email settings
python setup.py
```

### 2. Add Product

```bash
# Add product with single command
python quick_add.py https://www.amazon.com/dp/B08N5WRWNW

# Add with target price
python quick_add.py https://www.amazon.com/dp/B08N5WRWNW 299.99
```

### 3. Start Monitoring

```bash
# Start automatic monitoring
python start_monitoring.py
```

## Detailed Usage

### Manual Control

```bash
# Main program (with menu)
python amazon_price_tracker.py
```

Menu options:
1. Add new product
2. List tracked products  
3. Manual price check
4. Start monitoring
5. Exit

### Email Configuration

Configure your email settings in `config.json`:

```json
{
  "email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your_email@gmail.com",
    "sender_password": "your_app_password",
    "receiver_email": "recipient@gmail.com"
  }
}
```

#### Important Note for Gmail

If using Gmail:
1. Enable 2FA
2. Create an [App Password](https://support.google.com/accounts/answer/185833)
3. Use the app password instead of your regular password

### Monitoring Settings

```json
{
  "tracking": {
    "check_interval_hours": 6,        // Check interval in hours
    "price_drop_threshold": 5.0,      // Alert on 5% price drop
    "max_retries": 3,                 // Retry count on errors
    "delay_between_requests": 2       // Delay between requests
  }
}
```

## Supported Data

### Collected Information
- Product name and ASIN
- Prices from different sellers
- Stock status
- Prime membership status
- Shipping information
- Price history

### Email Alerts
- Price drop notifications
- Target price alerts
- Comparative price tables
- Direct product links

## Scripts

| Script | Description |
|--------|-------------|
| `amazon_price_tracker.py` | Main program (menu interface) |
| `quick_add.py` | Single command product addition |
| `start_monitoring.py` | Automatic monitoring starter |
| `setup.py` | Email and settings configuration |

## File Structure

```
amazon-price-tracker/
├── amazon_price_tracker.py    # Main system
├── quick_add.py              # Quick product addition
├── start_monitoring.py       # Monitoring starter
├── setup.py                  # Setup script
├── config.json              # Configuration
├── requirements.txt         # Python dependencies
├── price_tracker.db         # SQLite database (auto-created)
├── price_tracker.log        # Log file (auto-created)
├── LICENSE                  # MIT License
├── README.md               # Turkish documentation
└── README_EN.md           # This file
```

## Example Usage Scenarios

### Scenario 1: Single Product Tracking
```bash
# Track iPhone, alert when below $800
python quick_add.py https://www.amazon.com/dp/B09G9FPHY6 800

# Start monitoring
python start_monitoring.py
```

### Scenario 2: Multiple Product Tracking
```bash
# Add multiple products
python quick_add.py https://www.amazon.com/dp/B08N5WRWNW 300
python quick_add.py https://www.amazon.com/dp/B09G9FPHY6 800
python quick_add.py https://www.amazon.com/dp/B08N5WRWNW 400

# Monitor all at once
python start_monitoring.py
```

### Scenario 3: Manual Check
```bash
# Check once manually
python amazon_price_tracker.py
# Select "3. Manual price check" from menu
```

## Important Warnings

### Legal Considerations
- **Terms of Service**: Read Amazon's [terms of service](https://www.amazon.com/gp/help/customer/display.html?nodeId=508088)
- **robots.txt**: Comply with [Amazon robots.txt](https://www.amazon.com/robots.txt)
- **Personal Use**: Use only for personal purposes

### Technical Limitations
- **Rate Limiting**: Delays between requests to avoid overloading
- **IP Blocking**: May be temporarily blocked with excessive requests
- **User-Agent**: Different browser identities are used

## Troubleshooting

### Common Errors

**1. Email Not Sending**
```bash
# Test email settings
python setup.py
# Option 2: Test email settings
```

**2. Cannot Fetch Product Info**
```python
# Amazon's site structure may have changed
# Check log file: price_tracker.log
```

**3. 403/429 HTTP Errors**
```python
# You may have hit rate limits
# Increase delay_between_requests in config.json
```

### Debug Mode

For detailed logging in `amazon_price_tracker.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Future Features

- [ ] Telegram bot support
- [ ] Web dashboard
- [ ] Multi-country support (.com, .co.uk, .de)
- [ ] Graphical price analysis
- [ ] Desktop notifications
- [ ] SMS alerts

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

**Copyright (c) 2025 aydinmuhammed0534**

See `LICENSE` file for details.

## Acknowledgments

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing
- [Requests](https://docs.python-requests.org/) - HTTP requests
- [Schedule](https://schedule.readthedocs.io/) - Job scheduling

---

**Disclaimer**: This project is for educational purposes. The project maintainers are not responsible for any issues arising from usage that violates Amazon's terms of service.

---

**Amazon Price Tracker** - Catch the advantage in shopping!

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