import os
import discord
from discord.ext import commands
import threading 
from flask import Flask
from waitress import serve 

# ====================================================
# I. DEFINICIÓN GLOBAL
# ====================================================

# app de Flask para el 'Keep-Alive' de Render
app = Flask(__name__)

# Definimos los intents del Bot
intents = discord.Intents.default()
intents.message_content = True 

# Creamos la instancia del Bot
bot = commands.Bot(command_prefix='/', intents=intents) 

# ====================================================
# II. FUNCIONES DE INFRAESTRUCTURA
# ====================================================

@app.route('/')
def home():
    """
    Endpoint principal para la ruta web. 
    UptimeRobot (o servicio similar) hará ping aquí para mantener el bot activo.
    """
    return "Discord Bot is running 24/7!"

def run_discord():
    """
    Función que se ejecuta en un hilo separado para conectar el bot a Discord.
    """
    # Obtenemos el TOKEN desde las variables de entorno de Render
    TOKEN = os.getenv('DISCORD_TOKEN')
    
    # Comprobación de seguridad
    if TOKEN is None:
        print("\n[ERROR] TOKEN NO ENCONTRADO. Configúralo en las Environment Variables de Render.")
        return
        
    try:
        # Iniciamos el bot con el token
        bot.run(TOKEN) 
    except Exception as e:
        print(f"❌ Error al conectar Discord: {e}")

async def load_extensions():
    """
    Función de 'setup' que se ejecuta antes de 'on_ready'.
    Carga todos los Cogs (módulos de comandos) del bot.
    """
    
    # === LA CORRECCIÓN ESTÁ AQUÍ ===
    # Los nombres deben coincidir con los archivos .py en el directorio raíz.
    # Antes tenías 'moderacion.clear', 'utilidad.general', etc.
    # Lo correcto es 'clear', 'general', y 'dado', ya que los archivos
    # están en la misma carpeta que main.py.
    extensions = [
        'clear',
        'general',
        'dado' 
    ]
    
    print("🤖 [INFO] Iniciando carga de extensiones...")
    
    for extension in extensions:
        try:
            # Intentamos cargar la extensión
            await bot.load_extension(extension)
            print(f"✅ Cog cargado: {extension}")
        except Exception as e:
            # Si falla, imprimimos el error
            print(f"❌ [ERROR] Falló al cargar {extension}. Error: {e}")

# Asignamos la función al 'setup_hook' para que se ejecute al inicio
bot.setup_hook = load_extensions

@bot.event
async def on_ready():
    """
    Este evento se dispara cuando el bot se conecta exitosamente a Discord.
    """
    print('-------------------------------------------')
    print(f'✅ Bot Conectado como: {bot.user.name}')
    
    # SINCRONIZACIÓN DE SLASH COMMANDS
    # Esto es crucial para que los comandos / aparezcan en Discord.
    try:
        # Sincroniza los comandos definidos en los Cogs con Discord
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
    """
    Función principal que inicia ambos servicios:
    1. El bot de Discord (en un hilo secundario).
    2. El servidor web Waitress (en el hilo principal).
    """
    
    # Iniciamos el bot en un hilo para que no bloquee la ejecución de Waitress
    print("🚀 Iniciando hilo del Bot de Discord...")
    discord_thread = threading.Thread(target=run_discord)
    discord_thread.start()
    
    # Obtenemos el puerto que Render nos asigna (o 10000 si falla)
    port = int(os.environ.get('PORT', 10000)) 
    print(f"✅ Abriendo servidor Waitress en puerto {port} para Keep-Alive...")
    
    # Iniciamos el servidor web que Render necesita para validar el despliegue
    serve(app, host='0.0.0.0', port=port)

if __name__ == '__main__':
    # Punto de entrada del script
    start_bot_and_server()