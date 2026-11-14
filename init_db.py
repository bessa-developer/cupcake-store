import sys

from app import create_app
from app.extensions import db
from app.models import Produto, ItemPedido

SUFIXO_FOTO = "?auto=format&fit=crop&w=800&q=80"


def _foto(id_unsplash, recorte=""):
    # O recorte opcional usa os parâmetros do Unsplash para enquadrar melhor
    # fotos em que o cupcake fica fora do centro.
    return f"https://images.unsplash.com/{id_unsplash}{SUFIXO_FOTO}{recorte}"


# Catálogo de exemplo da loja, cada cupcake com a sua própria foto.
CUPCAKES_EXEMPLO = [
    {
        "nome": "Chocolate belga",
        "descricao": "Massa de cacau com cobertura de chocolate meio amargo.",
        "preco": 9.50,
        "imagem": _foto("photo-1640806353257-6c408529d822"),
    },
    {
        "nome": "Red velvet",
        "descricao": "Massa aveludada com cobertura de cream cheese.",
        "preco": 11.00,
        "imagem": _foto("photo-1614707267537-b85aaf00c4b7"),
    },
    {
        "nome": "Limão siciliano",
        "descricao": "Massa amanteigada com recheio de limão e merengue.",
        "preco": 10.00,
        "imagem": _foto("photo-1576618148400-f54bed99fcfd"),
    },
    {
        "nome": "Morango",
        "descricao": "Massa de baunilha com pedaços de morango e chantilly.",
        "preco": 10.50,
        "imagem": _foto("photo-1555684655-49a1c6b94dd1"),
    },
    {
        "nome": "Nozes com caramelo",
        "descricao": "Massa de baunilha com cobertura de chantilly, calda de caramelo e nozes.",
        "preco": 9.00,
        "imagem": _foto(
            "photo-1559114819-e881a3086b87",
            "&h=800&crop=focalpoint&fp-y=0.8",
        ),
    },
    {
        "nome": "Baunilha",
        "descricao": "Massa de baunilha com cobertura de buttercream e confeitos.",
        "preco": 8.50,
        "imagem": _foto("photo-1771016833967-3602b9e9a7e1"),
    },
    {
        "nome": "Brigadeiro",
        "descricao": "Massa de chocolate com cobertura de brigadeiro e granulado.",
        "preco": 11.50,
        "imagem": _foto("photo-1448131063153-f1e240f98a72"),
    },
    {
        "nome": "Coco",
        "descricao": "Massa de coco com cobertura de chantilly e coco ralado.",
        "preco": 10.00,
        "imagem": _foto("photo-1583531803919-ca2728fb12e7"),
    },
]


def semear_cupcakes():
    # Só insere os exemplos se a tabela ainda não tem produtos, para que rodar
    # o script de novo não duplique linhas.
    if Produto.query.count() > 0:
        return
    for dados in CUPCAKES_EXEMPLO:
        db.session.add(Produto(disponivel=True, **dados))
    db.session.commit()


def recriar_catalogo():
    # Apaga os produtos atuais e grava o catálogo de exemplo do zero. Só roda
    # quando nenhum pedido aponta para os produtos, para não violar a chave
    # estrangeira de itens_pedido.
    if ItemPedido.query.count() > 0:
        print("Existem pedidos gravados. O catálogo não foi recriado.")
        return False
    Produto.query.delete()
    db.session.commit()
    semear_cupcakes()
    return True


def main():
    app = create_app()
    with app.app_context():
        # Cria as tabelas a partir dos models e popula o catálogo de exemplo.
        db.create_all()
        if "--recriar" in sys.argv:
            recriar_catalogo()
        else:
            semear_cupcakes()
        print("Banco pronto. Produtos cadastrados:", Produto.query.count())


if __name__ == "__main__":
    main()
