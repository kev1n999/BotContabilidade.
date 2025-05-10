import discord
from discord.ext import commands
from database.database import Database
from database.bases import bate_ponto
from constants.constants import STAFF_ROLE_ID 
from components.buttons.bate_ponto import PontoView

db = bate_ponto.BatePontoDatabase()
db.table_ponto()
db.table_pausas()
db.table_recommendations()


db_avaliacao = Database("staffs")
db_avaliacao_cursor = db_avaliacao.cursor

class BatePontoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ponto")
    async def ponto_command(self, ctx):        
        if discord.utils.get(ctx.author.roles, id=STAFF_ROLE_ID) is None:
            await ctx.send(f"❌ Você não tem permissão para usar este comando. Este recurso é restrito a membros com o cargo necessário.")
            return

        embed = discord.Embed(
            title="🕒 Gerenciamento de Ponto de Trabalho",
            description="Use os botões abaixo para registrar seu ponto.",
            color=discord.Color.from_rgb(245, 245, 245)
        )
        embed.set_footer(text="Sistema de Ponto Automático • Organize seu tempo com eficiência")

        view = PontoView()
        await ctx.send(embed=embed, view=view)

def setup(bot):
    bot.add_cog(BatePontoCommand(bot))