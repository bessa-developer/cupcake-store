import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models import Usuario, Produto
from config import TestConfig


@pytest.fixture
def app():
    # Cria a aplicacao de teste e monta um banco limpo em memoria.
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def produto(app):
    # Um produto disponivel para os testes de catalogo e carrinho.
    p = Produto(nome="Baunilha", descricao="Classico", preco=8.00, disponivel=True)
    db.session.add(p)
    db.session.commit()
    return p


@pytest.fixture
def usuario(app):
    u = Usuario(
        nome="Cliente",
        email="cliente@exemplo.com",
        senha_hash=generate_password_hash("senha123"),
    )
    db.session.add(u)
    db.session.commit()
    return u


@pytest.fixture
def admin(app):
    u = Usuario(
        nome="Gestor",
        email="admin@exemplo.com",
        senha_hash=generate_password_hash("admin123"),
        is_admin=True,
    )
    db.session.add(u)
    db.session.commit()
    return u


@pytest.fixture
def login(client):
    # Atalho para autenticar nos testes.
    def _login(email, senha):
        return client.post(
            "/login",
            data={"email": email, "senha": senha},
            follow_redirects=True,
        )

    return _login
