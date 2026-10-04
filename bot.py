import requests

TOKEN = "8619062228:AAGoyimr33jeAqqM8ds7qBLKHXgm6-5rmQ"
ID_DO_CHAT = "@ofertasfitness0800"

# Termos diretos de busca no Mercado Livre
TERMOS_BUSCA = ["suplementos", "tenis fitness", "roupa academia", "creatina", "whey protein"]

def buscar_e_postar_oferta():
    for termo in TERMOS_BUSCA:
        url_busca = f"https://api.mercadolibre.com/sites/MLB/search?q={termo}&sort=relevance"
        res = requests.get(url_busca).json()

        for item in res.get("results", [])[:15]:
            preco_original = item.get("original_price")
            preco_atual = item.get("price")
            nome = item.get("title", "")

            # Se houver preço original e preço atual, calcula o desconto
            if preco_original and preco_atual and preco_original > preco_atual:
                desconto = round(((preco_original - preco_atual) / preco_original) * 100)

                # Regra de Desconto: Apenas de 10% a 65%
                if 10 <= desconto <= 65:
                    link = item.get("permalink")
                    preco_de = f"{preco_original:.2f}".replace('.', ',')
                    preco_por = f"{preco_atual:.2f}".replace('.', ',')

                    texto = f"🔥 <b>OFERTA IMPERDÍVEL</b> 🔥\n\n" \
                            f"<b>{nome}</b>\n\n" \
                            f"❌ De: ~R$ {preco_de}~\n" \
                            f"✅ Por apenas: <b>R$ {preco_por}</b> ({desconto}% OFF)\n\n" \
                            f"🛒 Garanta o seu aqui:\n" \
                            f"{link}\n\n" \
                            f"⚠️ <i>Oferta por tempo limitado!</i>"

                    payload = {
                        "chat_id": ID_DO_CHAT,
                        "text": texto,
                        "parse_mode": "HTML",
                        "link_preview_options": {"is_disabled": False}
                    }

                    resposta = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json=payload)
                    print(f"Resultado do envio: {resposta.status_code} - {resposta.text}")
                    print(f"Postado com sucesso: {nome} ({desconto}% OFF)")
                    return

    print("Nenhuma oferta encontrada nesta execução.")

buscar_e_postar_oferta()
