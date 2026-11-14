import pytest

from app import create_app
from app.extensions import db
from app.models import Usuario, Produto, Pedido, ItemPedido
from config import TestConfig, CHAVE_DESENVOLVIMENTO


DADOS_ENTREGA = {
    "destinatario": "Fulano de Tal",
    "endereco": "Rua das Flores",
    "numero": "100",
    "bairro": "Centro",
    "cidade": "Belo Horizonte",
    "cep": "30000-000",
}


# Ambiente de produção

def test_producao_exige_secret_key(monkeypatch):
    monkeypatch.setenv("VERCEL", "1")

    class SemChave(TestConfig):
        SECRET_KEY = None

    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        create_app(SemChave)


def test_producao_recusa_chave_de_desenvolvimento(monkeypatch):
    monkeypatch.setenv("VERCEL", "1")

    class ChavePadrao(TestConfig):
        SECRET_KEY = CHAVE_DESENVOLVIMENTO

    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        create_app(ChavePadrao)


def test_producao_liga_cookie_seguro(monkeypatch):
    monkeypatch.setenv("VERCEL", "1")

    class ChaveBoa(TestConfig):
        SECRET_KEY = "uma-chave-longa-e-aleatoria"

    app = create_app(ChaveBoa)
    assert app.config["SESSION_COOKIE_SECURE"] is True


def test_app_nao_sobe_sem_database_url():
    class SemBanco(TestConfig):
        TESTING = False
        SQLALCHEMY_DATABASE_URI = None

    with pytest.raises(RuntimeError, match="DATABASE_URL"):
        create_app(SemBanco)


# Proteção CSRF

def test_post_sem_token_csrf_e_recusado():
    class ComCsrf(TestConfig):
        WTF_CSRF_ENABLED = True

    client = create_app(ComCsrf).test_client()
    client.post("/login", data={"email": "cliente@exemplo.com", "senha": "senha123"})
    with client.session_transaction() as sessao:
        assert "usuario_id" not in sessao
        avisos = [texto for _, texto in sessao.get("_flashes", [])]
    assert "A sessão expirou. Tente novamente." in avisos


# Cadastro

@pytest.mark.parametrize(
    "dados",
    [
        {"nome": "Ana", "email": "email-sem-arroba", "senha": "segredo"},
        {"nome": "Ana", "email": "ana@exemplo.com", "senha": "123"},
        {"nome": "A" * 121, "email": "ana@exemplo.com", "senha": "segredo"},
    ],
    ids=["email-invalido", "senha-curta", "nome-longo"],
)
def test_registro_recusa_dados_invalidos(client, dados):
    resposta = client.post("/registro", data=dados)
    assert resposta.status_code == 200
    assert Usuario.query.count() == 0


# Entrega

@pytest.mark.parametrize(
    "campo, valor",
    [("cep", "123"), ("cep", "abcde-fgh"), ("numero", "1" * 21), ("observacao", "x" * 501)],
)
def test_entrega_recusa_dados_invalidos(client, produto, usuario, login, campo, valor):
    login("cliente@exemplo.com", "senha123")
    client.post(f"/carrinho/adicionar/{produto.id}", data={"quantidade": 1})
    client.post("/pedidos/entrega", data={**DADOS_ENTREGA, campo: valor})
    with client.session_transaction() as sessao:
        assert "entrega" not in sessao


# Admin

@pytest.mark.parametrize("preco", ["nan", "inf", "-1", "0", "abc", "10000"])
def test_admin_recusa_preco_invalido(client, admin, login, preco):
    login("admin@exemplo.com", "admin123")
    client.post("/admin/novo", data={"nome": "Teste", "preco": preco, "disponivel": "on"})
    assert Produto.query.filter_by(nome="Teste").first() is None


def test_admin_recusa_imagem_que_nao_e_link(client, admin, login):
    login("admin@exemplo.com", "admin123")
    client.post(
        "/admin/novo",
        data={"nome": "Teste", "preco": "9,50", "imagem": "javascript:alert(1)"},
    )
    assert Produto.query.filter_by(nome="Teste").first() is None


def test_admin_tira_da_vitrine_produto_com_pedido(client, admin, usuario, produto, login):
    pedido = Pedido(usuario_id=usuario.id)
    pedido.itens.append(ItemPedido(produto_id=produto.id, quantidade=1, preco_unitario=produto.preco))
    db.session.add(pedido)
    db.session.commit()

    login("admin@exemplo.com", "admin123")
    client.post(f"/admin/{produto.id}/remover")

    db.session.refresh(produto)
    assert db.session.get(Produto, produto.id) is not None
    assert produto.disponivel is False


# Carrinho

def test_carrinho_limita_quantidade_ao_adicionar(client, produto):
    client.post(f"/carrinho/adicionar/{produto.id}", data={"quantidade": 60})
    client.post(f"/carrinho/adicionar/{produto.id}", data={"quantidade": 60})
    with client.session_transaction() as sessao:
        assert sessao["carrinho"][str(produto.id)] == 99


def test_carrinho_limita_quantidade_ao_atualizar(client, produto):
    client.post(f"/carrinho/adicionar/{produto.id}", data={"quantidade": 1})
    client.post(f"/carrinho/atualizar/{produto.id}", data={"quantidade": 100000})
    with client.session_transaction() as sessao:
        assert sessao["carrinho"][str(produto.id)] == 99


def test_carrinho_descarta_produto_inexistente_ao_atualizar(client):
    with client.session_transaction() as sessao:
        sessao["carrinho"] = {"999": 1}
    client.post("/carrinho/atualizar/999", data={"quantidade": 3})
    with client.session_transaction() as sessao:
        assert "999" not in sessao["carrinho"]
