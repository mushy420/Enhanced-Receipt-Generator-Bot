import discord
from discord.ext import commands

def setup_error_handler(bot):
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Invalid command. Use !help to see available commands.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument. Please check the command usage.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument type. Please check the command usage.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the required permissions to use this command.")
        else:
            await ctx.send("An error occurred while processing the command.")
            print(f"Unhandled error: {error}")

