import os
import discord
from discord.ext import commands
import threading 
from flask import Flask
from waitress import serve 

# ====================================================
# I. DEFINICIÓN GLOBAL (ANTES DE LAS FUNCIONES)
# ====================================================

# A) CONFIGURACIÓN DEL SERVIDOR WEB (KEEP-ALIVE)
app = Flask(__name__)

# B) CONFIGURACIÓN DEL BOT DE DISCORD
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='/', intents=intents)

# ====================================================
# II. FUNCIONES Y RUTAS (DEFINIDAS DESPUÉS DE LAS GLOBALES)
# ====================================================

@app.route('/')
def home():
    """Endpoint al que pingueará UptimeRobot."""
    return "Discord Bot is running 24/7!"

def run_discord():
    """Conecta el bot de Discord en un hilo separado."""
    TOKEN = os.getenv('DISCORD_TOKEN')
    try:
        # Aquí 'bot' ya está definido
        bot.run(TOKEN) 
    except Exception as e:
        print(f"❌ Error al conectar Discord: {e}")

# ... (El resto de funciones como load_extensions, on_ready, etc. pueden ir aquí) ...

@bot.command(name='hola')
async def saludo(ctx):
    await ctx.send(f'¡Hola, {ctx.author.display_name}! Estoy en línea 24/7.')

# ----------------------------------------------------
# C) EJECUCIÓN: Función Principal
# ----------------------------------------------------

def start_bot_and_server():
    # El chequeo del TOKEN puede ir aquí, pero lo simplificamos en run_discord
    
    # Iniciamos el bot en un hilo
    discord_thread = threading.Thread(target=run_discord)
    discord_thread.start()
    
    # Abrimos Waitress en el hilo principal
    port = int(os.environ.get('PORT', 10000)) # Usamos 10000 por defecto para ser explícitos
    print(f"✅ Abriendo servidor Waitress en puerto {port} para Keep-Alive...")
    # Aquí 'app' ya está definido
    serve(app, host='0.0.0.0', port=port)

if __name__ == '__main__':
    start_bot_and_server()