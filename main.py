import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import json
from receipt_generator import generate_receipt
from store_manager import StoreManager
from error_handler import setup_error_handler

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

store_manager = StoreManager()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="!help for commands"))

@bot.command(name='receipt')
async def receipt(ctx, store: str, amount: float, style: str = 'default'):
    try:
        store_data = store_manager.get_store(store)
        if not store_data:
            await ctx.send(f"Store '{store}' not found. Use !liststores to see available stores.")
            return
        
        receipt_image = generate_receipt(store_data, amount, style)
        await ctx.send(file=discord.File(receipt_image, 'receipt.png'))
    except ValueError as e:
        await ctx.send(str(e))
    except Exception as e:
        print(f"An error occurred: {e}")
        await ctx.send("An error occurred while generating the receipt.")

@bot.command(name='addstore')
@commands.has_permissions(administrator=True)
async def add_store(ctx, name: str, *, details: str):
    try:
        store_manager.add_store(name, json.loads(details))
        await ctx.send(f"Store '{name}' added successfully.")
    except json.JSONDecodeError:
        await ctx.send("Invalid store details. Please provide a valid JSON string.")
    except Exception as e:
        print(f"An error occurred: {e}")
        await ctx.send("An error occurred while adding the store.")

@bot.command(name='removestore')
@commands.has_permissions(administrator=True)
async def remove_store(ctx, name: str):
    if store_manager.remove_store(name):
        await ctx.send(f"Store '{name}' removed successfully.")
    else:
        await ctx.send(f"Store '{name}' not found.")

@bot.command(name='liststores')
async def list_stores(ctx):
    stores = store_manager.list_stores()
    if stores:
        await ctx.send("Available stores:\n" + "\n".join(stores))
    else:
        await ctx.send("No stores available.")

@bot.command(name='liststyles')
async def list_styles(ctx):
    styles = ['default', 'minimal', 'fancy']
    await ctx.send("Available receipt styles:\n" + "\n".join(styles))

setup_error_handler(bot)

bot.run(TOKEN)
