import pandas as pd
import datetime
import requests
import os
import pytz

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
    
    # Ajustar para o fuso horário de Brasília (evita erro de data à noite)
    fuso = pytz.timezone('America/Sao_Paulo')
    hoje_brasil = datetime.datetime.now(fuso)
    amanha = (hoje_brasil + datetime.timedelta(days=1)).strftime('%d/%m/%Y')
    
    print(f"Procurando escala para: {amanha}")

    # Filtrar agentes usando os nomes exatos da sua imagem: 'dados' e 'função'
    # Usamos .str.strip() para remover espaços invisíveis que podem haver no CSV
    df.columns = df.columns.str.strip()
    agentes_amanha = df[df['dados'] == amanha]
    
    if not agentes_amanha.empty:
        header = f"<b>📅 ESCALA DE AMANHÃ ({amanha})</b>\n"
        header += "<i>Copie as mensagens abaixo para enviar:</i>\n\n"
        enviar_para_telegram(header)
        
        for _, row in agentes_amanha.iterrows():
            texto_copia = (
                f"Olá {row['agente']}, tudo bem? 🕊️\n\n"
                f"Passando para lembrar da sua escala na <b>Pascom</b> amanhã:\n"
                f"📍 <b>Missa:</b> {row['missa']}\n"
                f"🎥 <b>Função:</b> {row['função']}\n\n"
                f"Consegue confirmar a presença?"
            )
            enviar_para_telegram(f"<code>{texto_copia}</code>")
            print(f"Mensagem preparada para {row['agente']}")
    else:
        enviar_para_telegram(f"✅ Não há ninguém escalado para amanhã ({amanha}).")
        print("Ninguém encontrado para amanhã.")

if __name__ == "__main__":
    processar_escala()
