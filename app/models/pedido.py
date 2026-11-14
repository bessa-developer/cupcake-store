from datetime import datetime, timezone
from decimal import Decimal

from app.extensions import db


def agora_utc():
    # Data e hora atual em UTC, sem tzinfo, para casar com a coluna DateTime.
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    # O pedido só é gravado depois do pagamento, por isso já nasce confirmado.
    status = db.Column(db.String(30), default="confirmado", nullable=False)
    criado_em = db.Column(db.DateTime, default=agora_utc, nullable=False)

    # Dados de entrega, preenchidos na etapa de entrega do fluxo de pedido.
    destinatario = db.Column(db.String(120))
    endereco = db.Column(db.String(200))
    numero = db.Column(db.String(20))
    bairro = db.Column(db.String(80))
    cidade = db.Column(db.String(80))
    cep = db.Column(db.String(15))
    observacao = db.Column(db.Text)

    # Forma de pagamento escolhida na etapa de pagamento (cartão, pix ou boleto).
    forma_pagamento = db.Column(db.String(20))

    # Um pedido reúne vários itens, e apagar o pedido apaga os itens junto.
    itens = db.relationship("ItemPedido", backref="pedido", cascade="all, delete-orphan")

    @property
    def total(self):
        return sum((item.subtotal for item in self.itens), Decimal("0"))

    def __repr__(self):
        return f"<Pedido {self.id} status={self.status}>"


class ItemPedido(db.Model):
    __tablename__ = "itens_pedido"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)
    quantidade = db.Column(db.Integer, default=1, nullable=False)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)

    produto = db.relationship("Produto")

    @property
    def subtotal(self):
        # Usa o preço gravado no pedido, não o preço atual do produto.
        return self.preco_unitario * self.quantidade

    def __repr__(self):
        return f"<ItemPedido pedido={self.pedido_id} produto={self.produto_id}>"
