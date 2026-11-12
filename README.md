# Loja de Cupcakes

Loja virtual de cupcakes desenvolvida no Projeto Integrador Transdisciplinar em
Engenharia de Software II da Cruzeiro do Sul Virtual. O sistema cobre catalogo de
produtos, carrinho e pedidos, cadastro e autenticacao de usuarios e um painel
administrativo para gerenciar produtos.

## Tecnologias

- Python 3 com Flask, em arquitetura MVC
- SQLAlchemy sobre PostgreSQL hospedado no Neon
- HTML, CSS, JavaScript e Bootstrap 5 no frontend
- pytest para os testes
- Hospedagem na Vercel

## Estrutura

```
app/
  controllers/   rotas e blueprints
  models/        classes do banco (Produto, Usuario, Pedido, ItemPedido)
  views/         templates HTML
static/          css e js
tests/           testes com pytest
api/             ponto de entrada para a Vercel
app.py           execucao local
config.py        configuracoes e variaveis de ambiente
```

## Como rodar localmente

1. Crie e ative um ambiente virtual:

   ```
   python -m venv venv
   venv\Scripts\activate
   ```

2. Instale as dependencias:

   ```
   pip install -r requirements.txt
   ```

3. A connection string do PostgreSQL fica no `.env.local`, gerado pela Neon com
   `neon init`. Para as demais variaveis, copie `.env.example` para `.env`:

   - `SECRET_KEY`: chave usada pela sessao do Flask

   Sem a `DATABASE_URL`, o app usa um SQLite em memoria para subir durante o
   desenvolvimento.

4. Rode a aplicacao:

   ```
   python app.py
   ```

   A loja fica disponivel em `http://localhost:5000`.

## Testes

```
pytest
```
