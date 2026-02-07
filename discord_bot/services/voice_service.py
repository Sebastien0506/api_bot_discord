import discord

async def join_voice(bot, guild_id: int, user_id: int):
    guild = bot.get_guild(guild_id)
    if not guild:
        raise Exception("Guild introuvable")

    member = guild.get_member(user_id)
    if not member or not member.voice:
        raise Exception("Utilisateur pas en vocal")

    channel = member.voice.channel
    vc = guild.voice_client

    if vc:
        await vc.move_to(channel)
    else:
        await channel.connect()
            



