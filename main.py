import os
import discord
from discord.ext import commands
# IMPORTANTE: Eliminamos threading
from flask import Flask
from waitress import serve 

# ... (Sección A, B - El resto del código de Flask y Discord es el mismo) ...

# ----------------------------------------------------
# C) EJECUCIÓN ESTABLE CON WAITRESS (SIN THREADING)
# ----------------------------------------------------

def start_bot_and_server():
    # 1. Obtenemos el token
    TOKEN = os.getenv('DISCORD_TOKEN')

    if TOKEN is None:
        print("\n[ERROR] TOKEN NO ENCONTRADO. Configúralo en las Environment Variables de Render.")
        return

    # 2. Definimos el puerto que Render nos da (o el 8080 por defecto)
    port = int(os.environ.get('PORT', 8080))

    # 3. La lógica clave: ejecutamos el bot de Discord en el fondo
    #    y luego iniciamos Waitress para que Render detecte el puerto.

    # Usaremos una solución simple: conectamos el bot en un hilo, 
    # y luego dejamos que Waitress bloquee el hilo principal (que es lo que Render espera).
    
    # Crear un hilo para el bot.run()
    # Aunque eliminamos la importación de threading arriba, lo necesitamos aquí para que bot.run()
    # no bloquee la ejecución de Waitress. (Es una de las pocas veces que el threading es necesario en Render.)
    
    import threading 
    
    def run_discord():
        try:
            bot.run(TOKEN)
        except Exception as e:
            print(f"❌ Error al conectar Discord: {e}")
            
    # Iniciamos el bot en un hilo
    discord_thread = threading.Thread(target=run_discord)
    discord_thread.start()
    
    # Abrimos Waitress en el hilo principal
    print(f"✅ Abriendo servidor Waitress en puerto {port} para Keep-Alive...")
    serve(app, host='0.0.0.0', port=port)

if __name__ == '__main__':
    # Esta función ahora maneja el inicio de ambos
    start_bot_and_server()