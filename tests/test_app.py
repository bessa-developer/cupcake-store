from app import create_app


def test_app_sobe():
    app = create_app()
    assert app is not None


def test_pagina_inicial_responde():
    app = create_app()
    cliente = app.test_client()
    resposta = cliente.get("/")
    assert resposta.status_code == 200
