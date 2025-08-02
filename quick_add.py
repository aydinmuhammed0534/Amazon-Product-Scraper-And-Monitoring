#!/usr/bin/env python3
"""
Quick Amazon Product Adder
Add products with a single command using this script.
"""

import sys
from amazon_price_tracker import AmazonPriceTracker

def main():
    if len(sys.argv) < 2:
        print("Usage: python quick_add.py <amazon_url> [target_price]")
        print("\nExamples:")
        print("  python quick_add.py https://www.amazon.com/dp/B08N5WRWNW")
        print("  python quick_add.py https://www.amazon.com/dp/B08N5WRWNW 299.99")
        sys.exit(1)
    
    url = sys.argv[1]
    target_price = float(sys.argv[2]) if len(sys.argv) > 2 else None
    
    print("Amazon Price Tracker - Quick Add")
    print("=" * 45)
    print(f"URL: {url}")
    print(f"Target Price: ${target_price}" if target_price else "Target Price: Not specified")
    print()
    
    try:
        tracker = AmazonPriceTracker()
        
        print("Fetching product information...")
        product_id = tracker.add_product(url, target_price)
        
        print(f"Successfully added!")
        print(f"Product ID: {product_id}")
        print()
        print("Product is now being tracked. For manual control:")
        print("   python amazon_price_tracker.py")
        print()
        print("To start automatic monitoring:")
        print("   python start_monitoring.py")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()