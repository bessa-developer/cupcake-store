from flask import Flask

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
    app.register_blueprint(main_bp)

    return app
