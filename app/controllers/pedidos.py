from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    abort,
)

from app.extensions import db
from app.models import Pedido, ItemPedido
from app.auth_utils import login_required, usuario_atual
from app import carrinho as servico

pedidos_bp = Blueprint("pedidos", __name__, url_prefix="/pedidos")

CAMPOS_ENTREGA = ["destinatario", "endereco", "numero", "bairro", "cidade", "cep"]
FORMAS_PAGAMENTO = ["cartao", "pix", "boleto"]


@pedidos_bp.route("/entrega", methods=["GET", "POST"])
@login_required
def entrega():
    # Primeira etapa do fechamento. So avanca com carrinho que tem item disponivel.
    disponiveis, _ = servico.itens_disponiveis()
    if not disponiveis:
        flash("Seu carrinho esta vazio.")
        return redirect(url_for("carrinho.ver"))

    if request.method == "POST":
        dados = {campo: request.form.get(campo, "").strip() for campo in CAMPOS_ENTREGA}
        dados["observacao"] = request.form.get("observacao", "").strip()

        # Todos os campos de endereco sao obrigatorios; a observacao e opcional.
        if any(not dados[campo] for campo in CAMPOS_ENTREGA):
            flash("Preencha todos os dados de entrega.")
            return render_template("entrega.html", entrega=dados)

        session["entrega"] = dados
        return redirect(url_for("pedidos.pagamento"))

    return render_template("entrega.html", entrega=session.get("entrega", {}))


@pedidos_bp.route("/pagamento", methods=["GET", "POST"])
@login_required
def pagamento():
    # Segunda etapa. Depende da entrega ter sido preenchida.
    if "entrega" not in session:
        flash("Informe primeiro os dados de entrega.")
        return redirect(url_for("pedidos.entrega"))

    if request.method == "POST":
        forma = request.form.get("forma_pagamento", "")
        if forma not in FORMAS_PAGAMENTO:
            flash("Escolha uma forma de pagamento valida.")
            return render_template("pagamento.html", formas=FORMAS_PAGAMENTO)
        return _finalizar(forma)

    return render_template("pagamento.html", formas=FORMAS_PAGAMENTO)


def _finalizar(forma):
    # Confirma o pagamento e grava o pedido com itens, entrega e forma escolhida.
    disponiveis, indisponiveis = servico.itens_disponiveis()

    # Descarta e avisa cupcakes que sairam de linha durante o fechamento.
    for item in indisponiveis:
        servico.remover(item["produto"].id)
        flash(f"{item['produto'].nome} saiu de linha e foi removido do carrinho.")

    if not disponiveis:
        flash("Nenhum item disponivel para finalizar o pedido.")
        return redirect(url_for("carrinho.ver"))

    entrega = session.get("entrega", {})
    pedido = Pedido(
        usuario_id=usuario_atual().id,
        status="confirmado",
        forma_pagamento=forma,
        destinatario=entrega.get("destinatario"),
        endereco=entrega.get("endereco"),
        numero=entrega.get("numero"),
        bairro=entrega.get("bairro"),
        cidade=entrega.get("cidade"),
        cep=entrega.get("cep"),
        observacao=entrega.get("observacao"),
    )
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
    session.pop("entrega", None)
    flash("Pedido realizado com sucesso.")
    return redirect(url_for("pedidos.confirmacao", pedido_id=pedido.id))


@pedidos_bp.route("/confirmacao/<int:pedido_id>")
@login_required
def confirmacao(pedido_id):
    pedido = db.session.get(Pedido, pedido_id)
    # So o dono do pedido ve a confirmacao.
    if pedido is None or pedido.usuario_id != usuario_atual().id:
        abort(404)
    return render_template("confirmacao.html", pedido=pedido)


@pedidos_bp.route("/")
@login_required
def meus_pedidos():
    lista = (
        Pedido.query.filter_by(usuario_id=usuario_atual().id)
        .order_by(Pedido.criado_em.desc())
        .all()
    )
    return render_template("meus_pedidos.html", pedidos=lista)
