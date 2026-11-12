# Loja de Cupcakes

Loja virtual de cupcakes desenvolvida no Projeto Integrador Transdisciplinar em
Engenharia de Software II da Cruzeiro do Sul Virtual. O projeto dá continuidade ao
PI I, no qual os requisitos foram levantados com Scrum, por meio de histórias de
usuário e um backlog priorizado.

## Funcionalidades

### Definidas no PI I

O PI I previa quatro funcionalidades principais, todas presentes no sistema.

- Catálogo de produtos, com a listagem dos cupcakes e a página de cada um.
- Pedidos, com o carrinho de compras e o fechamento do pedido.
- Pagamento, com a escolha da forma (cartão, pix ou boleto) registrada no pedido.
- Entrega, com os dados do destinatário e do endereço informados no fechamento.

### Acrescentadas como evolução no PI II

O PI II evoluiu o projeto com duas funcionalidades que não faziam parte do escopo
original do PI I.

- Cadastro e autenticação de usuário, com a senha guardada em hash.
- Painel administrativo, para gerenciar os produtos do catálogo.

## Fluxo do pedido

O fechamento acontece em etapas, na ordem carrinho, entrega, pagamento e confirmação.
O pedido só é gravado ao confirmar o pagamento, guardando os itens com o preço do
momento, os dados de entrega e a forma escolhida. A etapa de pagamento é uma simulação
da escolha, sem integração com gateway real.

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
app.py           execução local
config.py        configurações e variáveis de ambiente
init_db.py       cria as tabelas e popula o catálogo de exemplo
migrar_pedido.py adiciona as colunas de entrega e pagamento a um banco já existente
```

## Como rodar localmente

1. Crie e ative um ambiente virtual.

   ```
   python -m venv venv
   venv\Scripts\activate
   ```

2. Instale as dependências.

   ```
   pip install -r requirements.txt
   ```

3. A connection string do PostgreSQL fica no `.env.local`, gerado pela Neon com
   `neon init`. Para as demais variáveis, copie `.env.example` para `.env` e preencha
   a `SECRET_KEY`, usada pela sessão do Flask. Sem a `DATABASE_URL`, o app usa um
   SQLite em memória para subir durante o desenvolvimento.

4. Crie as tabelas e popule o catálogo de exemplo.

   ```
   python init_db.py
   ```

5. Rode a aplicação.

   ```
   python app.py
   ```

   A loja fica disponível em `http://localhost:5000`.

## Testes

```
pytest
```
