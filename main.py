import os
import discord
from discord.ext import commands

# ----------------------------------------------------
# 1. Configuración del Bot y Prefijo
# ----------------------------------------------------
# Los 'intents' son necesarios para decirle a Discord qué datos necesita el bot.
intents = discord.Intents.default()
intents.message_content = True 

# Definimos el prefijo para los comandos (ej: !hola)
bot = commands.Bot(command_prefix='!', intents=intents)


# ----------------------------------------------------
# 2. Evento de Inicio (Se ejecuta al conectar)
# ----------------------------------------------------
@bot.event
async def on_ready():
    """Confirma que el bot ha iniciado sesión y está listo."""
    print('-------------------------------------------')
    print(f'✅ Bot Conectado como: {bot.user.name}')
    print('Render deployment successful.')
    print('-------------------------------------------')


# ----------------------------------------------------
# 3. Primer Comando: ¡Hola!
# ----------------------------------------------------
@bot.command(name='hola')
async def saludo(ctx):
    """Responde con un saludo al usar !hola"""
    await ctx.send(f'¡Hola, {ctx.author.display_name}! Estoy en línea y funcionando en Render.')


# ----------------------------------------------------
# 4. Ejecución Segura (Obteniendo el Token de Render)
# ----------------------------------------------------
# Render ya expone las variables de entorno sin necesidad de librerías extra.
TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    print("\n[ERROR] El TOKEN no fue encontrado. Configúralo en las Environment Variables de Render.")
else:
    try:
        # Iniciamos la conexión con Discord
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("\n[ERROR] El token de acceso proporcionado es inválido. Revisa tu Token en Render.")
    except Exception as e:
        print(f"\n[ERROR] Ocurrió un error al intentar iniciar el bot: {e}")