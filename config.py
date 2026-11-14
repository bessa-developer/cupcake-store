import os

from dotenv import load_dotenv

# Em desenvolvimento, carrega as variaveis dos arquivos locais. O .env.local
# e gerado pela Neon com a DATABASE_URL; o .env serve para o resto (ex. SECRET_KEY).
load_dotenv(".env.local")
load_dotenv()


def _normalizar_url(url):
    # Fixa o driver psycopg (psycopg3) na URL do Postgres. O Neon entrega a
    # string como postgres:// ou postgresql://; aqui ela vira sempre
    # postgresql+psycopg://, evitando depender do driver padrao do SQLAlchemy.
    if not url:
        return url
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


CHAVE_DESENVOLVIMENTO = "chave-de-desenvolvimento"


class Config:
    # A chave assina o cookie da sessão. O valor de desenvolvimento só vale na
    # máquina local, e o create_app recusa esse valor em produção.
    SECRET_KEY = os.getenv("SECRET_KEY", CHAVE_DESENVOLVIMENTO)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    # O banco é o PostgreSQL do Neon. Sem a DATABASE_URL o create_app para com
    # uma mensagem, em vez de subir com um banco vazio.
    SQLALCHEMY_DATABASE_URI = _normalizar_url(os.getenv("DATABASE_URL"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # O Neon encerra conexões paradas. O pre_ping testa a conexão antes de usar
    # e abre outra se ela tiver caído.
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}


class TestConfig(Config):
    # Forca um SQLite em memoria para os testes nunca tocarem no banco do Neon.
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SECRET_KEY = "chave-de-teste"
    # Nos testes o token CSRF fica desligado, menos no teste que confere a proteção.
    WTF_CSRF_ENABLED = False
