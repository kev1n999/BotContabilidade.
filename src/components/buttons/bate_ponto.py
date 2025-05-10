import discord 
from datetime import datetime, timedelta 

from database.bases import bate_ponto
from functions.sheets import write_to_user_sheet

db = bate_ponto.BatePontoDatabase()
cursor = db.cursor

horario_brasilia = datetime.utcnow() - timedelta(hours=3)

class PontoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Iniciar", style=discord.ButtonStyle.success, custom_id="ponto_iniciar")
    async def iniciar_ponto(self, button: discord.ui.Button, interaction: discord.Interaction):
        user_id = interaction.user.id

        cursor.execute("SELECT inicio FROM ponto WHERE user_id = ? AND termino IS NULL", (user_id,))
        registro = cursor.fetchone()
        if registro:
            await interaction.response.send_message(
                "Você já iniciou o ponto! Por favor, encerre o ponto atual antes de iniciar um novo.",
                ephemeral=True
            )
            return

        try:
            cursor.execute("INSERT INTO ponto (user_id, inicio) VALUES (?, ?)", (user_id, horario_brasilia))
            db.db.commit()

            await interaction.response.send_message(f"Seu ponto foi iniciado às {horario_brasilia.strftime('%H:%M')}.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Erro ao iniciar o ponto: {e}", ephemeral=True)

    @discord.ui.button(label="Pausar", style=discord.ButtonStyle.secondary, custom_id="ponto_pausar")
    async def pausar_ponto(self, button: discord.ui.Button, interaction: discord.Interaction):
        user_id = interaction.user.id

        try:
            cursor.execute("SELECT id FROM ponto WHERE user_id = ? AND termino IS NULL", (user_id,))
            ponto_id = cursor.fetchone()

            cursor.execute("SELECT id FROM pausas WHERE user_id = ? AND retorno IS NULL", (user_id,))
            pausa = cursor.fetchone()

            if pausa:
                await interaction.response.send_message(
                    "Você já está com o ponto pausado. Retome antes de pausar novamente.",
                    ephemeral=True
                )
                return

            if not ponto_id:
                await interaction.response.send_message(
                    "Você não iniciou nenhum ponto para pausar.",
                    ephemeral=True
                )
                return

            pausa = horario_brasilia
            ponto_id = ponto_id[0]
            cursor.execute(
                "INSERT INTO pausas (user_id, ponto_id, pausa) VALUES (?, ?, ?)",
                (user_id, ponto_id, pausa)
            )
            db.db.commit()

            await interaction.response.send_message(f"Ponto pausado às {pausa.strftime('%H:%M')}.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Erro ao pausar o ponto: {e}", ephemeral=True)

    @discord.ui.button(label="Retomar", style=discord.ButtonStyle.primary, custom_id="ponto_retornar")
    async def retomar_ponto(self, button: discord.ui.Button, interaction: discord.Interaction):
        user_id = interaction.user.id

        try:
            cursor.execute("SELECT id FROM pausas WHERE user_id = ? AND retorno IS NULL", (user_id,))
            pausa_id = cursor.fetchone()

            if not pausa_id:
                await interaction.response.send_message(
                    "Você não possui nenhuma pausa para retomar.",
                    ephemeral=True
                )
                return

            retorno = horario_brasilia()
            pausa_id = pausa_id[0]
            cursor.execute("UPDATE pausas SET retorno = ? WHERE id = ?", (retorno, pausa_id))
            db.db.commit()

            await interaction.response.send_message(f"Ponto retomado às {retorno.strftime('%H:%M')}.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Erro ao retomar o ponto: {e}", ephemeral=True)

    @discord.ui.button(label="Encerrar", style=discord.ButtonStyle.danger, custom_id="ponto_encerrar")
    async def encerrar_ponto(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        user_id = interaction.user.id
        termino = horario_brasilia()
        
        try:
            cursor.execute("SELECT id, inicio FROM ponto WHERE user_id = ? AND termino IS NULL", (user_id,))
            registro = cursor.fetchone()

            if not registro:
                await interaction.response.send_message(
                    "Você não possui nenhum ponto iniciado para encerrar.",
                    ephemeral=True
                )
                return

            ponto_id, inicio = registro
            inicio = datetime.fromisoformat(inicio)

            cursor.execute("SELECT pausa, retorno FROM pausas WHERE user_id = ? AND ponto_id = ?", (user_id, ponto_id))
            pausas = cursor.fetchall()

            total_pausa = timedelta()  
            pausas_formatadas = [] 

            for pausa, retorno in pausas:
                pausa_dt = datetime.fromisoformat(pausa)
                retorno_dt = datetime.fromisoformat(retorno) if retorno else None

                if retorno_dt:
                    total_pausa += retorno_dt - pausa_dt
                pausas_formatadas.append(f"{pausa_dt.strftime('%H:%M')} às {retorno_dt.strftime('%H:%M') if retorno_dt else '-'}")

            if not pausas_formatadas:
                pausas_formatadas = ["-"]
            else:
                pausas_formatadas = "\n".join(pausas_formatadas)

            duracao = termino - inicio - total_pausa
            tempo_trabalhado = f"{duracao.seconds // 3600}h {duracao.seconds % 3600 // 60}m"

            cursor.execute("UPDATE ponto SET termino = ?, tempo_trabalhado = ? WHERE id = ?", (termino, tempo_trabalhado, ponto_id))
            db.db.commit()

            display_name = interaction.user.display_name
            data = horario_brasilia().strftime("%d/%m/%Y")
    
            write_to_user_sheet(display_name, user_id, data, inicio.strftime('%H:%M'), termino.strftime('%H:%M'), pausas_formatadas, tempo_trabalhado)
            
            mensagem = (
                f"Seu ponto foi encerrado!\n"
                f"Data: {data}\n"
                f"Horário de início: {inicio.strftime('%H:%M')}\n"
                f"Horário de término: {termino.strftime('%H:%M')}\n"
                f"Horários de pausa:\n{pausas_formatadas}\n"
                f"Tempo trabalhado: {tempo_trabalhado}\n"
            )
            
            await interaction.followup.send(mensagem, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Erro ao encerrar o ponto: {e}", ephemeral=True)