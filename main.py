import os
import discord
from discord.ext import commands
# Importamos threading para ejecutar Flask en un hilo separado
import threading
from flask import Flask

# ----------------------------------------------------
# A) CONFIGURACIÓN DEL SERVIDOR WEB (KEEP-ALIVE)
# ----------------------------------------------------

# Flask es el servidor web simple que Render necesita para mantenerse "vivo".lll
app = Flask(__name__)

@app.route('/')
def home():
    """Endpoint al que pingueará el servicio externo."""
    return "Discord Bot is running and kept alive!"

def run_server():
    """Inicia Flask en un hilo de fondo."""
    # Render usa la variable de entorno PORT, la cogemos si existe, si no, usamos 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)


# ----------------------------------------------------
# B) CONFIGURACIÓN DEL BOT DE DISCORD
# ----------------------------------------------------
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print('-------------------------------------------')
    print(f'✅ Bot Conectado como: {bot.user.name}')
    print('Render deployment successful.')
    print('-------------------------------------------')


@bot.command(name='hola')
async def saludo(ctx):
    await ctx.send(f'¡Hola, {ctx.author.display_name}! Estoy en línea y funcionando 24/7.')


# ----------------------------------------------------
# C) EJECUCIÓN DEL BOT
# ----------------------------------------------------

# 1. Iniciamos el Servidor Web en un hilo paralelo
server_thread = threading.Thread(target=run_server)
server_thread.start()

# 2. Iniciamos el Bot de Discord
TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    print("\n[ERROR] El TOKEN no fue encontrado. Configúralo en las Environment Variables de Render.")
else:
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("\n[ERROR] El token de acceso proporcionado es inválido. Revisa tu Token en Render.")
    except Exception as e:
        print(f"\n[ERROR] Ocurrió un error al intentar iniciar el bot: {e}")