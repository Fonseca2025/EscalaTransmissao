import pandas as pd
import datetime
import requests
import os

# Configurações do Telegram
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def enviar_para_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "HTML"}
    requests.post(url, json=payload)

def processar_escala():
    # Carregar escala
    df = pd.read_csv('escala.csv')
    
    # Definir data de amanhã
    amanha = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%d/%m/%Y')
    
    # Filtrar agentes de amanhã
    agentes_amanha = df[df['data'] == amanha]
    
    if not agentes_amanha.empty:
        header = f"<b>📅 ESCALA DE AMANHÃ ({amanha})</b>\n"
        header += "<i>Copie as mensagens abaixo para enviar:</i>\n\n"
        enviar_para_telegram(header)
        
        for _, row in agentes_amanha.iterrows():
            # Monta o texto que você vai copiar e colar
            texto_copia = (
                f"Olá {row['agente']}, tudo bem? 🕊️\n\n"
                f"Passando para lembrar da sua escala na <b>Pascom</b> amanhã:\n"
                f"📍 <b>Missa:</b> {row['missa']}\n"
                f"🎥 <b>Função:</b> {row['funcao']}\n\n"
                f"Consegue confirmar a presença?"
            )
            # Envia cada bloco separado para facilitar a cópia
            enviar_para_telegram(f"<code>{texto_copia}</code>")
    else:
        enviar_para_telegram(f"✅ Não há ninguém escalado para amanhã ({amanha}).")

if __name__ == "__main__":
    processar_escala()
