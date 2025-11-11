import discord
from discord.ext import commands
from discord import app_commands # Importamos el módulo clave para Slash Commands

# La clase debe heredar de commands.Cog
class Clear(commands.Cog):
    """Contiene comandos de moderación como el borrado de mensajes (Slash Commands)."""
    
    def __init__(self, bot):
        self.bot = bot
        
    # --- Comando de Moderación: /clear (Slash Command) ---
    @app_commands.command(name="clear", description="Borra un número específico de mensajes en el canal.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear_slash(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100]):
        """
        Borra hasta 100 mensajes en el canal.
        El argumento 'amount' se define con un rango de 1 a 100 para validación automática.
        """
        
        # 1. Respuesta inicial (ephemeral=True la hace privada)
        # Usaremos la respuesta inicial como confirmación temporal.
        await interaction.response.send_message(f'🗑️ Preparando para borrar **{amount} mensajes...**', ephemeral=True)
        
        try:
            # Borra los mensajes (Discord borrará el mensaje de interacción principal del usuario,
            # pero necesitamos +1 para el mensaje de 'Preparando...')
            # La respuesta inicial del bot es privada, así que purgeamos solo los mensajes del canal.
            await interaction.channel.purge(limit=amount)
            
            # 2. Edita la respuesta inicial para mostrar la confirmación final
            # *** ERROR CORREGIDO: SE ELIMINA delete_after ***
            await interaction.edit_original_response(content=f'✅ **{amount} mensajes borrados.**') 

        except discord.Forbidden:
            # Si el bot no tiene permiso de Gestionar Mensajes
            # *** ERROR CORREGIDO: SE ELIMINA delete_after ***
            await interaction.edit_original_response(content="🔒 **Error de Permiso:** El bot necesita el permiso 'Gestionar Mensajes' para hacer esto.")
        except Exception as e:
            # *** ERROR CORREGIDO: SE ELIMINA delete_after ***
            await interaction.edit_original_response(content=f"❌ **Error desconocido al borrar mensajes:** {e}")


# Esta función es OBLIGATORIA para que el bot pueda cargar la extensión (Cog)
async def setup(bot):
    await bot.add_cog(Clear(bot))