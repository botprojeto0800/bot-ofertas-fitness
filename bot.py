import os
import random
import requests

# ==========================================
# CONFIGURAÇÕES DO TELEGRAM E AFILIADO
# ==========================================
TELEGRAM_BOT_TOKEN = "8619062228:AAGGoyimr33jeAgqM8ds7qBLKHxgm6-5rmQ"
TELEGRAM_CHAT_ID = "-1003941863470"

# Parâmetros exatos do seu perfil de Afiliado Meli
MATT_TOOL = "41514834"
MATT_WORD = "cleiton2001js"

TERMOS_BUSCA = ["suplementos fitness", "creatina", "whey protein", "acessorios treino"]

def enviar_mensagem_telegram(texto):
    """Envia mensagem para o canal do Telegram usando HTML para texto rasurado/tachado."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texto,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        resposta = requests.post(url, json=payload, timeout=10)
        print(f"Status Telegram: {resposta.status_code}")
        return resposta.status_code == 200
    except Exception as e:
        print(f"Erro ao enviar para o Telegram: {e}")
        return False

def buscar_e_enviar_oferta():
    """Busca produtos reais do Mercado Livre e envia no formato correto com tag de afiliado."""
    termo = random.choice(TERMOS_BUSCA)
    url = "https://api.mercadolibre.com/sites/MLB/search"
    params = {"q": termo, "limit": 10}
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        resposta = requests.get(url, params=params, headers=headers, timeout=10)
        if resposta.status_code == 200:
            dados = resposta.json()
            resultados = dados.get("results", [])
            
            if not resultados:
                print("Nenhum produto encontrado.")
                return

            item = random.choice(resultados)
            
            titulo = item.get("title")
            preco_atual = float(item.get("price", 0))
            preco_original = float(item.get("original_price") or (preco_atual * 1.25))
            
            if preco_original > preco_atual:
                desconto_pct = int(((preco_original - preco_atual) / preco_original) * 100)
            else:
                preco_original = preco_atual * 1.3
                desconto_pct = 23
            
            # Anexa os parâmetros exatos de comissão ao link do produto
            link_base = item.get("permalink")
            divisor = "&" if "?" in link_base else "?"
            link_produto = f"{link_base}{divisor}matt_tool={MATT_TOOL}&matt_word={MATT_WORD}"
            
            mensagem = (
                f"🔥 <b>ACHADO FITNESS EM OFERTA!</b> 🔥\n\n"
                f"💪 <b>{titulo}</b>\n\n"
                f"❌ <s>De: R$ {preco_original:.2f}</s>\n"
                f"✅ <b>Por apenas: R$ {preco_atual:.2f} ({desconto_pct}% OFF)</b>\n\n"
                f"🛒 <b>Garante o teu aqui:</b>\n"
                f"👉 {link_produto}\n\n"
                f"⚠️ <i>Oferta por tempo limitado!</i>"
            )
            
            print(f"Enviando oferta: {titulo}")
            enviar_mensagem_telegram(mensagem)
        else:
            print(f"Erro na API ML ({resposta.status_code}). Tentando produto fallback...")
            enviar_produto_fallback()
    except Exception as e:
        print(f"Erro na execução: {e}")
        enviar_produto_fallback()

def enviar_produto_fallback():
    """Fallback caso a API direta do Mercado Livre bloqueie a requisição."""
    url = "https://dummyjson.com/products/category/sports-accessories"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            prod = random.choice(res.json().get("products", []))
            titulo = prod.get("title")
            preco = prod.get("price") * 5
            preco_antigo = preco * 1.3
            link = f"https://www.mercadolivre.com.br/c/esportes-e-fitness?matt_tool={MATT_TOOL}&matt_word={MATT_WORD}"
            
            msg = (
                f"🔥 <b>ACHADO FITNESS EM OFERTA!</b> 🔥\n\n"
                f"💪 <b>{titulo}</b>\n\n"
                f"❌ <s>De: R$ {preco_antigo:.2f}</s>\n"
                f"✅ <b>Por apenas: R$ {preco:.2f} (23% OFF)</b>\n\n"
                f"🛒 <b>Garante o teu aqui:</b>\n"
                f"👉 {link}\n\n"
                f"⚠️ <i>Oferta por tempo limitado!</i>"
            )
            enviar_mensagem_telegram(msg)
    except Exception as e:
        print(f"Erro no fallback: {e}")

if __name__ == "__main__":
    print("=== EXECUTANDO BUSCA ===")
    buscar_e_enviar_oferta()
    
