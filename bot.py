import requests

TOKEN = "8619062228:AAGoyimr33jeAqqM8ds7qBLKHXgm6-5rmQ"
ID_DO_CHAT = "@ofertasfitness0800"

def buscar_e_postar_oferta():
    # API pública de ofertas e buscas do Mercado Livre Brasil
    url = "https://api.mercadolibre.com/sites/MLB/search?q=suplementos&limit=50"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        res = requests.get(url, headers=headers).json()
        resultados = res.get("results", [])
        
        print(f"Total de itens retornados pela API: {len(resultados)}")

        for item in resultados:
            nome = item.get("title", "")
            preco_atual = item.get("price")
            preco_original = item.get("original_price")
            link = item.get("permalink")

            # Se houver preço antigo e for maior que o atual
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

            # Se não houver preço original preenchido na API, envia o produto direto
            elif preco_atual and link:
                preco_por = f"{preco_atual:.2f}".replace('.', ',')

                texto = f"⚡ <b>DESTAQUE FITNESS</b> ⚡\n\n" \
                        f"<b>{nome}</b>\n\n" \
                        f"💰 Preço especial: <b>R$ {preco_por}</b>\n\n" \
                        f"🛒 Confira no Mercado Livre:\n" \
                        f"{link}\n\n" \
                        f"⚠️ <i>Aproveite enquanto durar o estoque!</i>"

                enviar_telegram(texto, nome, "Preço Especial")
                return

    except Exception as e:
        print(f"Erro na requisição: {e}")

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
