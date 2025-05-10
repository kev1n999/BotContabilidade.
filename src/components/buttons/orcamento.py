import discord 
from modals.modals import ticket_historic
from datetime import datetime 
from buttons.ticket_options import TicketOptionsButtons
from constants.constants import ORCAMENTO, STAFF_ROLE

class OrcamentoButton(discord.ui.Button):
    def __init__(self, custom_id="orcamento_button"):
        super().__init__(custom_id=custom_id, label="Fazer orçamento", style=discord.ButtonStyle.blurple)
    
    async def callback(self, interaction:discord.Interaction):
        categorie_id = discord.utils.get(interaction.guild.categories, id=ORCAMENTO)
        overwrites = {interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False), interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True), discord.utils.get(interaction.guild.roles, id=STAFF_ROLE): discord.PermissionOverwrite(view_channel=True, send_messages=True)}
        ticket_channel = await interaction.guild.create_text_channel(f"📂 ticket-{interaction.user}", overwrites=overwrites, category=categorie_id)

        ticket_historic[ticket_channel.id] = {
            "user": interaction.user.name,
            "user_id": interaction.user.id,
            "data": datetime.now(),
            "messages": [{"author": "Sistema", "content": f"Ticket aberto por {interaction.user.name}", "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}],
            "feedback": None,
            "nota": None
        }
        
        await interaction.response.send_message(ephemeral=True, content="Seu ticket foi aberto com sucesso em {}".format(ticket_channel.mention))
        embed = discord.Embed(title="📩  Novo ticket", description=f"**Usuário:** {interaction.user.mention}", color=0x2b2d31)
        embed.add_field(name="Opção escolhida", value=f"`Orçamento`", inline=True)
        embed.set_footer(text="Espere para ser atendido")
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        
        await ticket_channel.send(embed=embed, view=TicketOptionsButtons(user=interaction.user))