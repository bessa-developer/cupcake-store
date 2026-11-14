from sqlalchemy import text

from app import create_app
from app.extensions import db

# Colunas novas da tabela de pedidos, adicionadas para as etapas de entrega
# e pagamento. O ALTER é idempotente, então rodar de novo não causa erro.
COLUNAS = [
    ("destinatario", "VARCHAR(120)"),
    ("endereco", "VARCHAR(200)"),
    ("numero", "VARCHAR(20)"),
    ("bairro", "VARCHAR(80)"),
    ("cidade", "VARCHAR(80)"),
    ("cep", "VARCHAR(15)"),
    ("observacao", "TEXT"),
    ("forma_pagamento", "VARCHAR(20)"),
]


def main():
    app = create_app()
    with app.app_context():
        for nome, tipo in COLUNAS:
            db.session.execute(
                text(f"ALTER TABLE pedidos ADD COLUMN IF NOT EXISTS {nome} {tipo}")
            )
        db.session.commit()
        print("Migração aplicada. As colunas de entrega e pagamento já existem em pedidos.")


if __name__ == "__main__":
    main()
