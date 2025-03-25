
import discord
import os
import asyncio
from discord.ext import commands
import logging
from config import DISCORD_TOKEN, COOLDOWN_TIME

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("receipt-bot")

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot class with cogs support
class ReceiptBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            description="Enhanced Receipt Generator Bot"
        )
        self.logger = logger
        
    async def setup_hook(self):
        """Setup hook for loading cogs and syncing commands"""
        # Load cogs
        for cog_file in os.listdir("cogs"):
            if cog_file.endswith(".py"):
                cog_name = cog_file[:-3]  # Remove .py extension
                try:
                    await self.load_extension(f"cogs.{cog_name}")
                    self.logger.info(f"Loaded cog: {cog_name}")
                except Exception as e:
                    self.logger.error(f"Failed to load cog {cog_name}: {e}")
        
        # Sync commands
        await self.tree.sync()
        self.logger.info("Synced command tree")
        
    async def on_ready(self):
        """Event fired when the bot is ready"""
        self.logger.info(f"{self.user.name} is now online!")
        
        # Set activity
        await self.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching, 
            name="for /receipt commands"
        ))
        
        # Log guild count
        self.logger.info(f"Bot is in {len(self.guilds)} guilds")
    
    async def on_guild_join(self, guild):
        """Event fired when the bot joins a new guild"""
        self.logger.info(f"Joined new guild: {guild.name} (ID: {guild.id})")
        
        # Try to send a welcome message
        try:
            # Find a suitable channel
            channel = None
            if guild.system_channel:
                channel = guild.system_channel
            else:
                for channel_name in ["general", "bot", "bot-commands"]:
                    channels = [c for c in guild.text_channels if channel_name in c.name.lower()]
                    if channels:
                        channel = channels[0]
                        break
                
                if channel is None and guild.text_channels:
                    channel = guild.text_channels[0]
            
            if channel:
                embed = discord.Embed(
                    title="👋 Thanks for adding Enhanced Receipt Generator Bot!",
                    description="Generate professional receipts for various popular stores with customizable options.",
                    color=discord.Color.blue()
                )
                
                embed.add_field(
                    name="Getting Started", 
                    value="Use `/help` to see all available commands", 
                    inline=False
                )
                
                embed.add_field(
                    name="Generate a Receipt", 
                    value="Try `/receipt store:amazon product:\"Product Name\" price:19.99`", 
                    inline=False
                )
                
                embed.set_footer(text="Enhanced Receipt Generator Bot | v1.0.0")
                
                await channel.send(embed=embed)
        except Exception as e:
            self.logger.error(f"Error sending welcome message to {guild.name}: {e}")
    
    async def on_command_error(self, ctx, error):
        """Global error handler for command errors"""
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏱️ **Cooldown active!** Please try again in {error.retry_after:.1f} seconds.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ **Missing required argument!** Please check the command usage.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ **Invalid argument!** Please check the command usage.")
        else:
            self.logger.error(f"Command error: {error}")
            await ctx.send(f"❌ **An error occurred:** {str(error)}")

# Run the bot
if __name__ == "__main__":
    bot = ReceiptBot()
    
    if not DISCORD_TOKEN:
        logger.error("No Discord token found. Please set the DISCORD_TOKEN environment variable.")
    else:
        try:
            bot.run(DISCORD_TOKEN)
        except discord.errors.LoginFailure:
            logger.error("Invalid Discord token. Please check your token and try again.")
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
