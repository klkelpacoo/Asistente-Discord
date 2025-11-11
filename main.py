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
bot = commands.Bot(command_prefix='/', intents=intents) 

# --- Carga el ID de tu servidor para la sincronización ---
GUILD_ID_FROM_ENV = os.getenv('GUILD_ID')
MY_GUILD = None

if GUILD_ID_FROM_ENV:
    try:
        MY_GUILD = discord.Object(id=int(GUILD_ID_FROM_ENV))
        print(f"✅ [INFO] Sincronizando comandos con GUILD_ID: {GUILD_ID_FROM_ENV}")
    except ValueError:
        print(f"❌ [ERROR] El GUILD_ID '{GUILD_ID_FROM_ENV}' no es un número.")
else:
    print("⚠️ [AVISO] No se encontró GUILD_ID. La sincronización será global (lenta).")

# ====================================================
# II. FUNCIONES DE INFRAESTRUCTURA
# ====================================================

@app.route('/')
def home():
    """Endpoint para UptimeRobot"""
    return "Bot con Cogs (Guild Sync) está activo!"

def run_discord():
    """Ejecuta el bot de Discord en un hilo."""
    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN is None:
        print("\n[ERROR] TOKEN NO ENCONTRADO.")
        return
    try:
        print("🤖 [INFO] Conectando a Discord...")
        bot.run(TOKEN) 
    except Exception as e:
        print(f"❌ Error al conectar Discord: {e}")

# ====================================================
# III. CARGA DE COGS (¡ESTA ES LA PARTE QUE FALTABA!)
# ====================================================

async def load_extensions():
    """
    Carga todos los Cogs (extensiones) desde las carpetas.
    Esto se ejecuta ANTES de on_ready.
    """
    
    # Tus carpetas y archivos
    extensions = [
        'moderacion.clear',
        'utilidad.general',
        'juegos.dado' 
    ]
    
    print("🤖 [INFO] Iniciando carga de extensiones...")
    
    for extension in extensions:
        try:
            # Intenta cargar el archivo
            await bot.load_extension(extension)
            print(f"✅ Cog cargado: {extension}")
        except Exception as e:
            # Si falla, imprime el error
            print(f"❌ [ERROR] Falló al cargar {extension}. Error: {e}")

# Asignamos la función al 'setup_hook' para que se ejecute al inicio
# Esto reemplaza al comando /hola que tenías antes
bot.setup_hook = load_extensions

# ====================================================
# IV. EVENTO ON_READY
# ====================================================

@bot.event
async def on_ready():
    """Se ejecuta cuando el bot está conectado y los Cogs están cargados."""
    print('-------------------------------------------')
    print(f'✅ Bot Conectado como: {bot.user.name}')
    
    # --- SINCRONIZACIÓN CON GUILD ---
    # Sincroniza todos los comandos que los Cogs han registrado
    try:
        if MY_GUILD:
            print(f"🔄 [INFO] Sincronizando comandos para el servidor {MY_GUILD.id}...")
            # Sincroniza SOLO para tu servidor (instantáneo)
            synced = await bot.tree.sync(guild=MY_GUILD)
        else:
            print("🔄 [INFO] Sincronizando comandos globalmente (puede tardar)...")
            # Sincronización global (lenta, hasta 1h)
            synced = await bot.tree.sync()
            
        print(f"✅ Sincronizados {len(synced)} comandos.")
            
    except Exception as e:
        print(f"❌ Error al sincronizar comandos: {e}")
    
    print('Render deployment successful.')
    print('-------------------------------------------')


# ====================================================
# V. EJECUCIÓN DEL SERVICIO
# ====================================================

def start_bot_and_server():
    """Inicia el bot y el servidor web."""
    
    print("🚀 Iniciando hilo del Bot de Discord...")
    discord_thread = threading.Thread(target=run_discord)
    discord_thread.start()
    
    port = int(os.environ.get('PORT', 10000)) 
    print(f"✅ Abriendo servidor Waitress en puerto {port}...")
    serve(app, host='0.0.0.0', port=port)

if __name__ == '__main__':
    start_bot_and_server()