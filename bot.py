import os
import html
import logging
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from urllib.parse import urlparse

import requests


OFERTAS = [
    {
        "titulo": "Whey concentrado Growth Supplements Chocolate 1 kg",
        "preco": "249.90",
        "preco_original": "299.90",
        "link": "https://meli.la/1tBvC7K",
        "validade": "2026-10-04T18:00:00-03:00",
    },
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


def validar_link(link
