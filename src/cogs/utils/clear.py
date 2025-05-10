from discord.ext import commands

class ClearCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    
    @commands.has_permissions(administrator=True)
    @commands.slash_command(name="clear", description="Limpa uma quantidade específica de mensagens no chat atual.")
    async def clear(self, interaction, quantidade: int):
        if quantidade < 10:
            await interaction.response.send_message(ephemeral=True, content="Quantidade inválida! A quantidade mínima de mensagens para apagar é **10**.")
            return 
        
        elif quantidade > 100:
            await interaction.response.send_message(ephemeral=True, content="Quantidade inválida! A quantidade máxima de mensagens para apagar é **100**.")
            return 
        
        messages = await interaction.channel.purge(limit=quantidade)
        await interaction.response.send_message(f"-# ✅  | Foram deletadas {len(messages)} mensagens em {interaction.channel.mention} com sucesso!", delete_after=20.0)
        
def setup(bot):
    bot.add_cog(ClearCommand(bot))