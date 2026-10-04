import os
import requests
import urllib.parse

# ==========================================
# CONFIGURAÇÕES E CREDENCIAIS
# ==========================================
CLIENT_ID = "3834562383694739"
CLIENT_SECRET = "56kIUp6iddFIgljrB8vyT2oEmPcSOLQ1"
REDIRECT_URI = "https://www.google.com"
SITE_ID = "MLB"  # Mercado Livre Brasil

# ==========================================
# FUNÇÕES DE AUTENTICAÇÃO (OAUTH 2.0)
# ==========================================
def gerar_url_autorizacao():
    """Gera o link onde deves entrar no navegador para autorizar a aplicação."""
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI
    }
    url_base = "https://auth.mercadolivre.com.br/authorization"
    return f"{url_base}?{urllib.parse.urlencode(params)}"

def obter_tokens(code):
    """Troca o código 'code' obtido na URL após autorização pelos tokens de acesso."""
    url = "https://api.mercadolibre.com/oauth/token"
    payload = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded'
    }
    
    resposta = requests.post(url, data=payload, headers=headers)
    if resposta.status_code == 200:
        return resposta.json()
    else:
        print("Erro ao obter tokens:", resposta.text)
        return None

# ==========================================
# FUNÇÃO PARA BUSCAR OFERTAS / PRODUTOS
# ==========================================
def buscar_ofertas_fitness(termo="suplementos fitness", limite=5):
    """Realiza a busca de produtos/ofertas na API do Mercado Livre."""
    url = f"https://api.mercadolibre.com/sites/{SITE_ID}/search"
    params = {
        "q": termo,
        "limit": limite
    }
    
    resposta = requests.get(url, params=params)
    if resposta.status_code == 200:
        dados = resposta.json()
        resultados = dados.get("results", [])
        
        print(f"\n--- OFERTAS ENCONTRADAS PARA: '{termo}' ---")
        for item in resultados:
            titulo = item.get("title")
            preco = item.get("price")
            link = item.get("permalink")
            print(f"• {titulo}")
            print(f"  Preço: R$ {preco}")
            print(f"  Link: {link}\n")
    else:
        print("Erro ao realizar busca:", resposta.text)

# ==========================================
# EXECUÇÃO PRINCIPAL
# ==========================================
if __name__ == "__main__":
    print("=== BOT OFERTAS FITNESS ===")
    
    # 1. Verifica autorização
    print("\nPasso 1: Abre o link abaixo no navegador para autorizar:")
    print(gerar_url_autorizacao())
    print("\nApós clicar em 'Autorizar', serás redirecionado para o Google.")
    
    # 2. Recebe o código do utilizador
    code_url = input("\nCola aqui a URL completa para onde foste redirecionado (ou apenas o valor após 'code='): ").strip()
    
    # Extrai o código da URL se o utilizador colou a URL inteira
    if "code=" in code_url:
        code = code_url.split("code=")[1].split("&")[0]
    else:
        code = code_url
        
    # 3. Troca o código pelo token
    print("\nA autenticar aplicação...")
    tokens = obter_tokens(code)
    
    if tokens:
        print("\n✅ Autenticação realizada com sucesso!")
        print(f"Access Token: {tokens.get('access_token')[:15]}...")
        
        # 4. Executa a busca de ofertas
        print("\nA procurar produtos...")
        buscar_ofertas_fitness(termo="creatina fitness", limite=5)
    else:
        print("\n❌ Falha na autenticação. Verifica se o código colado está correto e tenta novamente.")
        
