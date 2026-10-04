import requests
import time

TOKEN = "8619062228:AAGGoyimr33jeAgqM8ds7qBLKHxgm6-5rmQ"
CHAT_ID = "@ofertasfitness0800"

# Categorias no Mercado Livre (MLB1227 = Suplementos / MLB1430 = Calçados e Roupas)
CATEGORIAS = [
    {"id": "MLB1227", "nome": "Suplementos"},
    {"id": "MLB1430", "nome": "Calçados/Roupas"}
]

TERMOS_SUPLEMENTOS = ["whey", "creatina", "hipercalorico", "barra proteica", "pre treino", "bcaa", "glutamina"]
TERMOS_VESTUARIO = ["tenis", "camiseta", "legging", "top", "bermuda", "shorts"]

def buscar_e_postar_oferta():
    for cat in CATEGORIAS:
        url_busca = f"https://api.mercadolibre.com/sites/MLB/search?category={cat['id']}&sort=relevance"
        res = requests.get(url_busca).json()
        
        for item in res.get("results", [])[:15]:
            preco_original = item.get("original_price")
            preco_atual = item.get("price")
            nome = item.get("title", "")
            nome_lc = nome.lower()
            
            # Validação de Categoria
            e_suplemento = any(termo in nome_lc for termo in TERMOS_SUPLEMENTOS)
            e_vestuario = any(termo in nome_lc for termo in TERMOS_VESTUARIO)
            
            if preco_original and preco_atual and (e_suplemento or e_vestuario):
                desconto = round(((preco_original - preco_atual) / preco_original) * 100)
                
                # Regra de Desconto: Apenas 10% a 50%
                if 10 <= desconto <= 50:
                    link = item.get("permalink")
                    preco_de = f"{preco_original:.2f}".replace('.', ',')
                    preco_por = f"{preco_atual:.2f}".replace('.', ',')
                    
                    categoria_txt = "💪 <b>ACHADO EM SUPLEMENTOS!</b>" if e_suplemento else "👟 <b>ACHADO FITNESS!</b>"
                    
                    texto = f"""🔥 {categoria_txt} 🔥

📦 <b>{nome}</b>

❌ De: <s>R$ {preco_de}</s>
✅ <b>Por apenas: R$ {preco_por}</b> ({desconto}% OFF)

🛒 <b>Garante o teu aqui:</b>
👉 {link}

⚠️ <i>Oferta por tempo limitado!</i>"""

                    payload = {
                        "chat_id": CHAT_ID,
                        "text": texto,
                        "parse_mode": "HTML",
                        "link_preview_options": {"prefer_small_media": True}
                    }
                    
                    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json=payload)
                    print(f"✅ Postado com sucesso: {nome} ({desconto}% OFF)")
                    return

# Loop automático a cada 2 horas
while True:
    print("🔎 Procurando novas ofertas...")
    buscar_e_postar_oferta()
    time.sleep(7200)
  
