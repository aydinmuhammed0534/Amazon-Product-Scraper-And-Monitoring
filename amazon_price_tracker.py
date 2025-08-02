2#!/usr/bin/env python3
"""
Amazon Price Tracker
This script monitors Amazon products and sends email alerts when different sellers offer lower prices.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import schedule
import re
import logging
from urllib.parse import urljoin, urlparse
import os
from typing import List, Dict, Optional, Tuple
import random

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('price_tracker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AmazonPriceTracker:
    def __init__(self, config_file='config.json'):
        """Amazon Price Tracker initializer"""
        self.config = self.load_config(config_file)
        self.session = requests.Session()
        self.setup_session()
        self.init_database()
        
    def load_config(self, config_file: str) -> Dict:
        """Load configuration file"""
        default_config = {
            "email": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "",
                "sender_password": "",
                "receiver_email": ""
            },
            "tracking": {
                "check_interval_hours": 6,
                "price_drop_threshold": 5.0,
                "max_retries": 3,
                "delay_between_requests": 2
            },
            "amazon": {
                "base_url": "https://www.amazon.com",
                "user_agents": [
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                ]
            }
        }
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    # Merge with defaults
                    default_config.update(user_config)
            except Exception as e:
                logger.warning(f"Config file could not be loaded: {e}, using default settings")
        else:
            # Create default config file
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            logger.info(f"Default config file created: {config_file}")
        
        return default_config
    
    def setup_session(self):
        """Setup HTTP session settings"""
        self.session.headers.update({
            'User-Agent': random.choice(self.config['amazon']['user_agents']),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect('price_tracker.db')
        cursor = conn.cursor()
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                title TEXT,
                asin TEXT,
                target_price REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_checked TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # Price history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                seller_name TEXT,
                price REAL,
                availability TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Email history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                email_type TEXT,
                sent_to TEXT,
                subject TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized")
    
    def extract_asin_from_url(self, url: str) -> Optional[str]:
        """Extract ASIN from Amazon URL"""
        patterns = [
            r'/dp/([A-Z0-9]{10})',
            r'/gp/product/([A-Z0-9]{10})',
            r'asin=([A-Z0-9]{10})',
            r'/([A-Z0-9]{10})(?:/|$)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def clean_url(self, url: str) -> str:
        """Clean URL (remove tracking parameters)"""
        if not url.startswith('http'):
            url = f"https://www.amazon.com/dp/{url}" if len(url) == 10 else url
        
        # Remove tracking parameters
        clean_url = url.split('?')[0].split('#')[0]
        return clean_url
    
    def get_product_info(self, url: str) -> Dict:
        """Fetch product information from Amazon"""
        url = self.clean_url(url)
        asin = self.extract_asin_from_url(url)
        
        if not asin:
            raise ValueError("Invalid Amazon URL")
        
        # Rotate user agent
        self.session.headers['User-Agent'] = random.choice(self.config['amazon']['user_agents'])
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            product_info = {
                'asin': asin,
                'url': url,
                'title': self._extract_title(soup),
                'sellers': self._extract_sellers(soup, asin),
                'main_price': self._extract_main_price(soup),
                'availability': self._extract_availability(soup),
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Product info fetched: {product_info['title']}")
            return product_info
            
        except Exception as e:
            logger.error(f"Could not fetch product info: {e}")
            raise
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract product title"""
        selectors = [
            '#productTitle',
            '.product-title',
            'h1.a-size-large',
            '[data-feature-name="title"] h1'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        return "Title not found"
    
    def _extract_main_price(self, soup: BeautifulSoup) -> Optional[float]:
        """Extract main price"""
        price_selectors = [
            '.a-price-current .a-offscreen',
            '.a-price .a-offscreen',
            '#corePrice_feature_div .a-price .a-offscreen',
            '.a-price-whole'
        ]
        
        for selector in price_selectors:
            element = soup.select_one(selector)
            if element:
                price_text = element.get_text(strip=True)
                price = self._parse_price(price_text)
                if price:
                    return price
        
        return None
    
    def _extract_availability(self, soup: BeautifulSoup) -> str:
        """Extract stock status"""
        availability_selectors = [
            '#availability span',
            '.a-color-success',
            '.a-color-state',
            '[data-feature-name="availability"] span'
        ]
        
        for selector in availability_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        return "Status unknown"
    
    def _extract_sellers(self, soup: BeautifulSoup, asin: str) -> List[Dict]:
        """Extract different sellers and their prices"""
        sellers = []
        
        # Main seller (Amazon or default)
        main_price = self._extract_main_price(soup)
        if main_price:
            sellers.append({
                'name': 'Amazon',
                'price': main_price,
                'shipping': 'Free',
                'prime': True
            })
        
        # Extract other sellers from "More Buying Choices" section
        seller_elements = soup.select('#aod-offer-list [data-aod-offer-id]')
        for element in seller_elements:
            try:
                seller_info = self._parse_seller_element(element)
                if seller_info:
                    sellers.append(seller_info)
            except Exception as e:
                logger.warning(f"Could not parse seller info: {e}")
                continue
        
        # If no sellers found, try alternative methods
        if len(sellers) <= 1:
            sellers.extend(self._try_alternative_seller_extraction(soup))
        
        return sellers
    
    def _parse_seller_element(self, element) -> Optional[Dict]:
        """Extract information from seller element"""
        seller = {}
        
        # Seller name
        seller_name = element.select_one('[aria-label*="seller"]')
        if seller_name:
            seller['name'] = seller_name.get_text(strip=True)
        
        # Fiyat
        price_element = element.select_one('.a-price .a-offscreen')
        if price_element:
            price = self._parse_price(price_element.get_text(strip=True))
            if price:
                seller['price'] = price
        
        # Shipping info
        shipping_element = element.select_one('[data-csa-c-content-id="aod-delivery-price"]')
        if shipping_element:
            seller['shipping'] = shipping_element.get_text(strip=True)
        
        # Prime
        prime_element = element.select_one('.aod-prime-logo')
        seller['prime'] = prime_element is not None
        
        return seller if seller.get('price') else None
    
    def _try_alternative_seller_extraction(self, soup: BeautifulSoup) -> List[Dict]:
        """Alternative seller extraction methods"""
        sellers = []
        
        # Try from JSON-LD structured data
        json_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and data.get('@type') == 'Product':
                    offers = data.get('offers', {})
                    if isinstance(offers, list):
                        for offer in offers:
                            seller = self._parse_json_offer(offer)
                            if seller:
                                sellers.append(seller)
            except:
                continue
        
        return sellers
    
    def _parse_json_offer(self, offer: Dict) -> Optional[Dict]:
        """Extract seller info from JSON offer"""
        try:
            return {
                'name': offer.get('seller', {}).get('name', 'Unknown'),
                'price': float(offer.get('price', 0)),
                'shipping': 'Unknown',
                'prime': False
            }
        except:
            return None
    
    def _parse_price(self, price_text: str) -> Optional[float]:
        """Convert price text to number"""
        if not price_text:
            return None
        
        # Remove currency symbols and clean
        price_clean = re.sub(r'[^\d.,]', '', price_text)
        price_clean = price_clean.replace(',', '')
        
        try:
            return float(price_clean)
        except ValueError:
            return None
    
    def add_product(self, url: str, target_price: Optional[float] = None) -> int:
        """Add product to track"""
        try:
            product_info = self.get_product_info(url)
            
            conn = sqlite3.connect('price_tracker.db')
            cursor = conn.cursor()
            
            # Add product to database
            cursor.execute('''
                INSERT OR REPLACE INTO products (url, title, asin, target_price)
                VALUES (?, ?, ?, ?)
            ''', (
                product_info['url'],
                product_info['title'],
                product_info['asin'],
                target_price
            ))
            
            product_id = cursor.lastrowid
            
            # Save initial price information
            for seller in product_info['sellers']:
                cursor.execute('''
                    INSERT INTO price_history (product_id, seller_name, price, availability)
                    VALUES (?, ?, ?, ?)
                ''', (
                    product_id,
                    seller['name'],
                    seller['price'],
                    product_info['availability']
                ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Product added: {product_info['title']} (ID: {product_id})")
            return product_id
            
        except Exception as e:
            logger.error(f"Could not add product: {e}")
            raise
    
    def check_price_changes(self, product_id: int) -> List[Dict]:
        """Check price changes"""
        conn = sqlite3.connect('price_tracker.db')
        cursor = conn.cursor()
        
        # Get product information
        cursor.execute('SELECT * FROM products WHERE id = ? AND is_active = TRUE', (product_id,))
        product = cursor.fetchone()
        
        if not product:
            return []
        
        try:
            # Fetch current prices
            current_info = self.get_product_info(product[1])  # URL
            
            # Get previous lowest price
            cursor.execute('''
                SELECT MIN(price) FROM price_history 
                WHERE product_id = ? AND timestamp > datetime('now', '-7 days')
            ''', (product_id,))
            previous_min_price = cursor.fetchone()[0] or float('inf')
            
            price_changes = []
            
            # Check for each seller
            for seller in current_info['sellers']:
                current_price = seller['price']
                
                # Check if there's a price drop
                if current_price < previous_min_price:
                    price_drop = previous_min_price - current_price
                    percentage_drop = (price_drop / previous_min_price) * 100
                    
                    price_changes.append({
                        'product_id': product_id,
                        'product_title': product[2],  # title
                        'seller_name': seller['name'],
                        'current_price': current_price,
                        'previous_min_price': previous_min_price,
                        'price_drop': price_drop,
                        'percentage_drop': percentage_drop,
                        'target_price': product[4],  # target_price
                        'is_target_reached': current_price <= product[4] if product[4] else False
                    })
                
                # Save new price
                cursor.execute('''
                    INSERT INTO price_history (product_id, seller_name, price, availability)
                    VALUES (?, ?, ?, ?)
                ''', (
                    product_id,
                    seller['name'],
                    current_price,
                    current_info['availability']
                ))
            
            # Update last check time
            cursor.execute('''
                UPDATE products SET last_checked = CURRENT_TIMESTAMP WHERE id = ?
            ''', (product_id,))
            
            conn.commit()
            conn.close()
            
            return price_changes
            
        except Exception as e:
            logger.error(f"Error in price check: {e}")
            conn.close()
            return []
    
    def send_price_alert(self, price_changes: List[Dict]):
        """Send price alert email"""
        if not price_changes:
            return
        
        email_config = self.config['email']
        
        if not all([email_config['sender_email'], email_config['sender_password'], email_config['receiver_email']]):
            logger.warning("Email configuration incomplete, cannot send email")
            return
        
        try:
            # Create email content
            subject = f"Amazon Price Alert - {len(price_changes)} products!"
            body = self._create_email_body(price_changes)
            
            # Send email
            msg = MIMEMultipart()
            msg['From'] = email_config['sender_email']
            msg['To'] = email_config['receiver_email']
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            server.login(email_config['sender_email'], email_config['sender_password'])
            
            text = msg.as_string()
            server.sendmail(email_config['sender_email'], email_config['receiver_email'], text)
            server.quit()
            
            # Log email to history
            self._log_email_sent(price_changes, subject)
            
            logger.info(f"Price alert sent: {len(price_changes)} products")
            
        except Exception as e:
            logger.error(f"Could not send email: {e}")
    
    def _create_email_body(self, price_changes: List[Dict]) -> str:
        """Create email content"""
        html = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; }
                .product { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
                .price-drop { color: #d32f2f; font-weight: bold; }
                .target-reached { background-color: #e8f5e8; }
                .seller { margin: 5px 0; padding: 8px; background-color: #f5f5f5; border-radius: 3px; }
            </style>
        </head>
        <body>
            <h2>Amazon Price Alert</h2>
            <p>Price drops detected on your tracked products!</p>
        """
        
        for change in price_changes:
            css_class = "target-reached" if change['is_target_reached'] else ""
            
            html += f"""
            <div class="product {css_class}">
                <h3>{change['product_title']}</h3>
                <div class="seller">
                    <strong>Seller:</strong> {change['seller_name']}<br>
                    <strong>Current Price:</strong> <span class="price-drop">${change['current_price']:.2f}</span><br>
                    <strong>Previous Lowest:</strong> ${change['previous_min_price']:.2f}<br>
                    <strong>Drop:</strong> ${change['price_drop']:.2f} (%{change['percentage_drop']:.1f})<br>
                    {f"<strong>Target price reached!</strong>" if change['is_target_reached'] else ""}
                </div>
            </div>
            """
        
        html += """
            <p><small>This email was sent automatically by Amazon Price Tracker.</small></p>
        </body>
        </html>
        """
        
        return html
    
    def _log_email_sent(self, price_changes: List[Dict], subject: str):
        """Log sent email"""
        conn = sqlite3.connect('price_tracker.db')
        cursor = conn.cursor()
        
        for change in price_changes:
            cursor.execute('''
                INSERT INTO email_history (product_id, email_type, sent_to, subject)
                VALUES (?, ?, ?, ?)
            ''', (
                change['product_id'],
                'price_alert',
                self.config['email']['receiver_email'],
                subject
            ))
        
        conn.commit()
        conn.close()
    
    def monitor_all_products(self):
        """Monitor all active products"""
        conn = sqlite3.connect('price_tracker.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM products WHERE is_active = TRUE')
        product_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        all_changes = []
        
        for product_id in product_ids:
            try:
                changes = self.check_price_changes(product_id)
                all_changes.extend(changes)
                
                # Rate limiting
                time.sleep(self.config['tracking']['delay_between_requests'])
                
            except Exception as e:
                logger.error(f"Product {product_id} could not be checked: {e}")
                continue
        
        # Send email if there are significant price drops
        significant_changes = [
            change for change in all_changes
            if change['percentage_drop'] >= self.config['tracking']['price_drop_threshold']
            or change['is_target_reached']
        ]
        
        if significant_changes:
            self.send_price_alert(significant_changes)
        
        logger.info(f"Monitoring completed: {len(product_ids)} products checked, {len(significant_changes)} significant changes")
    
    def start_monitoring(self):
        """Start periodic monitoring"""
        interval = self.config['tracking']['check_interval_hours']
        
        # Schedule job
        schedule.every(interval).hours.do(self.monitor_all_products)
        
        logger.info(f"Monitoring started: check every {interval} hours")
        
        # Do first check immediately
        self.monitor_all_products()
        
        # Scheduler loop
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Monitoring stopped")
    
    def list_products(self) -> List[Dict]:
        """List tracked products"""
        conn = sqlite3.connect('price_tracker.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.*, 
                   COUNT(ph.id) as price_records,
                   MIN(ph.price) as min_price,
                   MAX(ph.price) as max_price,
                   AVG(ph.price) as avg_price
            FROM products p
            LEFT JOIN price_history ph ON p.id = ph.product_id
            WHERE p.is_active = TRUE
            GROUP BY p.id
            ORDER BY p.created_at DESC
        ''')
        
        products = []
        for row in cursor.fetchall():
            products.append({
                'id': row[0],
                'url': row[1],
                'title': row[2],
                'asin': row[3],
                'target_price': row[4],
                'created_at': row[5],
                'last_checked': row[6],
                'price_records': row[8],
                'min_price': row[9],
                'max_price': row[10],
                'avg_price': row[11]
            })
        
        conn.close()
        return products

def main():
    """Main function"""
    print("Amazon Price Tracker")
    print("=" * 40)
    
    tracker = AmazonPriceTracker()
    
    while True:
        print("\nMenu:")
        print("1. Add new product")
        print("2. List tracked products")
        print("3. Manual price check")
        print("4. Start monitoring")
        print("5. Exit")
        
        choice = input("\nYour choice (1-5): ").strip()
        
        if choice == '1':
            url = input("Amazon product URL: ").strip()
            target_str = input("Target price (optional, leave empty if none): ").strip()
            target_price = float(target_str) if target_str else None
            
            try:
                product_id = tracker.add_product(url, target_price)
                print(f"Product added! ID: {product_id}")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == '2':
            products = tracker.list_products()
            if products:
                print(f"\nTracked Products ({len(products)} items):")
                for p in products:
                    print(f"\n{p['title'][:60]}...")
                    print(f"   ID: {p['id']} | ASIN: {p['asin']}")
                    print(f"   Target: ${p['target_price'] or 'None'}")
                    print(f"   Min: ${p['min_price']:.2f} | Max: ${p['max_price']:.2f}")
                    print(f"   Last check: {p['last_checked'] or 'Never'}")
            else:
                print("No tracked products found")
        
        elif choice == '3':
            try:
                tracker.monitor_all_products()
                print("Manual check completed")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == '4':
            print("Starting monitoring... (Press Ctrl+C to stop)")
            try:
                tracker.start_monitoring()
            except KeyboardInterrupt:
                print("\nMonitoring stopped")
        
        elif choice == '5':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
    