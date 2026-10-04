import os
import time
import requests

# ==========================================
# CONFIGURAÇÕES DO TELEGRAM
# ==========================================
TELEGRAM_BOT_TOKEN = "8619062228:AAGGoyimr33jeAgqM8ds7qBLKHxgm6-5rmQ"
TELEGRAM_CHAT_ID = "@ofertasfitness0080"

# Parâmetros de busca no Mercado Livre
SITE_ID = "MLB"  # Mercado Livre Brasil
TERMO_BUSCA = "suplementos fitness"
LIMITE_PRODUTOS = 5


def enviar_mensagem_telegram(texto):
    """Envia mensagem para o canal do Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    try:
        resposta = requests.post(url, json=payload)
        return resposta.status_code == 200
    except Exception as e:
        print(f"Erro ao enviar para o Telegram: {e}")
        return False


def buscar_e_enviar_ofertas():
    """Busca ofertas no Mercado Livre e publica no Telegram."""
    url = f"https://api.mercadolibre.com/sites/{SITE_ID}/search"
    params = {
        "q": TERMO_BUSCA,
        "limit": LIMITE_PRODUTOS
    }
    
    try:
        resposta = requests.get(url, params=params)
        if resposta.status_code == 200:
            dados = resposta.json()
            resultados = dados.get("results", [])
            
            if not resultados:
                print("Nenhuma oferta encontrada.")
                return

            print(f"Encontradas {len(resultados)} ofertas. Enviando para o Telegram...")
            
            for item in resultados:
                titulo = item.get("title")
                preco = item.get("price")
                link = item.get("permalink")
                
                mensagem = (
                    f"🔥 *OFERTA FITNESS ENCONTRADA!*\n\n"
                    f"📌 *Produto:* {titulo}\n"
                    f"💰 *Preço:* R$ {preco:.2f}\n\n"
                    f"🔗 [Clique aqui para ver a oferta]({link})"
                )
                
                enviar_mensagem_telegram(mensagem)
                time.sleep(2)  # Pausa de 2 segundos entre mensagens
                
            print("Envio concluído com sucesso!")
        else:
            print("Erro na API do Mercado Livre:", resposta.text)
    except Exception as e:
        print(f"Erro na execução da busca: {e}")


if __name__ == "__main__":
    print("=== EXECUTANDO BUSCA DE OFERTAS ===")
    buscar_e_enviar_ofertas()
    
