import os
import random
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
        print(f"Status Telegram: {resposta.status_code}")
        return resposta.status_code == 200
    except Exception as e:
        print(f"Erro ao enviar para o Telegram: {e}")
        return False

def buscar_e_enviar_oferta_unica():
    """Busca produtos, seleciona um e envia no formato de promoção."""
    url = "https://dummyjson.com/products/category/sports-accessories"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    try:
        resposta = requests.get(url, headers=headers, timeout=10)
        if resposta.status_code == 200:
            dados = resposta.json()
            produtos = dados.get("products", [])
            
            if not produtos:
                print("Nenhuma oferta encontrada.")
                return

            # Seleciona apenas 1 produto aleatório da lista por execução
            item = random.choice(produtos)
            
            titulo = item.get("title")
            preco_atual = item.get("price") * 5  # Conversão aproximada para R$
            desconto_pct = int(item.get("discountPercentage", 15))
            
            # Cálculo do preço antigo sem desconto
            preco_antigo = preco_atual / (1 - (desconto_pct / 100))
            
            link_oferta = "https://www.mercadolivre.com.br"
            
            # Formatação exatamente igual ao layout desejado
            mensagem = (
                f"🔥 *ACHADO FITNESS EM OFERTA!* 🔥\n\n"
                f"💪 *{titulo}*\n\n"
                f"❌ De: ~R$ {preco_antigo:.2f}~\n"
                f"✅ *Por apenas: R$ {preco_atual:.2f} ({desconto_pct}% OFF)*\n\n"
                f"🛒 Garante o teu aqui:\n"
                f"👉 {link_oferta}\n\n"
                f"⚠️ _Oferta por tempo limitado!_"
            )
            
            print(f"Enviando 1 oferta para o Telegram: {titulo}")
            enviar_mensagem_telegram(mensagem)
            print("Envio concluído com sucesso!")
        else:
            print("Erro na requisição:", resposta.status_code)
    except Exception as e:
        print(f"Erro na execução da busca: {e}")

if __name__ == "__main__":
    print("=== EXECUTANDO BUSCA DE OFERTA ÚNICA ===")
    buscar_e_enviar_oferta_unica()
    
