import discord 
from discord.ext import commands 
from constants.constants import WELCOME_CHANNEL, file

class MemberJoined(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.get_channel(WELCOME_CHANNEL)

        if channel:
            embed = discord.Embed(
                description=(
                    f"""
    # Bem-vindo(a) à Central de Atendimento EMC! ❤️
    Olá {member.mention}, é um prazer ter você aqui!

    Caso **AINDA NÃO SEJA NOSSO CLIENTE**, clique aqui: <#{file["canal_orcamento"]}>.\n
    Caso já seja nosso **CLIENTE**, e precisa de um orçamento, cliquei aqui: <#{file["canal_atendimento"]}>."""
                ),
                color=discord.Color.from_rgb(245, 245, 245)  
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

            embed.set_footer(
                text="EMC - Escritório Massias de Contabilidade",
                icon_url=self.bot.user.display_avatar.url
            )

            await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(MemberJoined(bot))