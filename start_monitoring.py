#!/usr/bin/env python3
"""
Amazon Price Tracker - Monitoring Starter
This script starts continuous monitoring mode.
"""

import sys
from amazon_price_tracker import AmazonPriceTracker

def main():
    print("Amazon Price Tracker - Monitoring Mode")
    print("=" * 45)
    
    tracker = AmazonPriceTracker()
    
    # Show tracked products
    products = tracker.list_products()
    
    if not products:
        print("No tracked products found!")
        print("First add products:")
        print("   python quick_add.py <amazon_url>")
        print("   or")
        print("   python amazon_price_tracker.py")
        sys.exit(1)
    
    print(f"Products to monitor: {len(products)}")
    print(f"Check interval: {tracker.config['tracking']['check_interval_hours']} hours")
    print(f"Email: {tracker.config['email']['receiver_email']}")
    print()
    
    # List products
    print("Tracked products:")
    for i, product in enumerate(products[:5], 1):
        print(f"  {i}. {product['title'][:50]}...")
        if product['target_price']:
            print(f"     Target: ${product['target_price']}")
    
    if len(products) > 5:
        print(f"  ... and {len(products) - 5} more products")
    
    print()
    confirm = input("Start monitoring? (y/N): ").strip().lower()
    
    if confirm != 'y':
        print("Operation cancelled")
        return
    
    print()
    print("Starting monitoring...")
    print("Press Ctrl+C to stop")
    print("=" * 45)
    
    try:
        tracker.start_monitoring()
    except KeyboardInterrupt:
        print("\nMonitoring stopped")
        print("Goodbye!")

if __name__ == "__main__":
    main()