import os

import click
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_wtf.csrf import CSRFError
from werkzeug.security import generate_password_hash

from config import Config, CHAVE_DESENVOLVIMENTO
from app.extensions import db, csrf


def create_app(config_class=Config):
    # Cria a aplicação e carrega as configurações a partir do config.py.
    app = Flask(
        __name__,
        template_folder="views",
        static_folder="../static",
    )
    app.config.from_object(config_class)
    _validar_ambiente(app)

    # Liga o banco à aplicação.
    db.init_app(app)
    csrf.init_app(app)

    # Garante que os models sejam conhecidos pelo SQLAlchemy.
    from app import models  # noqa: F401

    # Registra os blueprints (controllers).
    from app.controllers.main import main_bp
    from app.controllers.produtos import produtos_bp
    from app.controllers.carrinho import carrinho_bp
    from app.controllers.pedidos import pedidos_bp
    from app.controllers.auth import auth_bp
    from app.controllers.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(produtos_bp)
    app.register_blueprint(carrinho_bp)
    app.register_blueprint(pedidos_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    # Deixa o usuário logado disponível nos templates.
    from app.servicos.autenticacao import registrar_contexto
    registrar_contexto(app)

    # Contador de itens do carrinho, usado no topo de todas as páginas.
    from app.servicos import carrinho_sessao

    @app.context_processor
    def injetar_contador():
        return {"total_itens_carrinho": carrinho_sessao.quantidade_total()}

    # Página de erro 404 no estilo da loja.
    @app.errorhandler(404)
    def pagina_nao_encontrada(erro):
        return render_template("404.html"), 404

    # Formulário enviado sem token válido, em geral por sessão expirada.
    @app.errorhandler(CSRFError)
    def token_invalido(erro):
        from app.servicos.autenticacao import caminho_interno_seguro

        flash("A sessão expirou. Tente novamente.")
        destino = caminho_interno_seguro(request.referrer) or url_for("produtos.catalogo")
        return redirect(destino)

    registrar_comandos(app)

    return app


def _validar_ambiente(app):
    # Fora dos testes, o app não sobe sem o endereço do banco.
    if not app.config.get("TESTING") and not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError(
            "Defina a variável DATABASE_URL com a connection string do Neon."
        )

    # A Vercel define a variável VERCEL. Lá o app não sobe sem uma chave de
    # sessão própria, e o cookie da sessão só trafega por HTTPS.
    if not os.getenv("VERCEL"):
        return
    if app.config.get("SECRET_KEY") in (None, "", CHAVE_DESENVOLVIMENTO):
        raise RuntimeError(
            "Defina a variável SECRET_KEY nas configurações da Vercel antes do deploy."
        )
    app.config["SESSION_COOKIE_SECURE"] = True


def registrar_comandos(app):
    # Comando de linha para criar um administrador sem senha fixa no código.
    from app.models import Usuario

    @app.cli.command("criar-admin")
    @click.argument("nome")
    @click.argument("email")
    @click.argument("senha")
    def criar_admin(nome, email, senha):
        email = email.strip().lower()
        if Usuario.query.filter_by(email=email).first():
            click.echo("Já existe um usuário com este email.")
            return
        usuario = Usuario(
            nome=nome,
            email=email,
            senha_hash=generate_password_hash(senha),
            is_admin=True,
        )
        db.session.add(usuario)
        db.session.commit()
        click.echo(f"Administrador criado: {email}")
