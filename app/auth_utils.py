from functools import wraps
from urllib.parse import urlparse

from flask import session, redirect, url_for, flash, request

from app.extensions import db
from app.models import Usuario


def usuario_atual():
    # Retorna o usuario logado a partir do id guardado na sessao, ou None.
    usuario_id = session.get("usuario_id")
    if usuario_id is None:
        return None
    return db.session.get(Usuario, usuario_id)


def caminho_interno_seguro(destino):
    # Aceita apenas caminhos do proprio site, evitando redirecionamento aberto.
    if not destino:
        return None
    partes = urlparse(destino)
    if partes.netloc and partes.netloc != request.host:
        return None
    caminho = partes.path
    if not caminho.startswith("/") or caminho.startswith("//"):
        return None
    return caminho + (f"?{partes.query}" if partes.query else "")


def _redirecionar_login():
    # Guarda a pagina pretendida para voltar a ela depois do login.
    flash("Faca login para continuar.")
    destino = request.url if request.method == "GET" else request.referrer
    return redirect(url_for("auth.login", next=destino))


def login_required(view):
    # Bloqueia a rota quando nao ha usuario logado, mandando para o login.
    @wraps(view)
    def wrapper(*args, **kwargs):
        if usuario_atual() is None:
            return _redirecionar_login()
        return view(*args, **kwargs)

    return wrapper


def admin_required(view):
    # Permite a rota apenas para usuario logado e com perfil de admin.
    @wraps(view)
    def wrapper(*args, **kwargs):
        usuario = usuario_atual()
        if usuario is None:
            return _redirecionar_login()
        if not usuario.is_admin:
            flash("Acesso restrito ao administrador.")
            return redirect(url_for("produtos.catalogo"))
        return view(*args, **kwargs)

    return wrapper


def registrar_contexto(app):
    # Deixa o usuario atual disponivel em todos os templates.
    @app.context_processor
    def injetar_usuario():
        return {"usuario_atual": usuario_atual()}
