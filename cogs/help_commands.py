
import discord
from discord import app_commands
from discord.ext import commands
from config import COOLDOWN_TIME

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="help", description="Show bot commands and information")
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📜 Enhanced Receipt Generator Bot",
            description="Generate realistic receipts for various stores",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="🧾 `/receipt`", 
            value=(
                "Generate a receipt with the following parameters:\n"
                "- **store**: Store name (amazon, walmart, target, etc.)\n"
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
            value="View all available stores and their details", 
            inline=False
        )
        
        embed.add_field(
            name="ℹ️ `/about`", 
            value="Information about the Enhanced Receipt Generator Bot", 
            inline=False
        )
        
        embed.add_field(
            name="⏱️ Cooldown", 
            value=f"There is a {COOLDOWN_TIME} second cooldown between receipt generations.", 
            inline=False
        )
        
        embed.set_footer(text="Enhanced Receipt Generator Bot | v1.0.0")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="about", description="About the Enhanced Receipt Generator Bot")
    async def about_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="About Enhanced Receipt Generator Bot",
            description="A powerful receipt generator for Discord",
            color=discord.Color.purple()
        )
        
        embed.add_field(
            name="🌟 Features", 
            value=(
                "• Generate professional receipts for various stores\n"
                "• Customize product details, prices, and quantities\n"
                "• Multiple shipping and payment options\n"
                "• Realistic order numbers, tracking numbers, and dates\n"
                "• High-quality receipt images\n"
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
            value=f"{len(self.bot.guilds)} servers", 
            inline=True
        )
        
        embed.add_field(
            name="🔄 Version", 
            value="1.0.0", 
            inline=True
        )
        
        embed.add_field(
            name="📝 Disclaimer", 
            value=(
                "This bot is intended for educational purposes only. "
                "The generated receipts should not be used for fraudulent activities. "
                "The developer is not responsible for any misuse of this tool."
            ),
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
        
async def setup(bot):
    await bot.add_cog(HelpCommands(bot))
