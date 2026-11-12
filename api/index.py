import os
import sys

# A Vercel executa este arquivo de dentro da pasta api/; adiciona a raiz
# do projeto ao path para encontrar o pacote da aplicacao.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

# A Vercel usa este objeto app como ponto de entrada serverless.
app = create_app()
