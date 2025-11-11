import discord
from discord.ext import commands
from discord import app_commands
import time

class General(commands.Cog):
    """Contiene comandos de utilidad general como ping e info."""
    
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        
    @app_commands.command(name="ping", description="Muestra la latencia del bot en milisegundos.")
    async def ping_slash(self, interaction: discord.Interaction):
        latency_ms = round(self.bot.latency * 1000)
        await interaction.response.send_message(f'🏓 ¡Pong! Latencia: **{latency_ms} ms**', ephemeral=True)

    @app_commands.command(name="info", description="Muestra el tiempo activo (Uptime) y la versión del bot.")
    async def info_slash(self, interaction: discord.Interaction):
        current_time = time.time()
        uptime_seconds = int(round(current_time - self.start_time))
        
        days, remainder = divmod(uptime_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        uptime_str = f"**{days}d, {hours}h, {minutes}m, {seconds}s**"

        embed = discord.Embed(
            title="🤖 Información del Asistente",
            color=discord.Color.blue()
        )
        embed.add_field(name="Tiempo Activo (Uptime)", value=uptime_str, inline=False)
        embed.add_field(name="Versión de discord.py", value=f"v{discord.__version__}", inline=True)
        embed.set_footer(text=f"Desplegado en Render.com")

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(General(bot))