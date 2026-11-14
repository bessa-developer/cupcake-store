import click
from flask import Flask, render_template
from werkzeug.security import generate_password_hash

from config import Config
from app.extensions import db


def create_app(config_class=Config):
    # Cria a aplicacao e carrega as configuracoes a partir do config.py.
    app = Flask(
        __name__,
        template_folder="views",
        static_folder="../static",
    )
    app.config.from_object(config_class)

    # Liga o banco a aplicacao.
    db.init_app(app)

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

    # Deixa o usuario logado disponivel nos templates.
    from app.auth_utils import registrar_contexto
    registrar_contexto(app)

    # Contador de itens do carrinho, usado no topo de todas as paginas.
    from app import carrinho

    @app.context_processor
    def injetar_contador():
        return {"total_itens_carrinho": carrinho.quantidade_total()}

    # Pagina de erro 404 no estilo da loja.
    @app.errorhandler(404)
    def pagina_nao_encontrada(erro):
        return render_template("404.html"), 404

    registrar_comandos(app)

    return app


def registrar_comandos(app):
    # Comando de linha para criar um administrador sem senha fixa no codigo.
    from app.models import Usuario

    @app.cli.command("criar-admin")
    @click.argument("nome")
    @click.argument("email")
    @click.argument("senha")
    def criar_admin(nome, email, senha):
        email = email.strip().lower()
        if Usuario.query.filter_by(email=email).first():
            click.echo("Ja existe um usuario com este email.")
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
