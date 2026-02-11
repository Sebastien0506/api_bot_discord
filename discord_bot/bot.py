import os
import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

import django
django.setup()
import discord
if sys.platform == "darwin":
    try : 
        discord.opus.load_opus("/opt/homebrew/lib/libopus.dylib")
        print("✅ OPUS chargé manuellement")
    except Exception as e :
        print("❌ Erreur OPUS :", e)
print("🧪 OPUS chargé ?", discord.opus.is_loaded())
import asyncio
from discord.ext import commands
from discord_bot.services.generate_audio_message_service import generate_audio_message_service
from discord.ext import commands, tasks
from discord_bot.services.pending_actions_service import (
    get_pending_actions, 
    mark_action_done
)
from discord_bot.models import PendingAction
from dotenv import load_dotenv


load_dotenv()

# 🔐 Déclaration des intents
intents = discord.Intents.default()
intents.message_content = True   # 👈 OBLIGATOIRE pour lire les messages
intents.guilds = True
intents.members = True           # (utile plus tard)
intents.voice_states = True      # 👈 OBLIGATOIRE pour le vocal

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    process_pending_actions.start()
    print(f"✅ Bot connecté en tant que {bot.user}")
    print("📦 Guilds visibles par le bot :")

    for g in bot.guilds :
        print(f" - {g.name} ({g.id})")

@tasks.loop(seconds=1)
async def process_pending_actions():
    actions = await get_pending_actions()

    if not actions:
        return

    print("👀 Tick process_pending_actions")

    for action in actions:
        print(f"➡️ Action trouvée : {action}")

        # ─────────────────────────────
        # ACTION : JOIN VOICE
        # ─────────────────────────────
        if action.action == "join_voice":
            channel = bot.get_channel(action.channel_id)
            print("CHANNEL =", channel)

            if not channel:
                print("❌ Channel introuvable")
                continue

            voice_client = channel.guild.voice_client

            if voice_client is None:
                await channel.connect()
            else:
                await voice_client.move_to(channel)

            print("✅ Bot connecté au salon vocal")

        # ─────────────────────────────
        # ACTION : VOICE MESSAGE
        # ─────────────────────────────
        elif action.action == "voice_message":
            payload = action.payload

            if not payload or "message" not in payload:
                print("❌ Payload manquant")
                await mark_action_done(action)
                continue

            message = payload["message"]

            #Salon vocal ciblé par l'action
            action_channel = bot.get_channel(action.channel_id)
            if not action_channel :
                print("❌ Channel introuvable")
                continue
            
            vc = action_channel.guild.voice_client
            if not vc or not vc.is_connected():
                print("❌ Bot pas connecté en vocal")
                continue

            filepath = generate_audio_message_service(message)
            vc.play(discord.FFmpegPCMAudio(filepath))

            # 3️⃣ jouer l’audio
            if vc.is_playing():
                vc.stop()

            audio = discord.FFmpegPCMAudio(filepath)
            vc.play(audio)

            print("▶️ Lecture démarrée")

            while vc.is_playing():
                await asyncio.sleep(0.2)

            print("⏹️ Lecture terminée")

        # ─────────────────────────────
        # FIN : action traitée
        # ─────────────────────────────
        await mark_action_done(action)
        print("✅ Action exécutée et marquée comme done")

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN :
    raise RuntimeError("❌ DISCORD_TOKEN manquant")

print("🚀 Démarrage du bot Discord")
bot.run(TOKEN)
