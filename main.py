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

# Definimos los intents (permisos) MÍNIMOS del Bot
intents = discord.Intents.default()

# Creamos la instancia del Bot
# El 'command_prefix' es irrelevante para slash commands, pero se deja
bot = commands.Bot(command_prefix='/', intents=intents) 

# ====================================================
# II. FUNCIONES DE INFRAESTRUCTURA (Render)
# ====================================================

@app.route('/')
def home():
    """Endpoint para que UptimeRobot haga ping."""
    return "Bot de prueba simple está activo!"

def run_discord():
    """Se ejecuta en un hilo para conectar el bot a Discord."""
    TOKEN = os.getenv('DISCORD_TOKEN')
    
    if TOKEN is None:
        print("\n[ERROR] TOKEN NO ENCONTRADO. Configúralo en las Environment Variables de Render.")
        return
        
    try:
        print("🤖 [INFO] Conectando a Discord...")
        bot.run(TOKEN) 
    except Exception as e:
        print(f"❌ Error al conectar Discord: {e}")

# ====================================================
# III. CÓDIGO DEL BOT (Simple)
# ====================================================

@bot.event
async def on_ready():
    """Se ejecuta cuando el bot está conectado y listo."""
    print('-------------------------------------------')
    print(f'✅ Bot Conectado como: {bot.user.name}')
    
    # SINCRONIZACIÓN DE SLASH COMMANDS
    try:
        # Sincroniza los comandos definidos en ESTE archivo
        print("🔄 [INFO] Sincronizando comandos...")
        synced = await bot.tree.sync()
        print(f"✅ Sincronizados {len(synced)} Slash Commands.")
        if len(synced) == 0:
            print("⚠️ [AVISO] No se sincronizó ningún comando. Revisa el código.")
    except Exception as e:
        print(f"❌ Error al sincronizar comandos: {e}")
    
    print('Render deployment successful.')
    print('-------------------------------------------')


# --- Definición del comando /hola ---
# Usamos @bot.tree.command() para definir un comando global
@bot.tree.command(name="hola", description="El bot te saluda.")
async def hola_command(interaction: discord.Interaction):
    """Responde con un saludo simple."""
    # .response.send_message() es la forma de responder
    await interaction.response.send_message("¡Hola! 👋")


# ====================================================
# IV. EJECUCIÓN DEL SERVICIO
# ====================================================

def start_bot_and_server():
    """Inicia el bot de Discord en un hilo y Waitress en el hilo principal."""
    
    print("🚀 Iniciando hilo del Bot de Discord...")
    discord_thread = threading.Thread(target=run_discord)
    discord_thread.start()
    
    # Abrimos el servidor web que Render espera
    port = int(os.environ.get('PORT', 10000)) 
    print(f"✅ Abriendo servidor Waitress en puerto {port} para Keep-Alive...")
    serve(app, host='0.0.0.0', port=port)

if __name__ == '__main__':
    start_bot_and_server()