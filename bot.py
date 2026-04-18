import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

VERIFIED_ROLE_NAME = "Warga XML"
ALLOWED_GUILD_ID = 1452197469793419296

class VerifyButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ Klik untuk Verifikasi", style=discord.ButtonStyle.green, custom_id="verify_button")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, name=VERIFIED_ROLE_NAME)
        if role in interaction.user.roles:
            await interaction.response.send_message("⚠️ Kamu sudah terverifikasi!", ephemeral=True)
        elif role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("✅ Kamu sudah terverifikasi!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Role tidak ditemukan. Hubungi admin.", ephemeral=True)

@bot.event
async def on_ready():
    bot.add_view(VerifyButton())
    print(f"Bot online: {bot.user}")
    for guild in bot.guilds:
        if guild.id != ALLOWED_GUILD_ID:
            await guild.leave()
            print(f"Keluar dari server: {guild.name}")

@bot.event
async def on_guild_join(guild):
    if guild.id != ALLOWED_GUILD_ID:
        await guild.leave()
        print(f"Keluar dari server tidak diizinkan: {guild.name}")

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    if ctx.guild.id != ALLOWED_GUILD_ID:
        return
    embed = discord.Embed(
        title="✅ Verifikasi Member",
        description="Klik tombol di bawah untuk mendapatkan akses ke server.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed, view=VerifyButton())

bot.run(os.environ.get("DISCORD_TOKEN"))
