from flask_sqlalchemy import SQLAlchemy

# Instancia unica do SQLAlchemy, isolada aqui para os models e a factory
# importarem do mesmo lugar sem gerar import circular.
db = SQLAlchemy()
