import os
import time
import random
import requests

# ==========================================
# CONFIGURAÇÕES DO TELEGRAM E AFILIADO
# ==========================================
TELEGRAM_BOT_TOKEN = "8619062228:AAGGoyimr33jeAgqM8ds7qBLKHxgm6-5rmQ"
TELEGRAM_CHAT_ID = "-1003941863470"

# Parâmetros do perfil de Afiliado Mercado Livre
MATT_TOOL = "41514834"
MATT_WORD = "cleiton2001js"

# Tempo de espera entre cada envio (em segundos).Ex: 3600 = 1 hora
INTERVALO_SEGUNDOS = 3600 

TERMOS_SUPLEMENTOS = [
    "creatina", "whey protein", "hipercalorico", 
    "barra proteica", "pre treino", "bcaa", "glutamina", 
    "whey isolado", "pasta amendoim"
]

TERMOS_ROUPAS = [
    "camisa dry fit masculina", "top academia feminino", 
    "bermuda treino", "legging academia", 
    "luva academia", "garrafa agua fitness"
]

TERMOS_EQUIPAMENTOS = [
    "kit mini band", "colchonete academia", 
    "par halteres", "corda pular", "barra porta exercicios"
]

def escolher_termo_busca():
    """Proporção: ~75% suplementos, ~15% roupas, ~10% equipamentos."""
    sorteio = random.randint(1, 100)
    if sorteio <= 75:
        return random.choice(TERMOS_SUPLEMENTOS)
    elif sorteio <= 90:
        return random.choice(TERMOS_ROUPAS)
    else:
        return random.choice(TERMOS_EQUIPAMENTOS)

def enviar_mensagem_telegram(texto):
    """Envia mensagem formatada para o Telegram."""
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
        print(f"Erro Telegram: {e}")
        return False

def buscar_e_enviar_oferta():
    """Busca os produtos via API MLB e envia a mensagem com o link de afiliado."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    for tentativa in range(5):
        termo = escolher_termo_busca()
        url = "https://api.mercadolibre.com/sites/MLB/search"
        params = {"q": termo, "limit": 20}
        
        try:
            resposta = requests.get(url, params=params, headers=headers, timeout=10)
            if resposta.status_code == 200:
                dados = resposta.json()
                resultados = dados.get("results", [])
                
                itens_validos = [
                    item for item in resultados 
                    if item.get("permalink") and item.get("price")
                ]
                
                if itens_validos:
                    item = random.choice(itens_validos)
                    
                    titulo = item.get("title")
                    preco_atual = float(item.get("price", 0))
                    preco_original = float(item.get("original_price") or 0)
                    
                    if preco_original > preco_atual:
                        desconto_pct = int(((preco_original - preco_atual) / preco_original) * 100)
                    else:
                        preco_original = preco_atual * 1.25
                        desconto_pct = 20

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
                    
                    print(f"Sucesso na busca [{termo}]: {titulo}")
                    if enviar_mensagem_telegram(mensagem):
                        return True
        except Exception as e:
            print(f"Tentativa {tentativa+1} falhou: {e}")
            
    print("Não foi possível obter produtos nesta execução.")
    return False

if __name__ == "__main__":
    print("=== INICIANDO BOT DE OFERTAS ===")
    while True:
        buscar_e_enviar_oferta()
        print(f"Aguardando {INTERVALO_SEGUNDOS} segundos para a próxima postagem...")
        time.sleep(INTERVALO_SEGUNDOS)
        
