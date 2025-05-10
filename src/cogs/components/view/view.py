import discord
from cogs.components.buttons.orcamento import OrcamentoButton
from cogs.components.selects.options_select import SelectMenuOptions

class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SelectMenuOptions())
        self.add_item(OrcamentoButton())