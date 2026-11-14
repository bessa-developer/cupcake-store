from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.extensions import db
from app.models import Produto
from app.servicos import carrinho_sessao

carrinho_bp = Blueprint("carrinho", __name__, url_prefix="/carrinho")


@carrinho_bp.route("/")
def ver():
    itens, total = carrinho_sessao.itens_detalhados()
    return render_template("carrinho.html", itens=itens, total=total)


@carrinho_bp.route("/adicionar/<int:produto_id>", methods=["POST"])
def adicionar(produto_id):
    # So adiciona produto existente e disponivel.
    produto = db.session.get(Produto, produto_id)
    if produto is None or not produto.disponivel:
        flash("Produto indisponível.")
        return redirect(url_for("produtos.catalogo"))
    quantidade = request.form.get("quantidade", 1, type=int)
    carrinho_sessao.adicionar(produto_id, max(quantidade, 1))
    flash("Item adicionado ao carrinho.")
    return redirect(url_for("carrinho.ver"))


@carrinho_bp.route("/atualizar/<int:produto_id>", methods=["POST"])
def atualizar(produto_id):
    quantidade = request.form.get("quantidade", 1, type=int)
    carrinho_sessao.atualizar(produto_id, quantidade)
    return redirect(url_for("carrinho.ver"))


@carrinho_bp.route("/remover/<int:produto_id>", methods=["POST"])
def remover(produto_id):
    carrinho_sessao.remover(produto_id)
    return redirect(url_for("carrinho.ver"))
