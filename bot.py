import requests

TOKEN = "8619062228:AAGoyimr33jeAqqM8ds7qBLKHXgm6-5rmQ"
ID_DO_CHAT = "@ofertasfitness0800"

TERMOS_BUSCA = [
    "creatina", 
    "whey protein", 
    "suplementos", 
    "tenis masculino fitness", 
    "tenis feminino corrida", 
    "camisa drifit", 
    "short academia", 
    "pre treino"
]

def buscar_e_postar_oferta():
    for termo in TERMOS_BUSCA:
        url_busca = f"https://api.mercadolibre.com/sites/MLB/search?q={termo}&limit=50"
        try:
            res = requests.get(url_busca).json()
        except Exception as e:
            print(f"Erro ao buscar termo '{termo}': {e}")
            continue

        for item in res.get("results", []):
            preco_original = item.get("original_price")
            preco_atual = item.get("price")
            nome = item.get("title", "")
            link = item.get("permalink")

            # Caso 1: Tem preço original e desconto entre 10% e 65%
            if preco_original and preco_atual and preco_original > preco_atual:
                desconto = round(((preco_original - preco_atual) / preco_original) * 100)
                if 10 <= desconto <= 65:
                    preco_de = f"{preco_original:.2f}".replace('.', ',')
                    preco_por = f"{preco_atual:.2f}".replace('.', ',')

                    texto = f"🔥 <b>OFERTA IMPERDÍVEL</b> 🔥\n\n" \
                            f"<b>{nome}</b>\n\n" \
                            f"❌ De: ~R$ {preco_de}~\n" \
                            f"✅ Por apenas: <b>R$ {preco_por}</b> ({desconto}% OFF)\n\n" \
                            f"🛒 Garanta o seu aqui:\n" \
                            f"{link}\n\n" \
                            f"⚠️ <i>Oferta por tempo limitado!</i>"

                    enviar_telegram(texto, nome, f"{desconto}% OFF")
                    return

            # Caso 2: Se não houver desconto calculado mas for um produto válido com bom preço
            elif preco_atual:
                preco_por = f"{preco_atual:.2f}".replace('.', ',')

                texto = f"⚡ <b>DESTAQUE FITNESS</b> ⚡\n\n" \
                        f"<b>{nome}</b>\n\n" \
                        f"💰 Preço especial: <b>R$ {preco_por}</b>\n\n" \
                        f"🛒 Confira no Mercado Livre:\n" \
                        f"{link}\n\n" \
                        f"⚠️ <i>Aproveite enquanto durar o estoque!</i>"

                enviar_telegram(texto, nome, "Preço Especial")
                return

    print("Nenhum produto encontrado nesta execução.")

def enviar_telegram(texto, nome, status_desconto):
    payload = {
        "chat_id": ID_DO_CHAT,
        "text": texto,
        "parse_mode": "HTML",
        "link_preview_options": {"is_disabled": False}
    }
    resposta = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json=payload)
    print(f"Resultado Telegram: {resposta.status_code} - {resposta.text}")
    print(f"Postado com sucesso: {nome} ({status_desconto})")

buscar_e_postar_oferta()
