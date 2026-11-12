from datetime import datetime

from app.extensions import db


class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    status = db.Column(db.String(30), default="aberto", nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Um pedido reune varios itens; apagar o pedido apaga seus itens.
    itens = db.relationship("ItemPedido", backref="pedido", cascade="all, delete-orphan")

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

    def __repr__(self):
        return f"<ItemPedido pedido={self.pedido_id} produto={self.produto_id}>"
