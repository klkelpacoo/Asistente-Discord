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

# === NUEVO: Cargar el ID del servidor ===
# Lee la variable de entorno que acabas de añadir en Render.
GUILD_ID_FROM_ENV = os.getenv('GUILD_ID')
MY_GUILD = None

if GUILD_ID_FROM_ENV:
    try:
        # Crea un objeto 'Guild' que el bot puede entender
        MY_GUILD = discord.Object(id=int(GUILD_ID_FROM_ENV))
        print(f"✅ [INFO] Se cargó el GUILD_ID: {GUILD_ID_FROM_ENV}")
    except ValueError:
        print(f"❌ [ERROR] El GUILD_ID '{GUILD_ID_FROM_ENV}' no es un número válido.")
else:
    print("⚠️ [AVISO] No se encontró la variable GUILD_ID. La sincronización será global y puede tardar 1 hora.")


# ====================================================
# II. FUNCIONES DE INFRAESTRUCTURA (Render)
# ====================================================

@app.route('/')
def home():
    return "Bot con Guild Sync está activo!"

def run_discord():
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
# III. CÓDIGO DEL BOT
# ====================================================

@bot.event
async def on_ready():
    print('-------------------------------------------')
    print(f'✅ Bot Conectado como: {bot.user.name}')
    
    # === SINCRONIZACIÓN MEJORADA ===
    try:
        if MY_GUILD:
            print(f"🔄 [INFO] Sincronizando comandos para el servidor {MY_GUILD.id}...")
            # Sincroniza SOLO para tu servidor (instantáneo)
            synced = await bot.tree.sync(guild=MY_GUILD)
        else:
            print("🔄 [INFO] Sincronizando comandos globalmente (puede tardar)...")
            # Sincronización global (lenta, hasta 1h)
            synced = await bot.tree.sync()
            
        print(f"✅ Sincronizados {len(synced)} Slash Commands.")
        if len(synced) == 0:
            print("⚠️ [AVISO] No se sincronizó ningún comando. Revisa el código.")
            
    except Exception as e:
        print(f"❌ Error al sincronizar comandos: {e}")
    
    print('Render deployment successful.')
    print('-------------------------------------------')


# --- Definición del comando /hola ---
# === CAMBIO IMPORTANTE ===
# Ahora le decimos que este comando pertenece a TU servidor.
# Esto hace que aparezca al instante.
@bot.tree.command(name="hola", description="El bot te saluda (Test de Guild).", guild=MY_GUILD)
async def hola_command(interaction: discord.Interaction):
    """Responde con un saludo simple."""
    # Solo responde si la interacción viene del servidor correcto
    if interaction.guild.id != MY_GUILD.id:
        return
    await interaction.response.send_message("¡Hola! 👋 (Versión Guild)")


# ====================================================
# IV. EJECUCIÓN DEL SERVICIO
# ====================================================

def start_bot_and_server():
    print("🚀 Iniciando hilo del Bot de Discord...")
    discord_thread = threading.Thread(target=run_discord)
    discord_thread.start()
    
    port = int(os.environ.get('PORT', 10000)) 
    print(f"✅ Abriendo servidor Waitress en puerto {port} para Keep-Alive...")
    serve(app, host='0.0.0.0', port=port)

if __name__ == '__main__':
    start_bot_and_server()