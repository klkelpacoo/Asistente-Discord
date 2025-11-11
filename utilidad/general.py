import discord
from discord.ext import commands
from discord import app_commands
import time
import random

# La clase debe heredar de commands.Cog
class General(commands.Cog):
    """Contiene comandos de utilidad general como ping, info y roll."""
    
    def __init__(self, bot):
        self.bot = bot
        # Guardamos el tiempo de inicio para calcular el Uptime
        self.start_time = time.time()
        
    # --- 1. Comando /ping (Muestra la Latencia) ---
    @app_commands.command(name="ping", description="Muestra la latencia del bot en milisegundos.")
    async def ping_slash(self, interaction: discord.Interaction):
        # Calcula la latencia entre el mensaje y Discord
        latency_ms = round(self.bot.latency * 1000)
        await interaction.response.send_message(f'🏓 ¡Pong! Latencia: **{latency_ms} ms**', ephemeral=True)

    # --- 2. Comando /info (Uptime y Versión) ---
    @app_commands.command(name="info", description="Muestra el tiempo activo (Uptime) y la versión del bot.")
    async def info_slash(self, interaction: discord.Interaction):
        # Calcula el Uptime
        current_time = time.time()
        uptime_seconds = int(round(current_time - self.start_time))
        
        # Convierte segundos a formato H:M:S
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
        embed.add_field(name="Prefijo de Mensaje", value=f"`{self.bot.command_prefix}`", inline=True)
        embed.set_footer(text=f"Desplegado en Render.com")

        await interaction.response.send_message(embed=embed, ephemeral=True)

    # --- 3. Comando /roll (Lanza Dados) ---
    # Argumento 'dice_string' es el formato (e.g., 2d6)
    @app_commands.command(name="roll", description="Lanza dados (ej: /roll 2d6 o /roll 1d20).")
    @app_commands.describe(dice_string="El formato del dado a lanzar (ej: 2d6)")
    async def roll_slash(self, interaction: discord.Interaction, dice_string: str):
        try:
            # Separamos el número de dados (n) y las caras (s)
            num_dice, sides = map(int, dice_string.lower().split('d'))
        except ValueError:
            await interaction.response.send_message(
                "❌ **Formato incorrecto.** Usa el formato `NdS`, donde N es el número de dados y S es el número de caras. Ejemplo: `/roll 2d6`.", 
                ephemeral=True
            )
            return
        
        # Validaciones de límites
        if num_dice > 20 or sides > 100:
             await interaction.response.send_message(
                "❌ **Límite:** No puedo lanzar más de 20 dados ni dados con más de 100 caras.", 
                ephemeral=True
            )
             return

        # Simulación de la tirada
        rolls = [random.randint(1, sides) for _ in range(num_dice)]
        total = sum(rolls)
        
        response = f"🎲 **Resultado de `{num_dice}d{sides}`:**\n"
        response += f"Tiradas: `{rolls}`\n"
        response += f"**Total: {total}**"
        
        await interaction.response.send_message(response)


# Esta función es OBLIGATORIA para que el bot pueda cargar la extensión (Cog)
async def setup(bot):
    await bot.add_cog(General(bot))