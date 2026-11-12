from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models import Usuario
from app.auth_utils import caminho_interno_seguro

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        # Validacoes basicas antes de criar a conta.
        if not nome or not email or not senha:
            flash("Preencha todos os campos.")
            return render_template("registro.html")
        if Usuario.query.filter_by(email=email).first():
            flash("Ja existe uma conta com este email.")
            return render_template("registro.html")

        usuario = Usuario(
            nome=nome,
            email=email,
            senha_hash=generate_password_hash(senha),
        )
        db.session.add(usuario)
        db.session.commit()
        flash("Conta criada. Faca login para continuar.")
        return redirect(url_for("auth.login"))

    return render_template("registro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # O next vem na query no GET e no campo oculto no POST.
    proximo = request.values.get("next")

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        # Confere o email e o hash da senha antes de abrir a sessao.
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario is None or not check_password_hash(usuario.senha_hash, senha):
            flash("Email ou senha invalidos.")
            return render_template("login.html", proximo=proximo)

        session["usuario_id"] = usuario.id
        flash("Login realizado.")
        # Volta para a pagina pretendida quando ela for interna e segura.
        destino = caminho_interno_seguro(proximo) or url_for("produtos.catalogo")
        return redirect(destino)

    return render_template("login.html", proximo=proximo)


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("usuario_id", None)
    flash("Voce saiu da conta.")
    return redirect(url_for("produtos.catalogo"))
