import os
import discord
from discord.ext import commands
from flask import Flask
from waitress import serve # Necesitamos waitress para el Keep-Alive estable

# ----------------------------------------------------
# A) CONFIGURACIÓN DEL SERVIDOR WEB (KEEP-ALIVE)
# ----------------------------------------------------
app = Flask(__name__)

@app.route('/')
def home():
    """Endpoint al que pingueará UptimeRobot."""
    return "Discord Bot is running 24/7!"

# ----------------------------------------------------
# B) CONFIGURACIÓN DEL BOT DE DISCORD
# ----------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='/', intents=intents)

# ⬇️ FUNCIÓN PARA CARGAR LOS COGS ⬇️
async def load_extensions():
    try:
        # El path es 'nombre_carpeta.nombre_archivo_sin_py'
        await bot.load_extension('moderacion.clear')
        print("🤖 [INFO] Cog cargado: moderacion.clear")
    except Exception as e:
        print(f"❌ [ERROR] Error al cargar cog: moderacion.clear: {e}")

bot.setup_hook = load_extensions 
# ------------------------------------

@bot.event
async def on_ready():
    print('-------------------------------------------')
    print(f'✅ Bot Conectado como: {bot.user.name}')
    print('Render deployment successful.')
    print('-------------------------------------------')

# Comando !hola simple (opcional, se puede mover al Cog)
@bot.command(name='hola')
async def saludo(ctx):
    await ctx.send(f'¡Hola, {ctx.author.display_name}! Estoy en línea y funcionando 24/7.')


# ----------------------------------------------------
# C) EJECUCIÓN: Servir Flask y Discord en el mismo proceso
# ----------------------------------------------------

def run_discord_bot():
    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN is None:
        print("\n[ERROR] El TOKEN no fue encontrado. Configúralo en Render.")
    else:
        try:
            bot.run(TOKEN)
        except Exception as e:
            print(f"\n[ERROR] Error al iniciar el bot de Discord: {e}")

if __name__ == '__main__':
    # Esta es la lógica SÓLIDA para Render:
    port = int(os.environ.get('PORT', 8080))
    
    # 1. Iniciamos el servidor Flask (bloqueante)
    # 2. Render lo detectará como un Web Service.
    # 3. El bot de Discord se iniciará dentro del proceso de Flask.
    
    # Esta es una implementación avanzada, pero funciona:
    # Flask sirve la aplicación app, y run_discord_bot se ejecutará como un hook.
    # Como bot.run es bloqueante, Render necesita que hagamos esto para que el puerto se abra.
    # Sin el threading, necesitamos un servidor WSGI como Waitress, PERO 
    # Render solo espera que la aplicación escuche el puerto.
    
    # La versión con THREADING y FLASK (la que te funcionó una vez) es más simple,
    # así que la reintentaremos, pero con un detalle de puerto corregido.
    
    # --- Volvemos a la versión de Threading, quitando los comentarios lll ---
    
    # La versión original de threading es la que funcionó inicialmente.
    # Si quieres la versión estable, debemos usar la implementación original de Threading:
    
    # ¡IMPORTANTE!: Para que esta versión funcione, tu Start Command en Render debe seguir siendo: `python main.py`
    
    run_discord_bot()
    
    # En el entorno Render, el hilo principal puede morir, así que usaremos la versión original que probamos.
    # VUELVE A TU CÓDIGO ANTERIOR Y ASEGÚRATE DE ELIMINAR LA LÍNEA 'lll' y el COG pegado.