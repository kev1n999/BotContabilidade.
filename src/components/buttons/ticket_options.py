import discord
from discord.ui import View, Button
from constants.constants import STAFF_ROLE
from database.bases import staffs
from modals.modals import AvaliacaoModal, ticket_historic

db = staffs.StaffsDatabase()
cursor = db.cursor

# BOTÃO PARA O FECHAMENTO DO TICKET
class TicketOptionsButtons(View):
    def __init__(self, user):
        super().__init__(timeout=None)
        self.user = user
        self.staff_assumiu = None 
        
    @discord.ui.button(label="Fechar Ticket(Cliente)", style=discord.ButtonStyle.red)
    async def close_ticket(self, button: Button, interaction: discord.Interaction):
        if interaction.user != self.user:
            return 
        
        # Envia o modal de avaliação
        modal = AvaliacaoModal(ticket_channel=interaction.channel, user=self.user, staff=self.staff_assumiu)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Desativar Ticket(Staff)", style=discord.ButtonStyle.blurple)
    async def desable_ticket(self, button: Button, interaction: discord.Interaction):
        has_permission = any(role.id == STAFF_ROLE for role in interaction.user.roles)
        if not has_permission:
            await interaction.response.send_message("Você não tem permissão para desativar este ticket.", ephemeral=True)
            return
        
        await interaction.channel.delete()

    @discord.ui.button(label="Assumir(Staff)", style=discord.ButtonStyle.green)
    async def assumir(self, button: Button, interaction: discord.Interaction):
        has_permission = any(role.id == STAFF_ROLE for role in interaction.user.roles)
        if not has_permission:
            return
        
        await interaction.response.send_message("Você assumiu este ticket. Pode continuar seu atendimento!", ephemeral=True)
        self.staff_assumiu = interaction.user
        cursor.execute("INSERT INTO Staffs VALUES(?, ?)", (interaction.channel.id, self.staff_assumiu.id))
        db.db.commit()
        ticket_historic[interaction.channel.id]["staff"] = interaction.user 
        button.disabled = True 
        await interaction.message.edit(view=self, content=f"Ticket assumido por: {self.staff_assumiu.mention}")