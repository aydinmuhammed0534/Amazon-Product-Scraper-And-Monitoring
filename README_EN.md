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