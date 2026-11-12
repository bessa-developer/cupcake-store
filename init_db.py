from app import create_app
from app.extensions import db
from app.models import Produto

# Cupcakes de exemplo usados quando o catalogo ainda esta vazio.
CUPCAKES_EXEMPLO = [
    {
        "nome": "Chocolate belga",
        "descricao": "Massa de cacau com cobertura de chocolate meio amargo.",
        "preco": 9.50,
    },
    {
        "nome": "Red velvet",
        "descricao": "Massa aveludada com cream cheese por cima.",
        "preco": 11.00,
    },
    {
        "nome": "Limao siciliano",
        "descricao": "Massa amanteigada com recheio de limao e merengue.",
        "preco": 10.00,
    },
    {
        "nome": "Morango",
        "descricao": "Baunilha com pedacos de morango e chantilly.",
        "preco": 10.50,
    },
    {
        "nome": "Doce de leite",
        "descricao": "Massa de baunilha recheada com doce de leite.",
        "preco": 9.00,
    },
]


def semear_cupcakes():
    # So insere os exemplos se a tabela ainda nao tem produtos, para rodar
    # o script de novo nao duplicar linhas.
    if Produto.query.count() > 0:
        return
    for dados in CUPCAKES_EXEMPLO:
        db.session.add(Produto(disponivel=True, **dados))
    db.session.commit()


def main():
    app = create_app()
    with app.app_context():
        # Cria as tabelas a partir dos models e popula o catalogo de exemplo.
        db.create_all()
        semear_cupcakes()
        print("Banco pronto. Produtos cadastrados:", Produto.query.count())


if __name__ == "__main__":
    main()
