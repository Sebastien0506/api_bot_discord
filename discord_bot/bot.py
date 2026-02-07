import os
import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

import django
django.setup()
import discord
from discord.ext import commands

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

    if not actions :
        return
    
    print("👀 Tick process_pending_actions")
    #Pour tout les actions
    for action in actions:
        print(f"➡️ Action trouvée : {action}")
        
        #On récupère tous les channel
        channel = bot.get_channel(action.channel_id)
        print("CHANNEL =", channel)

        if not channel:
            print("❌ Guild introuvable")
            continue
        #On récupère les membres de chaque channel
        member = discord.utils.get(channel.members, id=action.user_id)
        print("MEMBER =", member)

        if not member:
            print("❌ Le membre n'est pas dans le salon vocal.")
            continue

        # 👉 S’il est bien en vocal
        channel = member.voice.channel
        print("🎙️ Channel =", channel)

        voice_client = channel.guild.voice_client
        #Si le bot n'est pas connecté on le connect
        if voice_client is None:
            await channel.connect()
        else : 
            await voice_client.move_to(channel)

        await mark_action_done(action)
        print("✅ Action exécutée et marquée comme done")

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN :
    raise RuntimeError("❌ DISCORD_TOKEN manquant")

print("🚀 Démarrage du bot Discord")
bot.run(TOKEN)
