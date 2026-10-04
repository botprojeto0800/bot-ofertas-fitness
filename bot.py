import os
import time
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

# Tempo entre postagens (em segundos). Exemplo: 3600 = 1 hora
INTERVALO_POSTAGEM = 3600 

TERMOS_SUPLEMENTOS = [
    "creatina growth", "whey protein concentrado", "hipercalorico", 
    "barra de proteina", "pre treino", "bcaa", "glutamina", 
    "whey isolado", "pasta de amendoim"
]

TERMOS_ROUPAS = [
    "camisa dry fit masculina treino", "top academia feminino", 
    "bermuda treino academia", "legging academia feminina", 
    "luva para academia treino", "garrafa de agua squeezes fitness"
]

TERMOS_EQUIPAMENTOS = [
    "elastico exercicio kit band", "colchonete academia", 
    "par de halteres", "corda de pular profissional", "barra de porta exercicios"
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
    """Envia mensagem para o canal do Telegram usando HTML."""
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
    """Busca produtos e envia a oferta diretamente."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for tentativa in range(5):
        termo = escolher_termo_busca()
        url = "https://api.mercadolibre.com/sites/MLB/search"
        params = {"q": termo, "limit": 15}
        
        try:
            resposta = requests.get(url, params=params, headers=headers, timeout=10)
            if resposta.status_code == 200:
                dados = resposta.json()
                resultados = dados.get("results", [])
                
                if resultados:
                    item = random.choice(resultados)
                    
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
                    
                    print(f"Enviando oferta [{termo}]: {titulo}")
                    if enviar_mensagem_telegram(mensagem):
                        return True
        except Exception as e:
            print(f"Tentativa {tentativa+1} falhou: {e}")
            
    print("Não foi possível enviar uma oferta nesta tentativa.")
    return False

if __name__ == "__main__":
    print("=== INICIANDO BOT DE OFERTAS CONTINUO ===")
    while True:
        buscar_e_enviar_oferta()
        print(f"Aguardando {INTERVALO_POSTAGEM} segundos para a próxima postagem...")
        time.sleep(INTERVALO_POSTAGEM)
        
