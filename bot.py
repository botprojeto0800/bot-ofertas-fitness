import os
import html
import logging
from decimal import Decimal, InvalidOperation
from urllib.parse import urlparse

import requests


# Cadastre produtos e links gerados na Central de Afiliados.
# Os valores abaixo são apenas um exemplo comentado.
OFERTAS = [
    # {
    #     "titulo": "Nome real do produto",
    #     "preco": "72.90",
    #     "preco_original": None,
    #     "link": "https://meli.la/SEU_LINK",
    #     "validade": "2026-10-05T23:59:00-03:00",
    # },
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def converter_preco(valor):
    if valor is None:
        return None

    try:
        numero = Decimal(str(valor))
    except (InvalidOperation, ValueError):
        return None

    if not numero.is_finite() or numero <= 0:
        return None

    return numero


def formatar_preco(numero):
    return (
        f"{numero:,.2f}"
        .replace(",", "_")
        .replace(".", ",")
        .replace("_", ".")
    )


def validar_link(link):
    if not isinstance(link, str):
        return False

    endereco = urlparse(link)
    dominio = endereco.hostname or ""

    return (
        endereco.scheme == "https"
        and not endereco.username
        and not endereco.password
        and (
            dominio == "meli.la"
            or dominio == "mercadolivre.com.br"
            or dominio.endswith(".mercadolivre.com.br")
        )
    )


def montar_mensagem(oferta):
    titulo = str(oferta.get("titulo", "")).strip()
    preco = converter_preco(oferta.get("preco"))
    original = converter_preco(oferta.get("preco_original"))
    link = oferta.get("link")

    if not titulo or len(titulo) > 400:
        raise ValueError("Título ausente ou muito longo.")

    if preco is None:
        raise ValueError("Preço inválido.")

    if not validar_link(link):
        raise ValueError("Link inválido. Use o link oficial de afiliado.")

    linhas = [
        "🔥 <b>ACHADO FITNESS</b>",
        "",
        f"💪 <b>{html.escape(titulo)}</b>",
        "",
    ]

    if original is not None and original > preco:
        desconto = int((original - preco) / original * 100)

        linhas.extend([
            f"❌ <s>De: R$ {formatar_preco(original)}</s>",
            f"✅ <b>Por: R$ {formatar_preco(preco)} "
            f"({desconto}% OFF)</b>",
        ])
    else:
        linhas.append(
            f"✅ <b>Preço consultado: R$ {formatar_preco(preco)}</b>"
        )

    link_seguro = html.escape(link, quote=True)

    linhas.extend([
        "",
        f'🛒 <a href="{link_seguro}">Ver no Mercado Livre</a>',
        "",
        "Publicidade • link de afiliado.",
        "⚠️ Preço e disponibilidade podem mudar. Confira no anúncio.",
    ])

    return "\n".join(linhas)


def enviar_telegram(texto, token, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": texto,
        "parse_mode": "HTML",
        "link_preview_options": {
            "is_disabled": False,
        },
    }

    try:
        resposta = requests.post(
            url,
            json=payload,
            timeout=(5, 20),
        )
    except requests.RequestException:
        # Não imprimir a exceção: pode conter o token na URL.
        logging.error(
            "Falha de rede. O envio pode ter ocorrido; "
            "confira o canal antes de tentar novamente."
        )
        return False

    try:
        dados = resposta.json()
    except ValueError:
        logging.error(
            "Resposta inválida do Telegram. Confira o canal."
        )
        return False

    if (
        resposta.status_code == 200
        and isinstance(dados, dict)
        and dados.get("ok") is True
    ):
        logging.info("Mensagem enviada com sucesso.")
        return True

    codigo = (
        dados.get("error_code", resposta.status_code)
        if isinstance(dados, dict)
        else resposta.status_code
    )

    motivos = {
        400: "Confira o ID do canal e a mensagem.",
        401: "Token inválido ou revogado.",
        403: "Confira a permissão do bot para publicar no canal.",
        429: "Limite de envio atingido. Aguarde.",
    }

    logging.error(
        "Telegram erro %s. %s",
        codigo,
        motivos.get(codigo, "Envio não confirmado."),
    )
    return False


def main():
    from datetime import datetime, timezone

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()

    if not token or not chat_id:
        logging.error(
            "Configure TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID "
            "no Environment do Render."
        )
        return 1

    agora = datetime.now(timezone.utc)
    validas = []

    for numero, oferta in enumerate(OFERTAS, start=1):
        try:
            validade = datetime.fromisoformat(
                oferta["validade"].replace("Z", "+00:00")
            )

            if validade.tzinfo is None:
                raise ValueError("A validade precisa incluir o fuso.")

            texto = montar_mensagem(oferta)

            if validade > agora:
                validas.append(texto)

        except (ValueError, KeyError, TypeError):
            logging.error(
                "Oferta %s inválida. Confira seus campos.",
                numero,
            )

    if not validas:
        logging.info("Nenhuma oferta válida cadastrada.")
        return 0

    # Alterna as ofertas por hora, sem depender de arquivo local.
    # Produtos podem repetir em horas posteriores.
    indice = int(agora.timestamp() // 3600) % len(validas)

    return 0 if enviar_telegram(validas[indice], token, chat_id) else 1


if __name__ == "__main__":
    raise SystemExit(main())
