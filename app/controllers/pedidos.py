from flask import Blueprint, render_template, redirect, url_for, flash

from app.extensions import db
from app.models import Pedido, ItemPedido
from app.auth_utils import login_required, usuario_atual
from app import carrinho as servico

pedidos_bp = Blueprint("pedidos", __name__, url_prefix="/pedidos")


@pedidos_bp.route("/finalizar", methods=["POST"])
@login_required
def finalizar():
    # Transforma o carrinho em um pedido do usuario logado.
    disponiveis, indisponiveis = servico.itens_disponiveis()

    # Avisa e descarta cupcakes que ficaram indisponiveis depois de entrar no carrinho.
    for item in indisponiveis:
        servico.remover(item["produto"].id)
        flash(f"{item['produto'].nome} saiu de linha e foi removido do carrinho.")

    if not disponiveis:
        flash("Nenhum item disponivel para finalizar o pedido.")
        return redirect(url_for("carrinho.ver"))

    pedido = Pedido(usuario_id=usuario_atual().id)
    db.session.add(pedido)

    # Grava o preco do momento em cada item, preservando o valor historico.
    for item in disponiveis:
        pedido.itens.append(
            ItemPedido(
                produto_id=item["produto"].id,
                quantidade=item["quantidade"],
                preco_unitario=item["produto"].preco,
            )
        )

    db.session.commit()
    servico.limpar()
    flash("Pedido realizado com sucesso.")
    return redirect(url_for("pedidos.meus_pedidos"))


@pedidos_bp.route("/")
@login_required
def meus_pedidos():
    lista = (
        Pedido.query.filter_by(usuario_id=usuario_atual().id)
        .order_by(Pedido.criado_em.desc())
        .all()
    )
    return render_template("meus_pedidos.html", pedidos=lista)
