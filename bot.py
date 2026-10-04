import requests

TOKEN = "8619062228:AAGoyimr33jeAqqM8ds7qBLKHXgm6-5rmQ"
ID_DO_CHAT = "@ofertasfitness0800"

def buscar_e_postar_oferta():
    # Categoria de Suplementos / Esportes e Fitness
    url = "https://api.mercadolibre.com/sites/MLB/search?category=MLB1276&limit=50"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    try:
        response = requests.get(url, headers=headers)
        res = response.json()
        resultados = res.get("results", [])
        
        print(f"Status da API: {response.status_code}")
        print(f"Total de itens retornados: {len(resultados)}")

        for item in resultados:
            nome = item.get("title", "")
            preco_atual = item.get("price")
            preco_original = item.get("original_price")
            link = item.get("permalink")

            # Se houver preço original com desconto entre 10% e 65%
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

            # Caso não tenha o campo original_price, envia como Destaque
            elif preco_atual and link:
                preco_por = f"{preco_atual:.2f}".replace('.', ',')

                texto = f"⚡ <b>DESTAQUE FITNESS</b> ⚡\n\n" \
                        f"<b>{nome}</b>\n\n" \
                        f"💰 Preço especial: <b>R$ {preco_por}</b>\n\n" \
                        f"🛒 Confira no Mercado Livre:\n" \
                        f"{link}\n\n" \
                        f"⚠️ <i>Aproveite enquanto durar o estoque!</i>"

                enviar_telegram(texto, nome, "Destaque")
                return

    except Exception as e:
        print(f"Erro ao consultar a API: {e}")

    print("Nenhum produto encontrado nesta execução.")

def enviar_telegram(texto, nome, status):
    payload = {
        "chat_id": ID_DO_CHAT,
        "text": texto,
        "parse_mode": "HTML",
        "link_preview_options": {"is_disabled": False}
    }
    resposta = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json=payload)
    print(f"Resultado Telegram: {resposta.status_code} - {resposta.text}")
    print(f"Postado com sucesso: {nome} ({status})")

buscar_e_postar_oferta()
