from PIL import Image, ImageDraw, ImageFont
import random
import datetime
import io
import pkg_resources

def generate_receipt(store_data, amount, style='default'):
    if style not in ['default', 'minimal', 'fancy']:
        raise ValueError(f"Invalid style '{style}'. Use !liststyles to see available styles.")

    # Create a blank white image
    img = Image.new('RGB', (400, 600), color='white')
    
    # Load background image if style is 'fancy'
    if style == 'fancy':
        background = Image.open(pkg_resources.resource_filename(__name__, 'backgrounds/fancy.png'))
        img.paste(background, (0, 0))

    d = ImageDraw.Draw(img)

    # Load fonts
    title_font = ImageFont.truetype(pkg_resources.resource_filename(__name__, 'fonts/arial.ttf'), 24)
    body_font = ImageFont.truetype(pkg_resources.resource_filename(__name__, 'fonts/arial.ttf'), 16)

    # Generate receipt content
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    receipt_number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    items = random.sample(store_data['items'], min(3, len(store_data['items'])))

    # Draw store name
    d.text((200, 20), store_data['name'], font=title_font, fill='black', anchor='mt')

    # Draw receipt details
    y_offset = 60
    if style != 'minimal':
        d.text((10, y_offset), f"Date: {current_time}", font=body_font, fill='black')
        y_offset += 20
        d.text((10, y_offset), f"Receipt #: {receipt_number}", font=body_font, fill='black')
        y_offset += 40

    # Draw items
    subtotal = 0
    for item in items:
        d.text((10, y_offset), item['name'], font=body_font, fill='black')
        d.text((390, y_offset), f"${item['price']:.2f}", font=body_font, fill='black', anchor='ra')
        y_offset += 20
        subtotal += item['price']

    # Draw totals
    y_offset += 20
    d.text((10, y_offset), "Subtotal:", font=body_font, fill='black')
    d.text((390, y_offset), f"${subtotal:.2f}", font=body_font, fill='black', anchor='ra')
    y_offset += 20
    tax = round(subtotal * store_data['tax_rate'], 2)
    d.text((10, y_offset), f"Tax ({store_data['tax_rate']*100}%):", font=body_font, fill='black')
    d.text((390, y_offset), f"${tax:.2f}", font=body_font, fill='black', anchor='ra')
    y_offset += 20
    total = subtotal + tax
    d.text((10, y_offset), "Total:", font=body_font, fill='black')
    d.text((390, y_offset), f"${total:.2f}", font=body_font, fill='black', anchor='ra')

    # Draw provided amount
    y_offset += 40
    d.text((200, y_offset), f"Amount Paid: ${amount:.2f}", font=title_font, fill='black', anchor='mt')

    # Add watermark for fancy style
    if style == 'fancy':
        watermark_font = ImageFont.truetype(pkg_resources.resource_filename(__name__, 'fonts/arial.ttf'), 36)
        d.text((200, 550), "FAKE", font=watermark_font, fill=(200, 200, 200, 128), anchor='mm')

    # Save the image to a bytes buffer
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

