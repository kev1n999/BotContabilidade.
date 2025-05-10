import discord
from discord.ext import commands
from components.selects.options_select import SelectMenuOptions
from components.buttons.orcamento import OrcamentoButton

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    
    @commands.has_permissions(administrator=True)
    @commands.command(name="abrir")
    async def ticket(self, ctx, arg = None):
        if arg is None:
            view = discord.ui.View(timeout=None)
            view.add_item(SelectMenuOptions())
            
            embed = discord.Embed(title="Central de suporte", description="""
**Nessa sessão você pode entrar em contato com a nossa equipe.**\n\n**Horário de atendimento**\n・Segunda a Sabádo das **8h às 18h**\nAguarde ser atendido.\n""", color=0xFFFFFF)
            desc = """
・**Contábil**
・**RH**
・**Fiscal**
・**Certificado Digital**
・**Consultoria**
・**Registro de marcas e patentes**"""

            embed.add_field(name="CONHEÇA NOSSOS SERVIÇOS", value=desc, inline=True)
            embed.set_footer(text="Escolha uma opção")
            embed.set_thumbnail(url=ctx.guild.icon.url)
            embed.set_footer(text=ctx.guild.name, icon_url=self.bot.user.display_avatar.url)
            
            await ctx.message.delete()
            await ctx.send(embed=embed, view=view)
            return 
        
        if arg == "orçamento" or arg == "orcamento":
            embed = discord.Embed(title="Central de suporte", description="""
**Nessa sessão você pode entrar em contato com a nossa equipe.**\n\n**Horário de atendimento**\n・Segunda a Sabádo das **8h às 18h**\n**FAÇA JÁ SEU ORÇAMENTO.**\n""", color=0xFFFFFF)
            desc = """
・**Contábil**
・**RH**
・**Fiscal**
・**Certificado Digital**
・**Consultoria**
・**Registro de marcas e patentes**"""

            embed.add_field(name="TRABALHAMOS COM:", value=desc, inline=True)
            embed.set_footer(text="Escolha uma opção")
            embed.set_thumbnail(url=ctx.guild.icon.url)
            embed.set_footer(text=ctx.guild.name, icon_url=self.bot.user.display_avatar.url)
            await ctx.send(view=discord.ui.View(OrcamentoButton()), embed=embed)
            await ctx.message.delete()
        
def setup(bot):
    bot.add_cog(TicketSystem(bot))
