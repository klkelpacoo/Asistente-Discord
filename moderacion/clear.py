import discord
from discord.ext import commands

# La clase debe heredar de commands.Cog
class Clear(commands.Cog):
    """Contiene comandos de moderación como el borrado de mensajes."""
    
    def __init__(self, bot):
        self.bot = bot
        
    # --- Comando de Moderación: /clear ---
    @commands.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        """
        Borra un número específico de mensajes en el canal.
        Uso: /clear <número>
        """
        if amount > 100:
            await ctx.send("🚨 Solo puedo borrar un máximo de 100 mensajes a la vez. Inténtalo de nuevo con un número menor.", delete_after=5)
            return
            
        if amount < 1:
            await ctx.message.delete()
            await ctx.send("🚨 Por favor, especifica un número positivo de mensajes a borrar.", delete_after=5)
            return

        # Borra los mensajes (amount + 1 para borrar también el mensaje de /clear)
        await ctx.channel.purge(limit=amount + 1)
        
        await ctx.send(f'🗑️ **{amount} mensajes borrados.**', delete_after=5)

    # --- Manejo de Errores para el Comando Clear ---
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("⚠️ **Uso incorrecto:** Necesitas especificar cuántos mensajes borrar. Ejemplo: `/clear 10`")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("🔒 **Permiso denegado.** Necesitas el permiso `Gestionar Mensajes` para usar este comando.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ **Error:** El argumento debe ser un número entero.")

# Esta función es OBLIGATORIA para que el bot pueda cargar la extensión (Cog)
async def setup(bot):
    await bot.add_cog(Clear(bot))