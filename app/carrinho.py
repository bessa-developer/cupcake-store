from decimal import Decimal

from flask import session

from app.extensions import db
from app.models import Produto

CHAVE = "carrinho"


def _obter():
    # O carrinho vive na sessao como um dicionario de produto_id para quantidade.
    return session.get(CHAVE, {})


def _salvar(carrinho):
    session[CHAVE] = carrinho
    session.modified = True


def adicionar(produto_id, quantidade=1):
    carrinho = _obter()
    chave = str(produto_id)
    carrinho[chave] = carrinho.get(chave, 0) + quantidade
    if carrinho[chave] < 1:
        carrinho.pop(chave, None)
    _salvar(carrinho)


def atualizar(produto_id, quantidade):
    # Define a quantidade exata de um item; zero ou menos remove o item.
    carrinho = _obter()
    chave = str(produto_id)
    if quantidade < 1:
        carrinho.pop(chave, None)
    else:
        carrinho[chave] = quantidade
    _salvar(carrinho)


def remover(produto_id):
    carrinho = _obter()
    carrinho.pop(str(produto_id), None)
    _salvar(carrinho)


def limpar():
    session.pop(CHAVE, None)


def itens_detalhados():
    # Monta a lista de itens com o produto, o subtotal e o total geral,
    # buscando os produtos atuais no banco.
    carrinho = _obter()
    itens = []
    total = Decimal("0")
    for produto_id, quantidade in carrinho.items():
        produto = db.session.get(Produto, int(produto_id))
        if produto is None:
            continue
        subtotal = produto.preco * quantidade
        total += subtotal
        itens.append({"produto": produto, "quantidade": quantidade, "subtotal": subtotal})
    return itens, total


def itens_disponiveis():
    # Separa os itens do carrinho em disponiveis e indisponiveis, usada no
    # checkout para nao fechar pedido com cupcake que saiu de linha.
    itens, _ = itens_detalhados()
    disponiveis = [item for item in itens if item["produto"].disponivel]
    indisponiveis = [item for item in itens if not item["produto"].disponivel]
    return disponiveis, indisponiveis
