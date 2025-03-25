
import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import json
import os

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.admin_ids = [
            # Add admin user IDs here
        ]
        self.stats_file = "data/stats.json"
        self.load_stats()
        
    def load_stats(self):
        """Load stats from file"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    self.stats = json.load(f)
            except json.JSONDecodeError:
                self.stats = {"receipts_generated": 0, "users": {}}
        else:
            self.stats = {"receipts_generated": 0, "users": {}}
    
    def save_stats(self):
        """Save stats to file"""
        os.makedirs(os.path.dirname(self.stats_file), exist_ok=True)
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f)
    
    def is_admin(self, user_id):
        """Check if user is an admin"""
        return str(user_id) in self.admin_ids
    
    @app_commands.command(name="stats", description="View bot statistics (Admin only)")
    async def stats_command(self, interaction: discord.Interaction):
        # Check if user is admin
        if not self.is_admin(interaction.user.id):
            await interaction.response.send_message("❌ **You don't have permission to use this command!**", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="📊 Bot Statistics",
            description="Usage statistics for the Enhanced Receipt Generator Bot",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="📝 Total Receipts Generated", 
            value=str(self.stats["receipts_generated"]), 
            inline=False
        )
        
        embed.add_field(
            name="👥 Unique Users", 
            value=str(len(self.stats["users"])), 
            inline=True
        )
        
        embed.add_field(
            name="🏪 Servers", 
            value=str(len(self.bot.guilds)), 
            inline=True
        )
        
        # Top stores
        store_counts = {}
        for user_id, user_data in self.stats["users"].items():
            for receipt in user_data.get("receipts", []):
                store = receipt.get("store", "unknown")
                store_counts[store] = store_counts.get(store, 0) + 1
        
        if store_counts:
            top_stores = sorted(store_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            stores_text = "\n".join([f"**{store.capitalize()}**: {count}" for store, count in top_stores])
            embed.add_field(
                name="🔝 Top Stores", 
                value=stores_text, 
                inline=False
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="announce", description="Send an announcement to all servers (Admin only)")
    @app_commands.describe(
        message="The announcement message to send"
    )
    async def announce_command(self, interaction: discord.Interaction, message: str):
        # Check if user is admin
        if not self.is_admin(interaction.user.id):
            await interaction.response.send_message("❌ **You don't have permission to use this command!**", ephemeral=True)
            return
        
        await interaction.response.send_message("📢 **Sending announcement...**", ephemeral=True)
        
        sent_count = 0
        failed_count = 0
        
        for guild in self.bot.guilds:
            try:
                # Try to find a suitable channel
                channel = None
                
                # Prioritize system channels, announcements, or general channels
                if guild.system_channel:
                    channel = guild.system_channel
                else:
                    # Look for channels with certain names
                    for channel_name in ["announcements", "general", "bot", "bot-commands"]:
                        channels = [c for c in guild.text_channels if channel_name in c.name.lower()]
                        if channels:
                            channel = channels[0]
                            break
                    
                    # If still no channel found, take the first text channel
                    if channel is None and guild.text_channels:
                        channel = guild.text_channels[0]
                
                if channel:
                    embed = discord.Embed(
                        title="📢 Enhanced Receipt Generator Announcement",
                        description=message,
                        color=discord.Color.blue()
                    )
                    
                    embed.set_footer(text=f"From the developers • {datetime.now().strftime('%Y-%m-%d')}")
                    
                    await channel.send(embed=embed)
                    sent_count += 1
                else:
                    failed_count += 1
            except Exception as e:
                failed_count += 1
                print(f"Failed to send announcement to {guild.name}: {e}")
        
        await interaction.followup.send(
            f"📢 **Announcement sent to {sent_count} servers. Failed: {failed_count}**",
            ephemeral=True
        )
    
    @app_commands.command(name="reset-cooldown", description="Reset a user's cooldown (Admin only)")
    @app_commands.describe(
        user="The user to reset cooldown for"
    )
    async def reset_cooldown_command(self, interaction: discord.Interaction, user: discord.User):
        # Check if user is admin
        if not self.is_admin(interaction.user.id):
            await interaction.response.send_message("❌ **You don't have permission to use this command!**", ephemeral=True)
            return
        
        # Get receipt commands cog
        receipt_cog = self.bot.get_cog("ReceiptCommands")
        
        if receipt_cog and user.id in receipt_cog.user_cooldowns:
            del receipt_cog.user_cooldowns[str(user.id)]
            await interaction.response.send_message(f"✅ **Cooldown reset for {user.name}!**", ephemeral=True)
        else:
            await interaction.response.send_message(f"ℹ️ **{user.name} doesn't have an active cooldown.**", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
