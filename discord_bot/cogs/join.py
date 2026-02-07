from discord import commands

@commands.command()
async def join(self, ctx) : 
    try : 
        channel_name = await self.joinService.join_voice(
            ctx.guild.id,
            ctx.author.id
        )
        await ctx.send(f"🎙️ Connecté à {channel_name}")
    except Exception as e :
        await ctx.send(f"❌ {e}")