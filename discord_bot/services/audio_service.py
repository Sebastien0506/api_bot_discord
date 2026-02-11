#Permet de générer l'audio d'un message
import discord
async def play_audio(channel, filepath) :
    #Si le bot n'est pas dans un salon on le connecte
    if not channel.guild.voice_client : 
        vc = await channel.connect()
    else : 
        vc = channel.guild.voice_client

    vc.play(discord.FFmpegPCMAudio(filepath))