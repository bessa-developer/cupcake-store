from flask import Blueprint, render_template, abort

from app.extensions import db
from app.models import Produto

produtos_bp = Blueprint("produtos", __name__, url_prefix="/produtos")


@produtos_bp.route("/")
def catalogo():
    # Lista apenas os cupcakes disponiveis para o cliente.
    lista = Produto.query.filter_by(disponivel=True).order_by(Produto.nome).all()
    return render_template("catalogo.html", produtos=lista)


@produtos_bp.route("/<int:produto_id>")
def detalhe(produto_id):
    produto = db.session.get(Produto, produto_id)
    if produto is None or not produto.disponivel:
        abort(404)
    return render_template("produto_detalhe.html", produto=produto)
