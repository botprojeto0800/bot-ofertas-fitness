import requests
import time

TOKEN = "8619062228:AAGoyimr33jeAqqM8ds7qBLKHXgm6-5rmQ"
ID_DO_CHAT = "@ofertasfitness0800"

# Categorias no Mercado Livre (MLB1227 = Suplementos / MLB1430 = Calçados e Roupas)
CATEGORIAS = [
    {"categoria_id": "MLB1227", "nome": "Suplementos"},
    {"categoria_id": "MLB1430", "nome": "Calçados/Roupas"}
]

TERMOS_SUPLEMENTOS = ["soro", "creatina", "hipercalórico", "barra proteica", "pré-treino", "bcaa", "glutamina"]
TERMOS_VESTUARIO = ["tênis", "camiseta", "legging", "regata", "bermuda", "shorts"]

def buscar_e_postar_oferta():
    for cat in CATEGORIAS:
        url_busca = f"https://api.mercadolibre.com/sites/MLB/search?category={cat['categoria_id']}&sort=relevance"
        res = requests.get(url_busca).json()

        for item in res.get("results", [])[:15]:
            preco_original = item.get("original_price")
            preco_atual = item.get("price")
            nome = item.get("title", "")
            nome_lc = nome.lower()

            # Validação de Categoria
            suplemento = any(termo in nome_lc for termo in TERMOS_SUPLEMENTOS)
            e_vestuario = any(termo in nome_lc for termo in TERMOS_VESTUARIO)

            if preco_original and preco_atual and (suplemento or e_vestuario):
                desconto = round(((preco_original - preco_atual) / preco_original) * 100)

                # Regra de Desconto: Apenas 10% a 50%
                if desconto >= 0:
                                    
                    link = item.get("permalink")
                    preco_de = f"{preco_original:.2f}".replace('.', ',')
                    preco_por = f"{preco_atual:.2f}".replace('.', ',')

                    pagina_txt = "ACHADO EM SUPLEMENTOS" if suplemento else "ACHADO EM VESTUÁRIO"

                    texto = f"🔥 <b>{pagina_txt}</b> 🔥\n\n" \
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

                    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json=payload)
                    print(f"Postado com sucesso: {nome} ({desconto}% OFF)")
                    return

# Executa uma única vez para o Cron Job do Render
buscar_e_postar_oferta()
