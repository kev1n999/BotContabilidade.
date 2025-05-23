# Código principal para enviar requisições para o google sheets 
import os 
import pickle 

from constants.constants import * 
from database.bases import bate_ponto, staffs
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

staff_db = staffs.StaffsDatabase() 
bate_ponto_db = bate_ponto.BatePontoDatabase()

def criar_planilha_avaliacao(service, nome_planilha="recomendações", sim=0, nao=0):
    # Recupera a lista de abas (sheets) existentes na planilha
    planilha = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    abas_existentes = [sheet['properties']['title'] for sheet in planilha['sheets']]

    # Verifica se a aba já existe
    if nome_planilha in abas_existentes:
        print(f"Aba '{nome_planilha}' já existe. Atualizando valores...")
    else:
        # Adiciona uma nova aba na planilha
        service.spreadsheets().batchUpdate(
            spreadsheetId=SHEET_ID,
            body={
                "requests": [
                    {
                        "addSheet": {
                            "properties": {
                                "title": nome_planilha
                            }
                        }
                    }
                ]
            }
        ).execute()
        print(f"Aba '{nome_planilha}' criada com sucesso.")

    # Define os valores iniciais a serem inseridos
    valores_iniciais = [
        ['Avaliação', 'Quantidade'],
        ['Sim', sim],
        ['Não', nao]
    ]
    
    # Atualiza os valores na aba
    service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID,
        range=f'{nome_planilha}!A1',
        valueInputOption='RAW',
        body={'values': valores_iniciais}
    ).execute()

    # URL da planilha
    planilha_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
    print(f"Planilha atualizada com sucesso: {planilha_url}")
    
def get_recomendacao(user_id):
    staff_db.cursor.execute("SELECT sim, nao FROM recomendacoes WHERE user_id = ?", (user_id,))
    recomendacoes = staff_db.cursor.fetchone()
    sim = recomendacoes[0] if recomendacoes else 0
    nao = recomendacoes[1] if recomendacoes else 0
    return sim, nao

def atualizar_recomendacao(user_id, recomendacao):
    # Verifica se o usuário já tem um registro na tabela de recomendacoes
    bate_ponto.cursor.execute("SELECT sim, nao FROM recomendacoes WHERE user_id = ?", (user_id,))
    resultado = bate_ponto_db.cursor.fetchone()

    if resultado:
        sim, nao = resultado
        if recomendacao == "sim":
            sim += 1
        elif recomendacao == "nao":
            nao += 1
        # Atualiza os valores de sim ou nao no banco de dados
        bate_ponto_db.cursor.execute("UPDATE recomendacoes SET sim = ?, nao = ? WHERE user_id = ?", (sim, nao, user_id))
        
    else:
        # Cria um novo registro com a primeira recomendação
        bate_ponto_db.cursor.execute("INSERT INTO recomendacoes (user_id, sim, nao) VALUES (?, ?, ?)", 
                       (user_id, 1 if recomendacao == "sim" else 0, 1 if recomendacao == "nao" else 0))

    bate_ponto_db.db.commit()

def criar_planilha_nota(service, nome_planilha="notas", user=None, user_id=None, nota=None):
    # Verifica se a planilha já existe
    sheets_metadata = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    sheets_titles = [sheet['properties']['title'] for sheet in sheets_metadata.get('sheets', [])]

    if nome_planilha not in sheets_titles:
        # Adiciona uma nova aba na planilha existente
        service.spreadsheets().batchUpdate(
            spreadsheetId=SHEET_ID,
            body={
                "requests": [
                    {
                        "addSheet": {
                            "properties": {
                                "title": nome_planilha
                            }
                        }
                    }
                ]
            }
        ).execute()

        valores_iniciais = [
            ['Nome', 'ID do Usuário', 'Bom', 'Ruim', 'Excelente'],
            [user, f'{user_id}', 0, 0, 0],
        ]

        if isinstance(nota, int) and 0 <= nota <= 2:  
            valores_iniciais[1][nota + 2] = 1  

        service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID,
            range=f'{nome_planilha}!A1',
            valueInputOption='RAW',
            body={'values': valores_iniciais}
        ).execute()

    else:
        # Atualiza a contagem da nota recebida na planilha existente
        valores = service.spreadsheets().values().get(
            spreadsheetId=SHEET_ID,
            range=f'{nome_planilha}!A2:G'
        ).execute().get('values', [])

        user_found = False  # Flag para verificar se o usuário foi encontrado

        for linha in valores:
            if linha[1] == f'{user_id}':
                user_found = True
                # Verifica se 'nota' está dentro do intervalo válido
                if isinstance(nota, int) and 0 <= nota <= 2:
                    # Incrementa a contagem da nota
                    linha[int(nota) + 2] = str(int(linha[int(nota) + 2]) + 1)
                break

        if not user_found:
            # Se o usuário não foi encontrado, cria uma nova linha
            nova_linha = [user, f'{user_id}', 0, 0, 0]
            if isinstance(nota, int) and 0 <= nota <= 2:
                nova_linha[nota + 2] = 1  # Marca a primeira avaliação recebida
            valores.append(nova_linha)

        service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID,
            range=f'{nome_planilha}!A2',  # Atualiza a partir da célula A2
            valueInputOption='RAW',
            body={'values': valores}
        ).execute()

    # URL da planilha
    planilha_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
    print(f"Planilha criada/atualizada com sucesso: {planilha_url}")

    
def authenticate_google_sheets():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        creds = Credentials.from_service_account_file(
            'config/hallowed-tea-387701-34bbaf2630f4.json', scopes=SCOPES)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('sheets', 'v4', credentials=creds)


def write_to_user_sheet(display_name, user_id, data, inicio, termino, pausas_formatadas, tempo_trabalhado):
    try:
        service = authenticate_google_sheets()
        sheet = service.spreadsheets()

        sheets_metadata = sheet.get(spreadsheetId=SHEET_ID).execute()
        sheets_titles = [sheet['properties']['title'] for sheet in sheets_metadata.get('sheets', [])]

        if display_name not in sheets_titles:
            sheet.batchUpdate(
                spreadsheetId=SHEET_ID,
                body={
                    "requests": [
                        {
                            "addSheet": {
                                "properties": {
                                    "title": display_name
                                }
                            }
                        }
                    ]
                }
            ).execute()

            header_values = [["Data", "Nome", "ID do Usuário", "Início", "Término", "Horários de Pausa", "Tempo Trabalhado"]]
            sheet.values().update(
                spreadsheetId=SHEET_ID,
                range=f"{display_name}!A1",
                valueInputOption="RAW",
                body={"values": header_values}
            ).execute()

        if isinstance(pausas_formatadas, list):
            pausas_formatadas = "\n".join(pausas_formatadas)
        if pausas_formatadas == []:
            pausas_formatadas = "-"

        # Dados para o novo registro
        values = [[data, display_name, f"'{user_id}", inicio, termino, pausas_formatadas, tempo_trabalhado]]
        sheet.values().append(
            spreadsheetId=SHEET_ID,
            range=f"{display_name}!A1",
            valueInputOption="RAW",
            body={"values": values}
        ).execute()

        # Atualiza a coluna de total
        sheet_data = sheet.values().get(
            spreadsheetId=SHEET_ID,
            range=f"{display_name}!G:G"
        ).execute()

        total_rows = len(sheet_data.get("values", [])) + 1
        formula_range = f"{display_name}!G{total_rows}"
        sheet.values().update(
            spreadsheetId=SHEET_ID,
            range=formula_range,
            valueInputOption="USER_ENTERED",
            body={"values": [[f"=SOMA(G2:G{total_rows - 1})"]]}).execute()
    except Exception as e:
        print(f"Erro ao gravar na planilha do Google: {e}")
