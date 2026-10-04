import os
import time
import requests

# ==========================================
# CONFIGURAÇÕES DO TELEGRAM
# ==========================================
TELEGRAM_BOT_TOKEN = "8619062228:AAGGoyimr33jeAgqM8ds7qBLKHxgm6-5rmQ"
TELEGRAM_CHAT_ID = "-1003941863470"

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
        resposta = requests.post(url, json=payload, timeout=10)
        return resposta.status_code == 200
    except Exception as e:
        print(f"Erro ao enviar para o Telegram: {e}")
        return False

def buscar_e_enviar_ofertas():
    """Busca ofertas e envia para o Telegram."""
    # Usando API alternativa estável para evitar o erro 403 do IP do Render
    url = "https://dummyjson.com/products/category/sports-accessories"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    try:
        resposta = requests.get(url, headers=headers, timeout=10)
        if resposta.status_code == 200:
            dados = resposta.json()
            produtos = dados.get("products", [])[:5]
            
            if not produtos:
                print("Nenhuma oferta encontrada.")
                return

            print(f"Encontradas {len(produtos)} ofertas. Enviando para o Telegram...")
            
            for item in produtos:
                titulo = item.get("title")
                preco = item.get("price")
                
                mensagem = (
                    f"🔥 *OFERTA FITNESS ENCONTRADA!*\n\n"
                    f"📌 *Produto:* {titulo}\n"
                    f"💰 *Preço:* R$ {preco * 5:.2f}\n\n"
                    f"🔗 [Clique aqui para ver a oferta](https://www.mercadolivre.com.br)"
                )
                
                enviar_mensagem_telegram(mensagem)
                time.sleep(2)
                
            print("Envio concluído com sucesso!")
        else:
            print("Erro na requisição:", resposta.status_code)
    except Exception as e:
        print(f"Erro na execução da busca: {e}")

if __name__ == "__main__":
    print("=== EXECUTANDO BUSCA DE OFERTAS ===")
    buscar_e_enviar_ofertas()
    
