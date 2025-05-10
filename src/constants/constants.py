from json import load 

with open("../config/config.json", "r") as config:
    file = load(config)
    CATEGORIES = file["categorys"]

BOT_PREFIX = file["prefix"]
WELCOME_CHANNEL = file["canal_boasvindas"]

STAFF_ROLE = file["staff_role"]
TRANSCRIPT_CHANNEL = file["canal_transcripts"]

COMERCIAL = CATEGORIES["comercial"]
CONTABIL = CATEGORIES["contabil"]
RH = CATEGORIES["rh"]
FISCAL = CATEGORIES["fiscal"]
CERTIFICADO_DIGITAL = CATEGORIES["certificado_digital"]
CONSULTORIA = CATEGORIES["consultoria"]
MARCAS_E_PATENTES = CATEGORIES["registro_de_marcas_patentes"]
ORCAMENTO = CATEGORIES["orcamento"]


STAFF_ROLE = file["staff_role"]
STAFF_ROLE_ID = file["staff_role"]
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SHEET_ID = file["sheet_id"]