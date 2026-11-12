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


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "chave-de-desenvolvimento")
    # Usa o Neon quando a DATABASE_URL existir; sem ela, cai para um SQLite
    # em memoria, que mantem o app e os testes rodando antes de ligar o banco.
    SQLALCHEMY_DATABASE_URI = _normalizar_url(os.getenv("DATABASE_URL")) or "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    # Forca um SQLite em memoria para os testes nunca tocarem no banco do Neon.
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SECRET_KEY = "chave-de-teste"
