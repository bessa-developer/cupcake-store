# Documentação do Projeto

Loja virtual de cupcakes desenvolvida no Projeto Integrador Transdisciplinar em Engenharia de Software da Cruzeiro do Sul Virtual. Este documento reúne o levantamento de requisitos realizado no PI I, com as histórias de usuário e o backlog priorizado que orientaram a construção do sistema no PI II.

## Visão geral

O projeto nasceu da necessidade de organizar a venda de cupcakes de uma pequena loja por meio de um aplicativo web. A proposta parte da situação-problema de alinhamento para o desenvolvimento de uma loja virtual, na qual o foco inicial foi levantar os requisitos do sistema de forma clara e estruturada, evitando falhas de comunicação e retrabalho comuns em projetos sem planejamento.

O trabalho do PI I concentrou-se na elicitação e na organização dos requisitos. As funcionalidades foram descritas como histórias de usuário e reunidas em um backlog de produto priorizado, servindo de base para a implementação feita no PI II.

## Objetivo

Levantar e documentar os requisitos da loja virtual de cupcakes de maneira clara e organizada, garantindo que as necessidades do cliente sejam atendidas e que as funcionalidades principais estejam bem definidas antes do desenvolvimento.

## Metodologia

A condução do projeto seguiu a metodologia ágil Scrum, com ênfase no levantamento de requisitos por meio de histórias de usuário, na priorização do backlog de produto e na definição das tarefas de desenvolvimento. O gerenciamento das atividades foi apoiado pela ferramenta Notion, usada para registrar as histórias, organizar o backlog e acompanhar o andamento do trabalho.

## Escopo

O escopo definido no PI I contempla quatro funcionalidades principais.

- Catálogo de produtos, com a exibição dos cupcakes disponíveis
- Pedidos, com a montagem e a finalização da compra
- Pagamento, com a escolha da forma de pagamento no fechamento do pedido
- Entrega, com o registro do endereço de destino do pedido

No PI II o projeto evoluiu e recebeu duas funcionalidades adicionais que ampliam o escopo original.

- Cadastro e autenticação de usuários, para identificar o cliente e proteger suas informações
- Painel administrativo, para o gerenciamento dos produtos pela loja

## Perfis de usuário

O sistema atende a dois perfis distintos.

O cliente é a pessoa que acessa a loja para consultar os cupcakes, montar o pedido, informar a entrega, escolher a forma de pagamento e concluir a compra.

O administrador é o responsável pela loja, que gerencia os produtos do catálogo e acompanha os pedidos recebidos por meio de uma área restrita.

## Requisitos funcionais

- RF01. O sistema deve exibir a lista de cupcakes disponíveis no catálogo
- RF02. O sistema deve exibir os detalhes de um cupcake selecionado
- RF03. O sistema deve permitir adicionar um cupcake ao carrinho
- RF04. O sistema deve permitir visualizar e alterar os itens do carrinho
- RF05. O sistema deve permitir finalizar o pedido a partir do carrinho
- RF06. O sistema deve permitir informar o endereço de entrega no fechamento do pedido
- RF07. O sistema deve permitir escolher a forma de pagamento no fechamento do pedido
- RF08. O sistema deve registrar o pedido com os itens, a entrega e o pagamento
- RF09. O sistema deve exibir uma confirmação após a conclusão do pedido
- RF10. O sistema deve permitir o cadastro de novos usuários
- RF11. O sistema deve permitir o login e o logout do usuário
- RF12. O sistema deve permitir que o administrador cadastre, edite e remova produtos
- RF13. O sistema deve restringir o painel administrativo a usuários com perfil de administrador

## Requisitos não funcionais

- RNF01. O sistema deve ser acessível pelo navegador, em interface web responsiva
- RNF02. As senhas dos usuários devem ser armazenadas de forma protegida, com hash
- RNF03. Os dados devem ser persistidos em banco de dados relacional PostgreSQL
- RNF04. O sistema deve seguir a arquitetura MVC, separando dados, regras e apresentação
- RNF05. As credenciais e chaves de acesso não devem ser expostas no repositório

## Histórias de usuário

As histórias descrevem as necessidades de cada perfil no formato de ação e benefício.

### Catálogo

- Como cliente, quero ver a lista de cupcakes disponíveis para conhecer as opções da loja
- Como cliente, quero abrir os detalhes de um cupcake para ver sua descrição e seu preço

### Carrinho e pedidos

- Como cliente, quero adicionar um cupcake ao carrinho para montar meu pedido
- Como cliente, quero revisar e ajustar os itens do carrinho para conferir a compra antes de fechar
- Como cliente, quero finalizar o pedido para concluir minha compra
- Como cliente, quero ver meus pedidos realizados para acompanhar o histórico

### Entrega

- Como cliente, quero informar o endereço de entrega para receber o pedido no local correto

### Pagamento

- Como cliente, quero escolher a forma de pagamento para concluir o pedido da maneira que preferir

### Cadastro e autenticação

- Como cliente, quero criar uma conta para guardar meus dados e pedidos
- Como cliente, quero entrar e sair da minha conta para acessar a loja com segurança

### Administração

- Como administrador, quero cadastrar novos produtos para manter o catálogo atualizado
- Como administrador, quero editar e remover produtos para corrigir informações e retirar itens indisponíveis
- Como administrador, quero acessar uma área restrita para gerenciar a loja com segurança

## Backlog do produto priorizado

O backlog organiza as histórias por prioridade, da mais essencial para a mais complementar.

| Prioridade | Funcionalidade | História |
| --- | --- | --- |
| Alta | Catálogo | Ver a lista de cupcakes disponíveis |
| Alta | Catálogo | Ver os detalhes de um cupcake |
| Alta | Carrinho e pedidos | Adicionar cupcake ao carrinho |
| Alta | Carrinho e pedidos | Finalizar o pedido |
| Alta | Entrega | Informar o endereço de entrega |
| Alta | Pagamento | Escolher a forma de pagamento |
| Média | Carrinho e pedidos | Revisar e ajustar o carrinho |
| Média | Cadastro e autenticação | Criar conta e autenticar o usuário |
| Média | Administração | Cadastrar, editar e remover produtos |
| Baixa | Carrinho e pedidos | Acompanhar o histórico de pedidos |
| Baixa | Administração | Acessar a área administrativa restrita |

## Considerações finais

O levantamento realizado no PI I organizou os requisitos da loja virtual de cupcakes e definiu as funcionalidades que guiaram o desenvolvimento. A aplicação construída no PI II contempla o escopo planejado, com catálogo, pedidos, pagamento e entrega, e evolui o projeto com o cadastro e a autenticação de usuários e o painel administrativo, mantendo a coerência entre o que foi planejado e o que foi entregue.
