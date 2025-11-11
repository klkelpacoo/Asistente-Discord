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
# IMPORTANTE: Necesario para leer contenido de mensajes
intents.message_content = True 
# Definimos el prefijo de mensaje como '/'
bot = commands.Bot(command_prefix='/', intents=intents) 

# ====================================================
# II. FUNCIONES Y RUTAS
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
        # Aquí 'bot' ya está definido
        bot.run(TOKEN) 
    except Exception as e:
        print(f"❌ Error al conectar Discord: {e}")


async def load_extensions():
    """Función para cargar los Cogs (Módulos) del bot."""
    # Lista de extensiones a cargar: carpeta.archivo
    extensions = [
        'moderacion.clear',
        'utilidad.general',
        'juegos.dado' # <--- ESTE DEBE ESTAR CARGADO
    ]
    
    print("🤖 [INFO] Iniciando carga de extensiones...")
    
    for extension in extensions:
        try:
            await bot.load_extension(extension)
            print(f"✅ Cog cargado: {extension}")
        except Exception as e:
            # Si un Cog falla al cargar, lo reportamos.
            print(f"❌ [ERROR] Falló al cargar {extension}: {e}")
            print(f"   Asegúrate de que la carpeta '{extension.split('.')[0]}' existe y que el archivo '{extension.split('.')[1]}.py' está en ella.")

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
# III. EJECUCIÓN ESTABLE CON WAITRESS
# ----------------------------------------------------

def start_bot_and_server():
    """Inicia el bot de Discord en un hilo y Waitress en el hilo principal para el puerto."""
    
    # Iniciamos el bot en un hilo para que no bloquee la ejecución de Waitress
    discord_thread = threading.Thread(target=run_discord)
    discord_thread.start()
    
    # Abrimos Waitress en el hilo principal (que Render espera)
    port = int(os.environ.get('PORT', 10000)) # Usamos 10000 como puerto de Render
    print(f"✅ Abriendo servidor Waitress en puerto {port} para Keep-Alive...")
    serve(app, host='0.0.0.0', port=port)

if __name__ == '__main__':
    start_bot_and_server()