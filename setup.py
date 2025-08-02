#!/usr/bin/env python3
"""
Amazon Price Tracker - Setup Script
This script configures email settings.
"""

import json
import os
import getpass

def setup_email_config():
    """Configure email settings"""
    print("Email Settings")
    print("-" * 20)
    print("You may need to use an app password for Gmail.")
    print("Details: https://support.google.com/accounts/answer/185833")
    print()
    
    sender_email = input("Sender email: ").strip()
    sender_password = getpass.getpass("Email password/app password: ")
    receiver_email = input("Receiver email (leave empty for same as sender): ").strip()
    
    if not receiver_email:
        receiver_email = sender_email
    
    # SMTP settings
    print("\nSMTP Settings")
    smtp_options = {
        "1": ("Gmail", "smtp.gmail.com", 587),
        "2": ("Outlook/Hotmail", "smtp-mail.outlook.com", 587),
        "3": ("Yahoo", "smtp.mail.yahoo.com", 587),
        "4": ("Custom", None, None)
    }
    
    print("Your email provider:")
    for key, (name, _, _) in smtp_options.items():
        print(f"  {key}. {name}")
    
    smtp_choice = input("Your choice (1-4): ").strip()
    
    if smtp_choice in smtp_options and smtp_choice != "4":
        _, smtp_server, smtp_port = smtp_options[smtp_choice]
    else:
        smtp_server = input("SMTP server: ").strip()
        smtp_port = int(input("SMTP port (usually 587): ").strip() or "587")
    
    return {
        "smtp_server": smtp_server,
        "smtp_port": smtp_port,
        "sender_email": sender_email,
        "sender_password": sender_password,
        "receiver_email": receiver_email
    }

def setup_tracking_config():
    """Configure tracking settings"""
    print("\nTracking Settings")
    print("-" * 20)
    
    interval = input("Check interval (hours, default 6): ").strip()
    interval = int(interval) if interval else 6
    
    threshold = input("Significant price drop threshold (%, default 5): ").strip()
    threshold = float(threshold) if threshold else 5.0
    
    delay = input("Delay between requests (seconds, default 2): ").strip()
    delay = int(delay) if delay else 2
    
    return {
        "check_interval_hours": interval,
        "price_drop_threshold": threshold,
        "max_retries": 3,
        "delay_between_requests": delay
    }

def create_config():
    """Create configuration file"""
    print("Amazon Price Tracker - Setup")
    print("=" * 40)
    
    if os.path.exists('config.json'):
        override = input("config.json exists. Overwrite? (y/N): ").strip().lower()
        if override != 'y':
            print("Setup cancelled")
            return
    
    email_config = setup_email_config()
    tracking_config = setup_tracking_config()
    
    # Complete configuration
    config = {
        "email": email_config,
        "tracking": tracking_config,
        "amazon": {
            "base_url": "https://www.amazon.com",
            "user_agents": [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            ]
        }
    }
    
    # Save to file
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("\nConfiguration saved successfully!")
    print("File: config.json")
    print()
    print("Next steps:")
    print("1. Add product:")
    print("   python quick_add.py <amazon_url>")
    print()
    print("2. Start monitoring:")
    print("   python start_monitoring.py")

def test_email():
    """Test email settings"""
    try:
        from amazon_price_tracker import AmazonPriceTracker
        import smtplib
        from email.mime.text import MIMEText
        
        print("\nTesting email settings...")
        
        if not os.path.exists('config.json'):
            print("config.json not found. Run setup first.")
            return
        
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        email_config = config['email']
        
        # Send test email
        subject = "Amazon Price Tracker - Test Email"
        body = """
        <html>
        <body>
            <h2>Test Successful!</h2>
            <p>Your Amazon Price Tracker email settings are working correctly.</p>
            <p>You can now receive price alerts!</p>
        </body>
        </html>
        """
        
        msg = MIMEText(body, 'html')
        msg['Subject'] = subject
        msg['From'] = email_config['sender_email']
        msg['To'] = email_config['receiver_email']
        
        server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
        server.starttls()
        server.login(email_config['sender_email'], email_config['sender_password'])
        server.send_message(msg)
        server.quit()
        
        print("Test email sent successfully!")
        print(f"Check: {email_config['receiver_email']}")
        
    except Exception as e:
        print(f"Email test error: {e}")
        print("\nCommon solutions:")
        print("- Use app password for Gmail")
        print("- Create special password if 2FA is enabled")
        print("- Check SMTP settings")

def main():
    """Main setup function"""
    print("Setup options:")
    print("1. Full setup (create config)")
    print("2. Test email settings")
    print("3. Exit")
    
    choice = input("\nYour choice (1-3): ").strip()
    
    if choice == "1":
        create_config()
    elif choice == "2":
        test_email()
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()