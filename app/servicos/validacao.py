import re
from decimal import Decimal, InvalidOperation

# Regras de validação usadas pelos controllers antes de gravar no banco.
# Os limites de tamanho acompanham as colunas definidas nos models.

PRECO_MAXIMO = Decimal("9999.99")

_FORMATO_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_FORMATO_CEP = re.compile(r"^\d{5}-?\d{3}$")


def texto_ate(valor, limite):
    # Confere se o texto preenchido cabe na coluna do banco.
    return len(valor) <= limite


def email_valido(email):
    return texto_ate(email, 120) and bool(_FORMATO_EMAIL.match(email))


def cep_valido(cep):
    # Aceita 00000000 ou 00000-000.
    return bool(_FORMATO_CEP.match(cep))


def imagem_valida(url):
    # A imagem é opcional. Quando vier, precisa ser um link http ou https.
    if not url:
        return True
    return texto_ate(url, 255) and url.startswith(("http://", "https://"))


def preco_valido(texto):
    # Converte o preço digitado. Devolve None para texto inválido, infinito,
    # NaN, zero, negativo ou acima do que a coluna Numeric(10, 2) comporta.
    try:
        preco = Decimal((texto or "").replace(",", "."))
    except InvalidOperation:
        return None
    if not preco.is_finite() or preco <= 0 or preco > PRECO_MAXIMO:
        return None
    return preco.quantize(Decimal("0.01"))
