import os
import discord
from discord.ext import commands
import threading 
from flask import Flask
from waitress import serve 

# ====================================================
# I. DEFINICIÓN GLOBAL
# ====================================================
app = Flask(__name__)
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='/', intents=intents) 

# ====================================================
# II. FUNCIONES DE INFRAESTRUCTURA
# ====================================================

@app.route('/')
def home():
    """Endpoint al que pingueará UptimeRobot."""
    return "Discord Bot is running 24/7!"

def run_discord():
    """Conecta el bot de Discord en un hilo separado."""
    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN is None:
        print("\n[ERROR] TOKEN NO ENCONTRADO. Configúralo en las Environment Variables de Render.")
        return
        
    try:
        bot.run(TOKEN) 
    except Exception as e:
        print(f"❌ Error al conectar Discord: {e}")

async def load_extensions():
    """Función para cargar los Cogs (Módulos) del bot."""
    extensions = [
        'moderacion.clear',
        'utilidad.general',
        'juegos.dado' 
    ]
    
    print("🤖 [INFO] Iniciando carga de extensiones...")
    
    for extension in extensions:
        try:
            await bot.load_extension(extension)
            print(f"✅ Cog cargado: {extension}")
        except Exception as e:
            print(f"❌ [ERROR] Falló al cargar {extension}. Error: {e}")

bot.setup_hook = load_extensions

@bot.event
async def on_ready():
    print('-------------------------------------------')
    print(f'✅ Bot Conectado como: {bot.user.name}')
    
    # SINCRONIZACIÓN DE SLASH COMMANDS
    try:
        synced = await bot.tree.sync()
        print(f"✅ Sincronizados {len(synced)} Slash Commands.")
    except Exception as e:
        print(f"❌ Error al sincronizar comandos: {e}")
    
    print('Render deployment successful.')
    print('-------------------------------------------')


# ----------------------------------------------------
# III. EJECUCIÓN DEL SERVICIO
# ----------------------------------------------------

def start_bot_and_server():
    """Inicia el bot de Discord en un hilo y Waitress en el hilo principal para el puerto."""
    
    # Iniciamos el bot en un hilo para que no bloquee la ejecución de Waitress
    discord_thread = threading.Thread(target=run_discord)
    discord_thread.start()
    
    # Abrimos Waitress en el hilo principal (que Render espera)
    port = int(os.environ.get('PORT', 10000)) 
    print(f"✅ Abriendo servidor Waitress en puerto {port} para Keep-Alive...")
    serve(app, host='0.0.0.0', port=port)

if __name__ == '__main__':
    start_bot_and_server()