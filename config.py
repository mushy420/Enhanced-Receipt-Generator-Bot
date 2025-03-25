
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
COOLDOWN_TIME = int(os.getenv('COOLDOWN_TIME', 300))  # Default 5 minutes

# Store data
STORES = {
    "amazon": {
        "name": "Amazon",
        "logo": "assets/logos/amazon_logo.png",
        "email_domain": "amazon.com",
        "address": "410 Terry Ave N, Seattle, WA 98109",
        "phone": "(206) 266-1000",
        "tax_rate": 0.0725,
        "shipping_options": ["Standard", "Prime", "Express", "One-Day"],
        "payment_methods": ["Visa", "Mastercard", "Discover", "American Express", "Amazon Gift Card"],
        "font": "assets/fonts/amazon_font.ttf",
        "template": "assets/templates/amazon_template.png",
        "order_format": "{}-{}-{}",  # Will be formatted with random numbers
        "order_prefix": "",
        "order_digits": [3, 7, 7]  # Number of digits in each part of the order number
    },
    "walmart": {
        "name": "Walmart",
        "logo": "assets/logos/walmart_logo.png",
        "email_domain": "walmart.com",
        "address": "702 SW 8th St, Bentonville, AR 72716",
        "phone": "(800) 925-6278",
        "tax_rate": 0.0825,
        "shipping_options": ["Standard", "Express", "Next-Day", "Store Pickup"],
        "payment_methods": ["Visa", "Mastercard", "Discover", "American Express", "Walmart Gift Card"],
        "font": "assets/fonts/walmart_font.ttf",
        "template": "assets/templates/walmart_template.png",
        "order_format": "{}",
        "order_prefix": "W",
        "order_digits": [8]
    },
    "target": {
        "name": "Target",
        "logo": "assets/logos/target_logo.png",
        "email_domain": "target.com",
        "address": "1000 Nicollet Mall, Minneapolis, MN 55403",
        "phone": "(800) 440-0680",
        "tax_rate": 0.0725,
        "shipping_options": ["Standard", "Express", "Next-Day", "Store Pickup"],
        "payment_methods": ["Visa", "Mastercard", "Discover", "American Express", "Target Gift Card"],
        "font": "assets/fonts/target_font.ttf",
        "template": "assets/templates/target_template.png",
        "order_format": "{}",
        "order_prefix": "T",
        "order_digits": [8]
    },
    "bestbuy": {
        "name": "Best Buy",
        "logo": "assets/logos/bestbuy_logo.png",
        "email_domain": "bestbuy.com",
        "address": "7601 Penn Ave S, Richfield, MN 55423",
        "phone": "(888) 237-8289",
        "tax_rate": 0.0825,
        "shipping_options": ["Standard", "Express", "Next-Day", "Store Pickup"],
        "payment_methods": ["Visa", "Mastercard", "Discover", "American Express", "Best Buy Gift Card"],
        "font": "assets/fonts/bestbuy_font.ttf",
        "template": "assets/templates/bestbuy_template.png",
        "order_format": "{}",
        "order_prefix": "BBY",
        "order_digits": [8]
    },
    "apple": {
        "name": "Apple",
        "logo": "assets/logos/apple_logo.png",
        "email_domain": "apple.com",
        "address": "One Apple Park Way, Cupertino, CA 95014",
        "phone": "(800) 275-2273",
        "tax_rate": 0.0875,
        "shipping_options": ["Standard", "Express", "Next-Day"],
        "payment_methods": ["Visa", "Mastercard", "Discover", "American Express", "Apple Gift Card"],
        "font": "assets/fonts/apple_font.ttf",
        "template": "assets/templates/apple_template.png",
        "order_format": "{}",
        "order_prefix": "W",
        "order_digits": [10]
    },
    "newegg": {
        "name": "Newegg",
        "logo": "assets/logos/newegg_logo.png",
        "email_domain": "newegg.com",
        "address": "17560 Rowland St, City of Industry, CA 91748",
        "phone": "(800) 390-1119",
        "tax_rate": 0.0775,
        "shipping_options": ["Standard", "3-Day", "2-Day", "Next-Day"],
        "payment_methods": ["Visa", "Mastercard", "Discover", "American Express", "Newegg Gift Card"],
        "font": "assets/fonts/newegg_font.ttf",
        "template": "assets/templates/newegg_template.png",
        "order_format": "{}",
        "order_prefix": "NE",
        "order_digits": [9]
    },
    "costco": {
        "name": "Costco",
        "logo": "assets/logos/costco_logo.png",
        "email_domain": "costco.com",
        "address": "999 Lake Dr, Issaquah, WA 98027",
        "phone": "(800) 774-2678",
        "tax_rate": 0.0775,
        "shipping_options": ["Standard", "Express", "2-Day"],
        "payment_methods": ["Visa", "Costco Cash Card"],
        "font": "assets/fonts/costco_font.ttf",
        "template": "assets/templates/costco_template.png",
        "order_format": "{}",
        "order_prefix": "C",
        "order_digits": [9]
    }
}

# Directory paths
ASSETS_DIR = "assets"
LOGOS_DIR = os.path.join(ASSETS_DIR, "logos")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
TEMPLATES_DIR = os.path.join(ASSETS_DIR, "templates")
DATA_DIR = "data"

# Create necessary directories
for directory in [LOGOS_DIR, FONTS_DIR, TEMPLATES_DIR, DATA_DIR]:
    os.makedirs(directory, exist_ok=True)
