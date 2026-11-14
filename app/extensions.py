from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# Instancia unica do SQLAlchemy, isolada aqui para os models e a factory
# importarem do mesmo lugar sem gerar import circular.
db = SQLAlchemy()

# Proteção CSRF. Todo formulário com POST precisa enviar o campo csrf_token.
csrf = CSRFProtect()
