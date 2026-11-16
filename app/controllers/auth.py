from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models import Usuario
from app.servicos.autenticacao import caminho_interno_seguro
from app.servicos.validacao import texto_ate, email_valido

auth_bp = Blueprint("auth", __name__)

SENHA_MINIMA = 6
SENHA_MAXIMA = 128


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        # Validações básicas antes de criar a conta.
        if not nome or not email or not senha:
            flash("Preencha todos os campos.")
            return render_template("registro.html")
        if not texto_ate(nome, 120):
            flash("O nome pode ter no máximo 120 caracteres.")
            return render_template("registro.html")
        if not email_valido(email):
            flash("Informe um email válido.")
            return render_template("registro.html")
        if not SENHA_MINIMA <= len(senha) <= SENHA_MAXIMA:
            flash(f"A senha deve ter entre {SENHA_MINIMA} e {SENHA_MAXIMA} caracteres.")
            return render_template("registro.html")
        if Usuario.query.filter_by(email=email).first():
            flash("Já existe uma conta com este email.")
            return render_template("registro.html")

        usuario = Usuario(
            nome=nome,
            email=email,
            senha_hash=generate_password_hash(senha),
        )
        db.session.add(usuario)
        db.session.commit()
        # O cadastro já abre a sessão e leva a pessoa logada ao catálogo.
        session["usuario_id"] = usuario.id
        flash("Conta criada com sucesso.")
        return redirect(url_for("produtos.catalogo"))

    return render_template("registro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # O next vem na query no GET e no campo oculto no POST.
    proximo = request.values.get("next")

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        # Confere o email e o hash da senha antes de abrir a sessão.
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario is None or not check_password_hash(usuario.senha_hash, senha):
            flash("Email ou senha inválidos.")
            return render_template("login.html", proximo=proximo)

        session["usuario_id"] = usuario.id
        flash("Login realizado.")
        # Volta para a página pretendida quando ela for interna e segura.
        destino = caminho_interno_seguro(proximo) or url_for("produtos.catalogo")
        return redirect(destino)

    return render_template("login.html", proximo=proximo)


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("usuario_id", None)
    flash("Você saiu da conta.")
    return redirect(url_for("produtos.catalogo"))
