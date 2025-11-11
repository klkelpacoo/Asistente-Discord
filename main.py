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
# Este intent es crucial para poder procesar comandos de texto (aunque usemos Slash Commands, es buena práctica)
intents.message_content = True 
# Definimos el prefijo de mensaje como '/' (aunque ahora solo usaremos Slash Commands)
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
    try:
        # El path es 'nombre_carpeta.nombre_archivo_sin_py'
        await bot.load_extension('moderacion.clear')
        print("🤖 [INFO] Cog cargado: moderacion.clear")
        await bot.load_extension('utilidad.general')
        print("🤖 [INFO] Cog cargado: utilidad.general")
    except Exception as e:
        print(f"❌ [ERROR] Error al cargar cog: moderacion.clear: {e}")

bot.setup_hook = load_extensions # Esto le dice al bot que ejecute load_extensions antes de conectarse

@bot.event
async def on_ready():
    print('-------------------------------------------')
    print(f'✅ Bot Conectado como: {bot.user.name}')
    
    # ⬇️ SINCRONIZACIÓN DE SLASH COMMANDS ⬇️
    try:
        # Sincroniza los comandos con Discord
        synced = await bot.tree.sync()
        print(f"✅ Sincronizados {len(synced)} Slash Commands.")
    except Exception as e:
        print(f"❌ Error al sincronizar comandos: {e}")
    # ------------------------------------
    
    print('Render deployment successful.')
    print('-------------------------------------------')

# *** COMANDO /HOLA ELIMINADO DE AQUÍ ***


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