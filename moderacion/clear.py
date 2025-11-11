import discord
from discord.ext import commands
from discord import app_commands

class Clear(commands.Cog):
    """Contiene el comando /clear para moderación."""
    
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="clear", description="Borra un número específico de mensajes en el canal.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear_slash(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100]):
        
        await interaction.response.send_message(f'🗑️ Preparando para borrar **{amount} mensajes...**', ephemeral=True)
        
        try:
            await interaction.channel.purge(limit=amount)
            await interaction.edit_original_response(content=f'✅ **{amount} mensajes borrados.**') 

        except discord.Forbidden:
            await interaction.edit_original_response(content="🔒 **Error de Permiso:** El bot necesita el permiso 'Gestionar Mensajes' para hacer esto.")
        except Exception as e:
            await interaction.edit_original_response(content=f"❌ **Error desconocido:** {e}")

async def setup(bot):
    await bot.add_cog(Clear(bot))