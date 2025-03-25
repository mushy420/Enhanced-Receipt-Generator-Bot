import discord
import os
import json
import random
from datetime import datetime, timedelta
import asyncio
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont
import io
from dotenv import load_dotenv
from receipt_generator import ReceiptGenerator

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
COOLDOWN_TIME = int(os.getenv('COOLDOWN_TIME', '300'))

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)

# Create receipt generator instance
receipt_gen = ReceiptGenerator()

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
        "template": "assets/templates/amazon_template.png"
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
        "template": "assets/templates/walmart_template.png"
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
        "template": "assets/templates/target_template.png"
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
        "template": "assets/templates/bestbuy_template.png"
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
        "template": "assets/templates/apple_template.png"
    }
}

# Create necessary directories
os.makedirs("assets/logos", exist_ok=True)
os.makedirs("assets/fonts", exist_ok=True)
os.makedirs("assets/templates", exist_ok=True)
os.makedirs("data", exist_ok=True)

# User cooldown data
user_cooldowns = {}

# Bot startup event
@bot.event
async def on_ready():
    print(f"{bot.user.name} is now online!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    
    # Set activity
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, 
        name="for /receipt commands"
    ))

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏱️ **Cooldown active!** Please try again in {error.retry_after:.1f} seconds.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ **Missing required argument!** Please check the command usage.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ **Invalid argument!** Please check the command usage.")
    else:
        await ctx.send(f"❌ **An error occurred:** {str(error)}")
        print(f"Error: {error}")

@bot.command(name='receipt')
async def receipt_command(ctx, store: str, product: str, price: float, quantity: int = 1, shipping: str = "Standard", payment: str = "Visa"):
    # Check if store exists
    store = store.lower()
    if store not in STORES:
        await ctx.send(f"❌ **Store '{store}' not found.** Use `/stores` to see available stores.")
        return
    
    # Check cooldown
    user_id = str(ctx.author.id)
    current_time = datetime.now()
    
    if user_id in user_cooldowns:
        time_diff = (current_time - user_cooldowns[user_id]).total_seconds()
        if time_diff < COOLDOWN_TIME:
            remaining = COOLDOWN_TIME - time_diff
            await ctx.send(f"⏱️ **Cooldown active!** Please try again in {remaining:.1f} seconds.")
            return
    
    # Set cooldown
    user_cooldowns[user_id] = current_time
    
    # Generate receipt
    try:
        # Validate inputs
        if price <= 0:
            await ctx.send("❌ **Price must be greater than zero!**")
            return
        
        if quantity <= 0:
            await ctx.send("❌ **Quantity must be greater than zero!**")
            return
        
        # Send initial response
        await ctx.send("🧾 **Generating your receipt...**")
        
        # Generate receipt image using the ReceiptGenerator class
        receipt_image = await receipt_gen.create_receipt_image(
            store, product, price, quantity, shipping, payment
        )
        
        # Send receipt as an image
        await ctx.send(
            content=f"✅ **Receipt generated successfully for {STORES[store]['name']}!**",
            file=discord.File(fp=receipt_image, filename=f"{store}_receipt.png")
        )
        
    except Exception as e:
        await ctx.send(f"❌ **An error occurred while generating the receipt:** {str(e)}")
        print(f"Error generating receipt: {e}")
    
    embed.add_field(
        name="🧾 `/receipt`", 
        value=(
            "Generate a receipt with the following parameters:\n"
            "- **store**: Store name (amazon, walmart, target, bestbuy, apple)\n"
            "- **product**: Product name\n"
            "- **price**: Product price\n"
            "- **quantity**: Quantity purchased (default: 1)\n"
            "- **shipping**: Shipping method\n"
            "- **payment**: Payment method\n"
        ), 
        inline=False
    )
    
    embed.add_field(
        name="ℹ️ `/stores`", 
        value="View all available stores", 
        inline=False
    )
    
    embed.add_field(
        name="⏱️ Cooldown", 
        value=f"There is a {COOLDOWN_TIME} second cooldown between receipt generations.", 
        inline=False
    )
    
    embed.set_footer(text="Enhanced Receipt Generator Bot | v1.0.0")
    
    await ctx.send(embed=embed)
    
    for store_id, store_data in STORES.items():
        embed.add_field(
            name=store_data["name"], 
            value=(
                f"**Tax Rate:** {store_data['tax_rate']*100:.2f}%\n"
                f"**Shipping Options:** {', '.join(store_data['shipping_options'])}\n"
            ), 
            inline=True
        )
    
    await ctx.send(embed=embed)
    
    embed.add_field(
        name="🌟 Features", 
        value=(
            "• Generate professional receipts for various stores\n"
            "• Customize product details, prices, and quantities\n"
            "• Multiple shipping and payment options\n"
            "• Realistic order numbers and dates\n"
        ), 
        inline=False
    )
    
    embed.add_field(
        name="🛠️ Developer", 
        value="Created by @mushy420", 
        inline=False
    )
    
    embed.add_field(
        name="📊 Server Count", 
        value=f"{len(bot.guilds)} servers", 
        inline=True
    )
    
    embed.add_field(
        name="🔄 Version", 
        value="1.0.0", 
        inline=True
    )
    
    await ctx.send(embed=embed)

# Run the bot
if __name__ == "__main__":
    if not TOKEN:
        print("Error: No Discord token found. Please set the DISCORD_TOKEN environment variable.")
    else:
        try:
            bot.run(TOKEN, reconnect=True)
        except Exception as e:
            print(f"Error starting bot: {e}")
