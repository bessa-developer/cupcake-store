from decimal import Decimal, InvalidOperation

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

from app.extensions import db
from app.models import Produto
from app.auth_utils import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def _ler_formulario():
    # Le e valida os campos do produto vindos do formulario.
    nome = request.form.get("nome", "").strip()
    descricao = request.form.get("descricao", "").strip()
    imagem = request.form.get("imagem", "").strip()
    disponivel = request.form.get("disponivel") == "on"
    try:
        preco = Decimal(request.form.get("preco", "").replace(",", "."))
    except (InvalidOperation, AttributeError):
        preco = None
    return nome, descricao, imagem, disponivel, preco


@admin_bp.route("/")
@admin_required
def lista():
    # O admin enxerga todos os produtos, disponiveis ou nao.
    produtos = Produto.query.order_by(Produto.nome).all()
    return render_template("admin/lista.html", produtos=produtos)


@admin_bp.route("/novo", methods=["GET", "POST"])
@admin_required
def novo():
    if request.method == "POST":
        nome, descricao, imagem, disponivel, preco = _ler_formulario()
        if not nome or preco is None:
            flash("Informe ao menos nome e preco validos.")
            return render_template("admin/form.html", produto=None)

        produto = Produto(
            nome=nome,
            descricao=descricao,
            imagem=imagem,
            preco=preco,
            disponivel=disponivel,
        )
        db.session.add(produto)
        db.session.commit()
        flash("Produto criado.")
        return redirect(url_for("admin.lista"))

    return render_template("admin/form.html", produto=None)


@admin_bp.route("/<int:produto_id>/editar", methods=["GET", "POST"])
@admin_required
def editar(produto_id):
    produto = db.session.get(Produto, produto_id)
    if produto is None:
        abort(404)

    if request.method == "POST":
        nome, descricao, imagem, disponivel, preco = _ler_formulario()
        if not nome or preco is None:
            flash("Informe ao menos nome e preco validos.")
            return render_template("admin/form.html", produto=produto)

        produto.nome = nome
        produto.descricao = descricao
        produto.imagem = imagem
        produto.preco = preco
        produto.disponivel = disponivel
        db.session.commit()
        flash("Produto atualizado.")
        return redirect(url_for("admin.lista"))

    return render_template("admin/form.html", produto=produto)


@admin_bp.route("/<int:produto_id>/remover", methods=["POST"])
@admin_required
def remover(produto_id):
    produto = db.session.get(Produto, produto_id)
    if produto is None:
        abort(404)
    db.session.delete(produto)
    db.session.commit()
    flash("Produto removido.")
    return redirect(url_for("admin.lista"))
