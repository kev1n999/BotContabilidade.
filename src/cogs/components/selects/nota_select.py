import discord 

from functions.sheets import criar_planilha_nota, authenticate_google_sheets
from functions.transcript import generate_transcript
from components.modals.modals import ticket_historic

class NotaSelect(discord.ui.Select):
    def __init__(self, ticket_channel, staff):
        self.ticket_channel = ticket_channel
        self.staff = staff 
        
        options = [
            discord.SelectOption(label="Bom", value="Bom"),
            discord.SelectOption(label="Ruim", value="Ruim"),
            discord.SelectOption(label="Excelente", value="Excelente"),
        ]
        super().__init__(placeholder="Como você nos avalia?", options=options)
        
    async def callback(self, interaction: discord.Interaction):
        nota = self.values[0]
        ticket_historic[self.ticket_channel.id]["nota"] = nota
        await generate_transcript(ticket_historic[self.ticket_channel.id], interaction.user)
        
        nota_map = {"Bom": 0, "Ruim": 1, "Excelente": 2}
        nota_numerica = nota_map.get(nota, None)
        if nota_numerica is not None:
            criar_planilha_nota(authenticate_google_sheets(), user=self.staff.name, user_id=self.staff.id, nota=nota_numerica)
        
        await interaction.channel.set_permissions(interaction.user, view_channel=False, send_messages=False)
        await self.ticket_channel.send("Este ticket foi fechado pelo cliente.")