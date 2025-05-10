import discord 
from constants.constants import *
from components.modals.modals import ticket_historic
from datetime import datetime 
from components.buttons.ticket_options import TicketOptionsButtons

class SelectMenuOptions(discord.ui.Select):
    def __init__(self, custom_id="select_menu_options"):
        super().__init__(placeholder="Selecione uma opção", custom_id=custom_id)
        self.comercial = discord.SelectOption(
            label="Comercial",
            description=None 
        )
        self.contabil = discord.SelectOption(
            label="Contábil",
            description="Lançamentos de entrada e saida, balanço patrimonial"
        )
        self.rh = discord.SelectOption(
            label="RH",
            description="Gestão de pessoas, folha de pagamento, rescisão trabalhistas, homologação..."
        )
        self.fiscal = discord.SelectOption(
            label="Fiscal",
            description="Apuração de impostos, envio das obrigações mensais, controle de entrada e saída"
        )
        self.certificadoDigital = discord.SelectOption(
            label="Certificado Digital",
            description="Venda, emissão e validação de certificação digital"
        )
        self.consultoria = discord.SelectOption(
            label="Consultoria",
            description="Consultoria financeira e empresarial"
        )
        self.marcas_patentes = discord.SelectOption(
            label="Marcas e patentes",
            description="Processos que envolvem o registro da sua marca"
        )
        
        self.options.append(self.comercial)
        self.options.append(self.contabil)
        self.options.append(self.rh)
        self.options.append(self.fiscal)
        self.options.append(self.certificadoDigital)
        self.options.append(self.consultoria)
        self.options.append(self.marcas_patentes)
        self.count = 1
        
    async def callback(self, interaction):
        #global ticket_counter

        ticket_name = f"📂 ticket-{interaction.user}"
        
        while discord.utils.get(interaction.guild.text_channels, name=ticket_name):
            ticket_counter += 1
            ticket_name = f"ticket-{ticket_counter}"

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(send_messages=True, view_channel=True),
            discord.utils.get(interaction.guild.roles, id=STAFF_ROLE): discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        ticket_id = None 
        
        if self.values[0] == "Comercial":
            ticket_id = COMERCIAL 
        elif self.values[0] == "Contábil":
            ticket_id = CONTABIL
        elif self.values[0] == "RH":
            ticket_id = RH 
        elif self.values[0] == "Fiscal":
            ticket_id = FISCAL 
        elif self.values[0] == "Certificado Digital":
            ticket_id = CERTIFICADO_DIGITAL    
        elif self.values[0] == "Consultoria":
            ticket_id = CONSULTORIA
        elif self.values[0] == "Marcas e patentes":
            ticket_id = MARCAS_E_PATENTES
            
        ticket_channel = await interaction.guild.create_text_channel(ticket_name, category=discord.utils.get(interaction.guild.categories, id=ticket_id), overwrites=overwrites)

        ticket_historic[ticket_channel.id] = {
            "user": interaction.user.name,
            "user_id": interaction.user.id,
            "data": datetime.now(),
            "messages": [{"author": "Sistema", "content": f"Ticket aberto por {interaction.user.name}", "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}],
            "feedback": None,
            "nota": None
        }

        embed = discord.Embed(title="📩  Novo ticket", description=f"**Usuário:** {interaction.user.mention}", color=0x2b2d31)
        embed.add_field(name="Opção escolhida", value=f"`{self.values[0]}`", inline=True)
        embed.set_footer(text="Espere para ser atendido")
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        
        await interaction.response.send_message(content=f"Seu ticket para {self.values[0]} foi criado em {ticket_channel.mention}", ephemeral=True)
        await ticket_channel.send(embed=embed, view=TicketOptionsButtons(interaction.user))
        await self.reset_select(interaction)
        
    async def reset_select(self, interaction:discord.Interaction):
        select = SelectMenuOptions()  

        view = discord.ui.View(timeout=None)
        view.add_item(select)
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
        embed.set_thumbnail(url=interaction.guild.icon.url)
        embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.me._user.display_avatar.url)
        
        await interaction.message.edit(embed=embed, view=view)