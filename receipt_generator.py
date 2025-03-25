
import random
import io
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import os
from config import STORES

class ReceiptGenerator:
    def __init__(self):
        self.default_font = "arial.ttf"
        
    def generate_order_number(self, store_id):
        """Generate a realistic order number based on store format"""
        store = STORES.get(store_id.lower())
        if not store:
            return f"ORD-{random.randint(1000000, 9999999)}"
            
        # Generate random numbers for each part of the order format
        order_parts = []
        for digits in store["order_digits"]:
            min_val = 10 ** (digits - 1)
            max_val = (10 ** digits) - 1
            order_parts.append(random.randint(min_val, max_val))
            
        # Format the order number
        order_number = store["order_prefix"] + store["order_format"].format(*order_parts)
        return order_number
    
    def generate_date(self, days_ago_min=1, days_ago_max=30):
        """Generate a random date within the specified range"""
        days_ago = random.randint(days_ago_min, days_ago_max)
        date = datetime.now() - timedelta(days=days_ago)
        return date.strftime("%Y-%m-%d %H:%M:%S")
    
    def calculate_total(self, price, quantity, tax_rate):
        """Calculate subtotal, tax, and total price"""
        subtotal = price * quantity
        tax = subtotal * tax_rate
        total = subtotal + tax
        return subtotal, tax, total
    
    def generate_tracking_number(self, carrier="ups"):
        """Generate a realistic tracking number"""
        carriers = {
            "ups": "1Z",
            "fedex": "78",
            "usps": "94"
        }
        
        prefix = carriers.get(carrier.lower(), "1Z")
        
        if carrier.lower() == "ups":
            tracking = prefix + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))
            tracking += ''.join(random.choices('0123456789', k=10))
        elif carrier.lower() == "fedex":
            tracking = prefix + ''.join(random.choices('0123456789', k=10))
        elif carrier.lower() == "usps":
            tracking = prefix + ''.join(random.choices('0123456789', k=20))
        else:
            tracking = prefix + ''.join(random.choices('0123456789', k=12))
            
        return tracking
    
    def generate_card_number(self, card_type="visa"):
        """Generate a masked credit card number"""
        if card_type.lower() == "visa":
            return "4XXX XXXX XXXX " + ''.join(random.choices('0123456789', k=4))
        elif card_type.lower() == "mastercard":
            return "5XXX XXXX XXXX " + ''.join(random.choices('0123456789', k=4))
        elif card_type.lower() == "american express":
            return "3XXX XXXXXX " + ''.join(random.choices('0123456789', k=5))
        elif card_type.lower() == "discover":
            return "6XXX XXXX XXXX " + ''.join(random.choices('0123456789', k=4))
        else:
            return "XXXX XXXX XXXX " + ''.join(random.choices('0123456789', k=4))
    
    async def create_receipt_image(self, store_id, product_name, price, quantity, shipping, payment_method):
        """Create a receipt image"""
        store_data = STORES.get(store_id.lower(), STORES["amazon"])
        
        # Generate order information
        order_number = self.generate_order_number(store_id)
        order_date = self.generate_date()
        subtotal, tax, total = self.calculate_total(price, quantity, store_data["tax_rate"])
        tracking_number = self.generate_tracking_number()
        card_number = self.generate_card_number(payment_method)
        
        # Create a new image (white background)
        img = Image.new('RGB', (800, 1000), color='white')
        draw = ImageDraw.Draw(img)
        
        # Use default font if store font doesn't exist
        try:
            # For simplicity, using default font - in a real implementation you'd use the store's font
            font_large = ImageFont.truetype(self.default_font, 24)
            font_medium = ImageFont.truetype(self.default_font, 18)
            font_small = ImageFont.truetype(self.default_font, 14)
        except IOError:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Draw store name at the top
        draw.text((400, 50), store_data["name"], fill='black', font=font_large, anchor="mm")
        
        # Draw receipt details
        draw.text((50, 100), f"Order Number: {order_number}", fill='black', font=font_medium)
        draw.text((50, 130), f"Order Date: {order_date}", fill='black', font=font_medium)
        draw.text((50, 160), f"Shipping Method: {shipping}", fill='black', font=font_medium)
        draw.text((50, 190), f"Payment Method: {payment_method} ({card_number})", fill='black', font=font_medium)
        draw.text((50, 220), f"Tracking Number: {tracking_number}", fill='black', font=font_medium)
        
        # Draw line separator
        draw.line((50, 250, 750, 250), fill='black', width=2)
        
        # Draw column headers
        draw.text((50, 270), "Item", fill='black', font=font_medium)
        draw.text((500, 270), "Qty", fill='black', font=font_medium)
        draw.text((600, 270), "Price", fill='black', font=font_medium)
        draw.text((700, 270), "Total", fill='black', font=font_medium)
        
        # Draw line separator
        draw.line((50, 300, 750, 300), fill='black', width=1)
        
        # Draw product info
        # Truncate long product names
        if len(product_name) > 50:
            product_name = product_name[:47] + "..."
        
        draw.text((50, 320), product_name, fill='black', font=font_medium)
        draw.text((500, 320), str(quantity), fill='black', font=font_medium)
        draw.text((600, 320), f"${price:.2f}", fill='black', font=font_medium)
        draw.text((700, 320), f"${price * quantity:.2f}", fill='black', font=font_medium)
        
        # Draw line separator
        draw.line((50, 360, 750, 360), fill='black', width=1)
        
        # Draw summary
        draw.text((500, 390), "Subtotal:", fill='black', font=font_medium)
        draw.text((700, 390), f"${subtotal:.2f}", fill='black', font=font_medium)
        
        draw.text((500, 420), f"Tax ({store_data['tax_rate']*100:.2f}%):", fill='black', font=font_medium)
        draw.text((700, 420), f"${tax:.2f}", fill='black', font=font_medium)
        
        # Add shipping cost if not free
        if shipping != "Free" and shipping != "Store Pickup":
            shipping_cost = random.uniform(5.99, 19.99)
            draw.text((500, 450), "Shipping:", fill='black', font=font_medium)
            draw.text((700, 450), f"${shipping_cost:.2f}", fill='black', font=font_medium)
            total += shipping_cost
            y_offset = 480
        else:
            draw.text((500, 450), "Shipping:", fill='black', font=font_medium)
            draw.text((700, 450), "Free", fill='black', font=font_medium)
            y_offset = 480
        
        # Draw total
        draw.text((500, y_offset), "Total:", fill='black', font=font_large)
        draw.text((700, y_offset), f"${total:.2f}", fill='black', font=font_large)
        
        # Draw billing and shipping address
        y_offset += 50
        draw.text((50, y_offset), "Billing Address:", fill='black', font=font_medium)
        y_offset += 30
        draw.text((50, y_offset), f"John Doe", fill='black', font=font_small)
        y_offset += 20
        draw.text((50, y_offset), f"123 Main St", fill='black', font=font_small)
        y_offset += 20
        draw.text((50, y_offset), f"Anytown, CA 12345", fill='black', font=font_small)
        
        y_offset = 530
        draw.text((400, y_offset), "Shipping Address:", fill='black', font=font_medium)
        y_offset += 30
        draw.text((400, y_offset), f"John Doe", fill='black', font=font_small)
        y_offset += 20
        draw.text((400, y_offset), f"123 Main St", fill='black', font=font_small)
        y_offset += 20
        draw.text((400, y_offset), f"Anytown, CA 12345", fill='black', font=font_small)
        
        # Draw store address and contact
        draw.text((400, 750), store_data["address"], fill='grey', font=font_small, anchor="mm")
        draw.text((400, 770), f"Phone: {store_data['phone']}", fill='grey', font=font_small, anchor="mm")
        draw.text((400, 790), f"Email: support@{store_data['email_domain']}", fill='grey', font=font_small, anchor="mm")
        
        # Draw thank you message
        draw.text((400, 850), "Thank you for your purchase!", fill='black', font=font_medium, anchor="mm")
        
        # Add return policy
        draw.text((400, 880), "Return Policy:", fill='black', font=font_small, anchor="mm")
        draw.text((400, 900), "Items may be returned within 30 days of purchase with receipt.", fill='grey', font=font_small, anchor="mm")
        
        # Convert the image to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return img_byte_arr
