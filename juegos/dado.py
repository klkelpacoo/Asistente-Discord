import discord
from discord.ext import commands
from discord import app_commands
import random
import os # Importar os

# --- Cargar el Guild ID desde las variables de entorno ---
GUILD_ID_FROM_ENV = os.getenv('GUILD_ID')
MY_GUILD = None
if GUILD_ID_FROM_ENV:
    try:
        MY_GUILD = discord.Object(id=int(GUILD_ID_FROM_ENV))
    except ValueError:
        MY_GUILD = None # Falla si el ID no es un número

class Dado(commands.Cog):
    """Contiene el comando /roll para lanzar dados."""
    
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="roll", description="Lanza dados (ej: /roll 2d6 o /roll 1d20).", guild=MY_GUILD)
    @app_commands.describe(dice_string="El formato del dado a lanzar (ej: 2d6)")
    async def roll_slash(self, interaction: discord.Interaction, dice_string: str):
        try:
            num_dice, sides = map(int, dice_string.lower().split('d'))
        except ValueError:
            await interaction.response.send_message(
                "❌ **Formato incorrecto.** Usa el formato `NdS`. Ejemplo: `/roll 2d6`.", 
                ephemeral=True
            )
            return
        
        if num_dice > 20 or sides > 100:
             await interaction.response.send_message(
                "❌ **Límite:** No puedo lanzar más de 20 dados o dados de +100 caras.", 
                ephemeral=True
            )
             return

        rolls = [random.randint(1, sides) for _ in range(num_dice)]
        total = sum(rolls)
        
        response = f"🎲 **Resultado de `{num_dice}d{sides}`:**\n"
        response += f"Tiradas: `{rolls}`\n"
        response += f"**Total: {total}**"
        
        await interaction.response.send_message(response)

async def setup(bot):
    await bot.add_cog(Dado(bot))