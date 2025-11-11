import discord
from discord.ext import commands
from discord import app_commands
import random

class Dado(commands.Cog):
    """Contiene el comando /roll para lanzar dados."""
    
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="roll", description="Lanza dados (ej: /roll 2d6 o /roll 1d20).")
    @app_commands.describe(dice_string="El formato del dado a lanzar (ej: 2d6)")
    async def roll_slash(self, interaction: discord.Interaction, dice_string: str):
        try:
            num_dice, sides = map(int, dice_string.lower().split('d'))
        except ValueError:
            await interaction.response.send_message(
                "❌ **Formato incorrecto.** Usa el formato `NdS`, donde N es el número de dados y S es el número de caras. Ejemplo: `/roll 2d6`.", 
                ephemeral=True
            )
            return
        
        if num_dice > 20 or sides > 100:
             await interaction.response.send_message(
                "❌ **Límite:** No puedo lanzar más de 20 dados ni dados con más de 100 caras.", 
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