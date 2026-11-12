from app.extensions import db


class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    imagem = db.Column(db.String(255))
    disponivel = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Produto {self.nome}>"
