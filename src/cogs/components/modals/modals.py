import discord
from discord.ui import Modal, InputText, View
from json import load 
from database.bases import staffs
from functions.sheets import atualizar_recomendacao, get_recomendacao, criar_planilha_avaliacao, authenticate_google_sheets
from src.cogs.components.selects.nota_select import NotaSelect

db = staffs.StaffsDatabase()
cursor = db.cursor 

db.table_staff()
db.table_recomendacoes()
db.table_avaliacoes()

db.db.commit()
    
with open("config/config.json", "r") as config:
    file = load(config)

STAFF_ROLE = file["staff_role"]
TRANSCRIPT_CHANNEL = file["canal_transcripts"]

# --> REGISTRO <-- 
ticket_historic = {}
        
class AvaliacaoModal(Modal):
    def __init__(self, ticket_channel, user, staff):
        super().__init__(title="Deixe uma avaliação")
        self.ticket_channel = ticket_channel
        self.user = user
        self.staff = staff 
        
        self.feedback = InputText(
            label="Deixe um feedback",
            placeholder="Descreva o que você achou do atendimento",
            style=discord.InputTextStyle.long,
            required=True
        )
        self.recomenda = InputText(
            label="Indicaria nosso escritório? Sim ou Não",
            placeholder="Digite Sim ou Não",
            style=discord.InputTextStyle.singleline,
            required=True 
        )

        self.add_item(self.feedback)
        self.add_item(self.recomenda)

    async def callback(self, interaction: discord.Interaction):
        if self.ticket_channel.id not in ticket_historic:
            await interaction.response.send_message("Erro: O histórico deste ticket não foi encontrado.", ephemeral=True)
            return

        # Salva a avaliação e feedback
        feedback = self.feedback.value
        recomenda = self.recomenda.value
        
        validas = ["sim", "não", "nao", "claro", "com certeza"]
        
        if (recomenda.lower() not in validas):
            await interaction.response.send_message(f"{interaction.user.mention}\n⚠ **Você deve responder apenas `sim ou não` ao recomendar nosso escritório! Tente avaliar novamente.**", ephemeral=True)
            await interaction.response.send_modal(self)
            return 

        # Atualizando o histórico de avaliação
        ticket_historic[self.ticket_channel.id]["feedback"] = feedback
        
        ticket_historic[self.ticket_channel.id]["recomenda"] = "Sim" if recomenda.lower() in ["sim", "claro", "com certeza"] else recomenda
        
        # Salva a avaliação no banco de dados
        cursor.execute("INSERT INTO Avaliacoes (staff_id, client_id, nota, recomenda) VALUES (?, ?, ?, ?)", (self.ticket_channel.id, interaction.user.id, ticket_historic[self.ticket_channel.id]["nota"], recomenda))
        db.db.commit()
        
        # Atualiza a recomendação no banco de dados
        recomendacao = "sim" if recomenda.lower() in ["sim", "claro", "com certeza"] else "nao"
        atualizar_recomendacao(self.staff.id, recomendacao)
        
        await interaction.response.send_message(view=View(NotaSelect(self.ticket_channel, self.staff)), ephemeral=True)

        sim, nao = get_recomendacao(user_id=self.staff.id)
        criar_planilha_avaliacao(authenticate_google_sheets(), sim=sim, nao=nao)

def setup():
    ...