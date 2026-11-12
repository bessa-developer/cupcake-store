from app.extensions import db
from app.models import Usuario, Produto, Pedido


def _criar_produto(nome, preco, disponivel=True):
    p = Produto(nome=nome, descricao="", preco=preco, disponivel=disponivel)
    db.session.add(p)
    db.session.commit()
    return p


def _fluxo_pedido(client, forma="pix"):
    # Percorre as etapas de entrega e pagamento ate finalizar o pedido.
    client.post(
        "/pedidos/entrega",
        data={
            "destinatario": "Fulano de Tal",
            "endereco": "Rua das Flores",
            "numero": "100",
            "bairro": "Centro",
            "cidade": "Belo Horizonte",
            "cep": "30000-000",
            "observacao": "",
        },
    )
    return client.post(
        "/pedidos/pagamento",
        data={"forma_pagamento": forma},
        follow_redirects=True,
    )


def test_app_sobe(app):
    assert app is not None


def test_home_redireciona_para_catalogo(client):
    resposta = client.get("/")
    assert resposta.status_code == 302
    assert "/produtos" in resposta.headers["Location"]


def test_catalogo_lista_produto_disponivel(client, produto):
    resposta = client.get("/produtos/")
    assert resposta.status_code == 200
    assert b"Baunilha" in resposta.data


def test_registro_cria_usuario_com_hash(client):
    client.post(
        "/registro",
        data={"nome": "Novo", "email": "novo@exemplo.com", "senha": "segredo"},
    )
    usuario = Usuario.query.filter_by(email="novo@exemplo.com").first()
    assert usuario is not None
    # A senha nunca fica em texto puro no banco.
    assert usuario.senha_hash != "segredo"


def test_login_valido_abre_sessao(client, usuario, login):
    resposta = login("cliente@exemplo.com", "senha123")
    assert resposta.status_code == 200
    with client.session_transaction() as sessao:
        assert sessao.get("usuario_id") == usuario.id


def test_login_invalido_nao_abre_sessao(client, usuario, login):
    login("cliente@exemplo.com", "errada")
    with client.session_transaction() as sessao:
        assert "usuario_id" not in sessao


def test_rota_protegida_sem_login_redireciona(client):
    resposta = client.get("/pedidos/")
    assert resposta.status_code == 302
    assert "/login" in resposta.headers["Location"]


def test_carrinho_soma_itens(client, produto):
    client.post(f"/carrinho/adicionar/{produto.id}", data={"quantidade": 2})
    resposta = client.get("/carrinho/")
    assert resposta.status_code == 200
    assert b"Baunilha" in resposta.data


def test_checkout_gera_pedido_e_limpa_carrinho(client, produto, usuario, login):
    login("cliente@exemplo.com", "senha123")
    client.post(f"/carrinho/adicionar/{produto.id}", data={"quantidade": 3})
    _fluxo_pedido(client, forma="pix")

    pedido = Pedido.query.filter_by(usuario_id=usuario.id).first()
    assert pedido is not None
    assert pedido.status == "confirmado"
    assert pedido.forma_pagamento == "pix"
    assert pedido.cidade == "Belo Horizonte"
    assert len(pedido.itens) == 1
    assert pedido.itens[0].quantidade == 3
    # O preco do item guarda o valor do momento da compra.
    assert pedido.itens[0].preco_unitario == produto.preco
    with client.session_transaction() as sessao:
        assert "carrinho" not in sessao
        assert "entrega" not in sessao


def test_admin_cria_e_remove_produto(client, admin, login):
    login("admin@exemplo.com", "admin123")
    client.post(
        "/admin/novo",
        data={"nome": "Cenoura", "preco": "7,50", "disponivel": "on"},
    )
    criado = Produto.query.filter_by(nome="Cenoura").first()
    assert criado is not None

    client.post(f"/admin/{criado.id}/remover")
    assert db.session.get(Produto, criado.id) is None


def test_usuario_comum_barrado_no_admin(client, usuario, login):
    login("cliente@exemplo.com", "senha123")
    resposta = client.get("/admin/")
    assert resposta.status_code == 302
    assert "/produtos" in resposta.headers["Location"]


def test_checkout_ignora_item_indisponivel(client, usuario, login):
    disponivel = _criar_produto("Disponivel", 5.00, disponivel=True)
    indisponivel = _criar_produto("Fora de linha", 6.00, disponivel=True)
    login("cliente@exemplo.com", "senha123")
    client.post(f"/carrinho/adicionar/{disponivel.id}", data={"quantidade": 1})
    client.post(f"/carrinho/adicionar/{indisponivel.id}", data={"quantidade": 1})

    # O item sai de linha depois de ja estar no carrinho.
    indisponivel.disponivel = False
    db.session.commit()

    _fluxo_pedido(client)

    pedido = Pedido.query.filter_by(usuario_id=usuario.id).first()
    assert pedido is not None
    assert len(pedido.itens) == 1
    assert pedido.itens[0].produto_id == disponivel.id


def test_checkout_bloqueado_quando_tudo_indisponivel(client, usuario, login):
    produto = _criar_produto("Unico", 5.00, disponivel=True)
    login("cliente@exemplo.com", "senha123")
    client.post(f"/carrinho/adicionar/{produto.id}", data={"quantidade": 1})

    produto.disponivel = False
    db.session.commit()

    _fluxo_pedido(client)
    assert Pedido.query.filter_by(usuario_id=usuario.id).first() is None


def test_login_retorna_ao_destino_pretendido(client, usuario, login):
    # Rota protegida redireciona ao login carregando o next.
    resposta = client.get("/pedidos/")
    assert resposta.status_code == 302
    assert "next=" in resposta.headers["Location"]

    # Apos autenticar com o next, o usuario volta ao destino.
    retorno = client.post(
        "/login",
        data={"email": "cliente@exemplo.com", "senha": "senha123", "next": "http://localhost/pedidos/"},
    )
    assert retorno.status_code == 302
    assert retorno.headers["Location"].endswith("/pedidos/")


def test_login_ignora_next_externo(client, usuario):
    retorno = client.post(
        "/login",
        data={"email": "cliente@exemplo.com", "senha": "senha123", "next": "http://evil.com/x"},
    )
    assert retorno.status_code == 302
    assert "/produtos" in retorno.headers["Location"]
    assert "evil.com" not in retorno.headers["Location"]


def test_entrega_exige_carrinho_com_item(client, usuario, login):
    login("cliente@exemplo.com", "senha123")
    resposta = client.get("/pedidos/entrega")
    assert resposta.status_code == 302
    assert "/carrinho" in resposta.headers["Location"]


def test_entrega_campo_vazio_nao_avanca(client, produto, usuario, login):
    login("cliente@exemplo.com", "senha123")
    client.post(f"/carrinho/adicionar/{produto.id}", data={"quantidade": 1})
    client.post(
        "/pedidos/entrega",
        data={
            "destinatario": "Fulano",
            "endereco": "Rua A",
            "numero": "10",
            "bairro": "Centro",
            "cidade": "",
            "cep": "30000-000",
        },
    )
    with client.session_transaction() as sessao:
        assert "entrega" not in sessao


def test_pagamento_sem_entrega_redireciona(client, produto, usuario, login):
    login("cliente@exemplo.com", "senha123")
    client.post(f"/carrinho/adicionar/{produto.id}", data={"quantidade": 1})
    resposta = client.get("/pedidos/pagamento")
    assert resposta.status_code == 302
    assert "/pedidos/entrega" in resposta.headers["Location"]


def test_forma_pagamento_invalida_recusada(client, produto, usuario, login):
    login("cliente@exemplo.com", "senha123")
    client.post(f"/carrinho/adicionar/{produto.id}", data={"quantidade": 1})
    _fluxo_pedido(client, forma="cheque")
    assert Pedido.query.filter_by(usuario_id=usuario.id).first() is None


def test_confirmacao_somente_do_dono(client, produto, usuario, admin, login):
    login("cliente@exemplo.com", "senha123")
    client.post(f"/carrinho/adicionar/{produto.id}", data={"quantidade": 1})
    _fluxo_pedido(client)
    pedido = Pedido.query.filter_by(usuario_id=usuario.id).first()
    assert pedido is not None

    # Outro usuario nao enxerga a confirmacao de um pedido alheio.
    client.post("/logout")
    login("admin@exemplo.com", "admin123")
    resposta = client.get(f"/pedidos/confirmacao/{pedido.id}")
    assert resposta.status_code == 404
