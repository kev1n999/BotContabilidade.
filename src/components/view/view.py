import discord
from buttons.orcamento import OrcamentoButton
from selects.options_select import SelectMenuOptions

class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SelectMenuOptions())
        self.add_item(OrcamentoButton())