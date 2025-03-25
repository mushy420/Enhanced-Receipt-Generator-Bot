
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import random
import asyncio
from config import STORES, COOLDOWN_TIME
from receipt_generator import ReceiptGenerator

class ReceiptCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.receipt_generator = ReceiptGenerator()
        self.user_cooldowns = {}
        
    @app_commands.command(name="receipt", description="Generate a receipt for a purchase")
    @app_commands.describe(
        store="Store name (amazon, walmart, target, bestbuy, apple, etc)",
        product="Product name",
        price="Product price",
        quantity="Quantity purchased",
        shipping="Shipping method",
        payment="Payment method"
    )
    @app_commands.choices(
        store=[
            app_commands.Choice(name=data["name"], value=store_id)
            for store_id, data in STORES.items()
        ],
        shipping=[
            app_commands.Choice(name="Standard", value="Standard"),
            app_commands.Choice(name="Express", value="Express"),
            app_commands.Choice(name="Next-Day", value="Next-Day"),
            app_commands.Choice(name="Store Pickup", value="Store Pickup")
        ],
        payment=[
            app_commands.Choice(name="Visa", value="Visa"),
            app_commands.Choice(name="Mastercard", value="Mastercard"),
            app_commands.Choice(name="American Express", value="American Express"),
            app_commands.Choice(name="Discover", value="Discover"),
            app_commands.Choice(name="Store Gift Card", value="Store Gift Card")
        ]
    )
    async def receipt_command(
        self,
        interaction: discord.Interaction, 
        store: str, 
        product: str, 
        price: float, 
        quantity: int = 1,
        shipping: str = "Standard",
        payment: str = "Visa"
    ):
        # Check cooldown
        user_id = str(interaction.user.id)
        current_time = datetime.now()
        
        if user_id in self.user_cooldowns:
            time_diff = (current_time - self.user_cooldowns[user_id]).total_seconds()
            if time_diff < COOLDOWN_TIME:
                remaining = COOLDOWN_TIME - time_diff
                await interaction.response.send_message(
                    f"⏱️ **Cooldown active!** Please try again in {remaining:.1f} seconds.",
                    ephemeral=True
                )
                return
        
        # Set cooldown
        self.user_cooldowns[user_id] = current_time
        
        # Send initial response
        await interaction.response.send_message("🧾 **Generating your receipt...**")
        
        try:
            # Validate inputs
            if price <= 0:
                await interaction.edit_original_response(content="❌ **Price must be greater than zero!**")
                return
            
            if quantity <= 0:
                await interaction.edit_original_response(content="❌ **Quantity must be greater than zero!**")
                return
            
            # Generate receipt image
            receipt_image = await self.receipt_generator.create_receipt_image(
                store, product, price, quantity, shipping, payment
            )
            
            # Get store info
            store_data = STORES.get(store.lower(), STORES["amazon"])
            
            # Send receipt as an image
            await interaction.edit_original_response(
                content=f"✅ **Receipt generated successfully for {store_data['name']}!**"
            )
            
            await interaction.followup.send(
                file=discord.File(fp=receipt_image, filename=f"{store}_receipt.png")
            )
            
        except Exception as e:
            await interaction.edit_original_response(
                content=f"❌ **An error occurred while generating the receipt:** {str(e)}"
            )
            print(f"Error generating receipt: {e}")
    
    @app_commands.command(name="stores", description="Show available stores")
    async def stores_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🏪 Available Stores",
            description="Here are all the stores currently supported for receipt generation",
            color=discord.Color.green()
        )
        
        # Group stores into two columns
        stores_list = list(STORES.items())
        
        for i in range(0, len(stores_list), 3):
            for j in range(3):
                if i + j < len(stores_list):
                    store_id, store_data = stores_list[i + j]
                    embed.add_field(
                        name=store_data["name"], 
                        value=(
                            f"**Tax Rate:** {store_data['tax_rate']*100:.2f}%\n"
                            f"**Shipping Options:** {', '.join(store_data['shipping_options'][:2])}...\n"
                        ), 
                        inline=True
                    )
        
        # Add footer
        embed.set_footer(text="Use /receipt to generate a receipt for any of these stores!")
        
        await interaction.response.send_message(embed=embed)
        
async def setup(bot):
    await bot.add_cog(ReceiptCommands(bot))
