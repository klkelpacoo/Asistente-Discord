print("=============================================")
print("[LOG] INICIANDO SCRIPT main.py (Nivel 0)")
print("=============================================")

import os
import discord
from discord.ext import commands
import threading 
from flask import Flask
from waitress import serve 

print("[LOG] Módulos importados correctamente.")

# ====================================================
# I. DEFINICIÓN GLOBAL
# ====================================================

print("[LOG] --- SECCIÓN I: DEFINICIÓN GLOBAL ---")

print("[LOG] Creando instancia de Flask...")
app = Flask(__name__)
print("[LOG] Instancia de Flask CREADA.")

print("[LOG] Definiendo Intents de Discord...")
intents = discord.Intents.default()
print("[LOG] Intents DEFINIDOS.")

print("[LOG] Creando instancia del Bot...")
bot = commands.Bot(command_prefix='/', intents=intents) 
print("[LOG] Instancia del Bot CREADA.")

# --- Carga el ID de tu servidor para la sincronización ---
print("[LOG] Intentando cargar GUILD_ID desde variables de entorno...")
GUILD_ID_FROM_ENV = os.getenv('GUILD_ID')
MY_GUILD = None

if GUILD_ID_FROM_ENV:
    try:
        MY_GUILD = discord.Object(id=int(GUILD_ID_FROM_ENV))
        print(f"✅ [LOG] GUILD_ID cargado y configurado: {GUILD_ID_FROM_ENV}")
    except ValueError:
        print(f"❌ [LOG-ERROR] El GUILD_ID '{GUILD_ID_FROM_ENV}' no es un número.")
else:
    print("⚠️ [LOG-AVISO] No se encontró GUILD_ID. Se usará sincronización global (lenta).")

# ====================================================
# II. FUNCIONES DE INFRAESTRUCTURA
# ====================================================

print("[LOG] --- SECCIÓN II: INFRAESTRUCTURA ---")

@app.route('/')
def home():
    """Endpoint para UptimeRobot"""
    print("[LOG] Ruta '/' (home) ha recibido un ping.")
    return "Bot con Cogs (Guild Sync) está activo! (Logs Detallados)"

def run_discord():
    """Ejecuta el bot de Discord en un hilo."""
    print("[LOG] Función run_discord() iniciada.")
    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN is None:
        print("\n❌ [LOG-ERROR] TOKEN NO ENCONTRADO. Revisa las variables de entorno.\n")
        return
    
    print("🤖 [LOG] TOKEN encontrado. Conectando a Discord...")
    try:
        bot.run(TOKEN) 
    except Exception as e:
        print(f"❌ [LOG-ERROR] Falló bot.run(TOKEN): {e}")

print("[LOG] Funciones de infraestructura DEFINIDAS.")

# ====================================================
# III. CARGA DE COGS (LA PARTE MÁS IMPORTANTE)
# ====================================================

print("[LOG] --- SECCIÓN III: CARGA DE COGS ---")

async def load_extensions():
    """Carga todos los Cogs (extensiones) desde las carpetas."""
    print("🤖 [LOG] load_extensions() INICIADA.")
    
    extensions = [
        'moderacion.clear',
        'utilidad.general',
        'juegos.dado' 
    ]
    print(f"[LOG] Lista de extensiones a cargar: {extensions}")
    
    print("[LOG] Iniciando bucle de carga de extensiones...")
    for extension in extensions:
        try:
            print(f"[LOG] ... Cargando {extension} ...")
            await bot.load_extension(extension)
            print(f"✅ [LOG] ÉXITO al cargar: {extension}")
        except Exception as e:
            print(f"❌ [LOG-ERROR] FALLÓ al cargar {extension}. Error: {e}")
    
    print("🤖 [LOG] load_extensions() COMPLETADA.")

# Asignamos la función al 'setup_hook'
print("[LOG] Asignando load_extensions al bot.setup_hook...")
bot.setup_hook = load_extensions
print("[LOG] bot.setup_hook ASIGNADO.")

# ====================================================
# IV. EVENTO ON_READY
# ====================================================

print("[LOG] --- SECCIÓN IV: EVENTO ON_READY ---")

@bot.event
async def on_ready():
    """Se ejecuta cuando el bot está conectado y los Cogs están cargados."""
    print("\n=============================================")
    print(f"✅ [LOG] ¡EVENTO on_ready() EJECUTADO! Bot Conectado como: {bot.user.name}")
    print("=============================================\n")
    
    print("[LOG] on_ready: Iniciando bloque try/except de Sincronización.")
    try:
        if MY_GUILD:
            print(f"🔄 [LOG] Sincronizando comandos para el servidor (Guild): {MY_GUILD.id}...")
            synced = await bot.tree.sync(guild=MY_GUILD)
        else:
            print("🔄 [LOG] Sincronizando comandos globalmente...")
            synced = await bot.tree.sync()
            
        # ESTA ES LA LÍNEA MÁS IMPORTANTE
        print("\n=============================================")
        print(f"✅ [LOG] ¡Sincronización completada! Comandos sincronizados: {len(synced)}")
        print("=============================================\n")
            
    except Exception as e:
        print(f"❌ [LOG-ERROR] Error fatal durante la sincronización: {e}")
    
    print("[LOG] Render deployment successful (mensaje de on_ready).")
    print("-------------------------------------------\n")

print("[LOG] Evento on_ready DEFINIDO.")

# ====================================================
# V. EJECUCIÓN DEL SERVICIO
# ====================================================

print("[LOG] --- SECCIÓN V: EJECUCIÓN ---")

def start_bot_and_server():
    """Inicia el bot y el servidor web."""
    print("[LOG] start_bot_and_server() INICIADA.")
    
    print("🚀 [LOG] Creando hilo del Bot de Discord...")
    discord_thread = threading.Thread(target=run_discord)
    print("🚀 [LOG] Iniciando hilo del Bot de Discord (thread.start())...")
    discord_thread.start()
    
    port = int(os.environ.get('PORT', 10000)) 
    print(f"✅ [LOG] Abriendo servidor Waitress en puerto {port} (esto bloqueará el hilo principal)...")
    serve(app, host='0.0.0.0', port=port)

# Punto de entrada
if __name__ == '__main__':
    print("[LOG] __name__ == '__main__' (Punto de entrada) detectaado.")
    start_bot_and_server()
else:
    print("[LOG] __name__ != '__main__' (Script importado?).")
