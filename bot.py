import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

VERIFIED_ROLE_NAME = "Verified"

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

@bot.command()
async def verify(ctx):
    role = discord.utils.get(ctx.guild.roles, name=VERIFIED_ROLE_NAME)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"✅ {ctx.author.mention} sudah terverifikasi!")
    else:
        await ctx.send("❌ Role 'Verified' tidak ditemukan.")

bot.run(os.environ.get("DISCORD_TOKEN"))
