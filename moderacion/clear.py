import discord
from discord.ext import commands
from discord import app_commands # Importamos el módulo clave para Slash Commands

# La clase debe heredar de commands.Cog
class Clear(commands.Cog):
    """Contiene comandos de moderación como el borrado de mensajes (Slash Commands)."""
    
    def __init__(self, bot):
        self.bot = bot
        
    # --- Comando de Moderación: /clear (Slash Command) ---
    # Usamos app_commands.command y definimos los argumentos explícitamente.
    @app_commands.command(name="clear", description="Borra un número específico de mensajes en el canal.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear_slash(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100]):
        """
        Borra hasta 100 mensajes en el canal.
        El argumento 'amount' se define con un rango de 1 a 100 para validación automática.
        """
        
        # Respuesta inicial para evitar el error de interacción de Discord
        await interaction.response.send_message(f'🗑️ Preparando para borrar **{amount} mensajes...**', ephemeral=True)
        
        try:
            # Borra los mensajes (amount + 1 para borrar también la respuesta inicial del bot)
            await interaction.channel.purge(limit=amount + 1)
            
            # Edita la respuesta inicial para mostrar la confirmación final
            await interaction.edit_original_response(content=f'✅ **{amount} mensajes borrados.**', delete_after=5)

        except discord.Forbidden:
            # Si el bot no tiene permiso de Gestionar Mensajes
            await interaction.edit_original_response(content="🔒 **Error de Permiso:** El bot necesita el permiso 'Gestionar Mensajes' para hacer esto.", delete_after=10)
        except Exception as e:
            await interaction.edit_original_response(content=f"❌ **Error desconocido al borrar mensajes:** {e}", delete_after=10)


# Esta función es OBLIGATORIA para que el bot pueda cargar la extensión (Cog)
async def setup(bot):
    await bot.add_cog(Clear(bot))