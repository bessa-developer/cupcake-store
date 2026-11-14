from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

from app.extensions import db
from app.models import Produto, ItemPedido
from app.servicos.autenticacao import admin_required
from app.servicos.validacao import texto_ate, imagem_valida, preco_valido

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

DESCRICAO_MAXIMA = 1000


def _ler_formulario():
    # Lê os campos do produto vindos do formulário.
    return {
        "nome": request.form.get("nome", "").strip(),
        "descricao": request.form.get("descricao", "").strip(),
        "imagem": request.form.get("imagem", "").strip(),
        "disponivel": request.form.get("disponivel") == "on",
        "preco": preco_valido(request.form.get("preco")),
    }


def _erro_no_formulario(dados):
    # Devolve a mensagem do primeiro problema encontrado, ou None se estiver tudo certo.
    if not dados["nome"] or not texto_ate(dados["nome"], 120):
        return "Informe um nome com até 120 caracteres."
    if not texto_ate(dados["descricao"], DESCRICAO_MAXIMA):
        return f"A descrição pode ter no máximo {DESCRICAO_MAXIMA} caracteres."
    if not imagem_valida(dados["imagem"]):
        return "A imagem precisa ser um link começando com http:// ou https://."
    if dados["preco"] is None:
        return "Informe um preço maior que zero e até R$ 9.999,99."
    return None


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
        dados = _ler_formulario()
        erro = _erro_no_formulario(dados)
        if erro:
            flash(erro)
            return render_template("admin/form.html", produto=None)

        db.session.add(Produto(**dados))
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
        dados = _ler_formulario()
        erro = _erro_no_formulario(dados)
        if erro:
            flash(erro)
            return render_template("admin/form.html", produto=produto)

        for campo, valor in dados.items():
            setattr(produto, campo, valor)
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

    # Produto que já aparece em algum pedido não pode ser apagado, porque o
    # pedido guarda a referência a ele. Nesse caso ele só sai da vitrine.
    if ItemPedido.query.filter_by(produto_id=produto.id).first():
        produto.disponivel = False
        db.session.commit()
        flash("O produto já tem pedidos e foi retirado da vitrine.")
        return redirect(url_for("admin.lista"))

    db.session.delete(produto)
    db.session.commit()
    flash("Produto removido.")
    return redirect(url_for("admin.lista"))
