# Desafio Back-End: Api em Python Usando Flask para realizar operações CRUD com funcionários de uma empresa.

### Contexto!

Você está atuando como estagiário em uma empresa de tecnologia que está desenvolvendo uma API simples para cadastro e gestão de pessoas. O projeto surgiu em resposta a uma solicitação específica do cliente, que busca uma aplicação capaz de cadastrar informações básicas sobre funcionários e realizar operações de consulta, atualização e exclusão desses registros. A API será construída em Python, utilizando o framework de escolha do desenvolvedor (FastAPI, Flask, Django, etc.).

## Passo a Passo para Executar a Aplicação Localmente:

### Pré-requisitos:
1. Certifique-se de ter o Python instalado em sua máquina. Você pode baixá-lo em [python.org](https://www.python.org/downloads/).
2. Instale o gerenciador de pacotes pip, que geralmente é incluído com a instalação do Python.

### Passos:

#### 1. Clone o Repositório:

#### 2. Acesse o Diretório do Projeto:
```bash
cd diretório-clonado
```

#### 3. Instale as Dependências:
```bash
pip install -r requirements.txt
```

#### 4. Execute a Aplicação:
```bash
flask run 
```

#### 5. Teste as Funcionalidades:
Abra um navegador e acesse http://localhost:5000/teste (ou outra porta configurada).

Essa rota irá abrir uma página html teste que permitirá que você teste a aplicação. 

Você também pode utilizar ferramentas como curl ou Postman para testar as operações/rotas de CRUD que serão listadas abaixo.

# Documentação da API

## 1. Cadastrar Pessoa

### Rota
- **POST** `/pessoas/adicionar`

#### Descrição
Cadastra uma nova pessoa.

#### Parâmetros no Corpo da Requisição
- `nome_completo` (string): Nome completo da pessoa.
- `data_nascimento` (string): Data de nascimento no formato "YYYY-MM-DD".
- `endereco` (string): Endereço da pessoa.
- `cpf` (string): CPF da pessoa.
- `estado_civil` (string): Estado civil da pessoa.

#### Resposta
- Código 201 (Created) em caso de sucesso, com os dados da pessoa cadastrada.
- Código 400 (Bad Request) em caso de campos obrigatórios ausentes ou inválidos.
- Código 500 (Internal Server Error) em caso de erro interno no servidor.

## 2. Atualizar Pessoa por ID

### Rota
- **PUT** `/pessoas/edit/id/<int:pessoa_id>`

#### Descrição
Atualiza os dados de uma pessoa com base no ID.

#### Parâmetros no Corpo da Requisição
- `campo` (string): Nome do campo a ser atualizado.
- `novo_valor` (string): Novo valor para o campo especificado.

#### Resposta
- Código 200 (OK) em caso de sucesso, com os dados atualizados da pessoa.
- Código 400 (Bad Request) em caso de campos ausentes ou inválidos.
- Código 404 (Not Found) se a pessoa com o ID especificado não for encontrada.
- Código 500 (Internal Server Error) em caso de erro interno no servidor.

## 3. Atualizar Pessoa por CPF

### Rota
- **PUT** `/pessoas/edit/cpf/<string:pessoa_cpf>`

#### Descrição
Atualiza os dados de uma pessoa com base no CPF.

#### Parâmetros no Corpo da Requisição
- `campo` (string): Nome do campo a ser atualizado.
- `novo_valor` (string): Novo valor para o campo especificado.

#### Resposta
- Código 200 (OK) em caso de sucesso, com os dados atualizados da pessoa.
- Código 400 (Bad Request) em caso de campos ausentes ou inválidos.
- Código 404 (Not Found) se a pessoa com o CPF especificado não for encontrada.
- Código 500 (Internal Server Error) em caso de erro interno no servidor.

## 4. Listar Pessoas

### Rota
- **GET** `/pessoas`

#### Descrição
Lista todas as pessoas cadastradas.

#### Resposta
- Código 200 (OK) em caso de sucesso, com a lista de pessoas cadastradas.
- Código 500 (Internal Server Error) em caso de erro interno no servidor.

## 5. Obter Pessoa por CPF

### Rota
- **GET** `/pessoas/<string:cpf>`

#### Descrição
Obtém os dados de uma pessoa com base no CPF.

#### Parâmetros
- Método: GET
- Caminho: `/pessoas/<string:cpf>`

#### Resposta
- Código 200 (OK) em caso de sucesso, com os dados da pessoa.
- Código 400 (Bad Request) se o CPF for inválido.
- Código 404 (Not Found) se a pessoa com o CPF especificado não for encontrada.
- Código 500 (Internal Server Error) em caso de erro interno no servidor.

## 6. Obter Pessoa por ID

### Rota
- **GET** `/pessoas/id/<int:pessoa_id>`

#### Descrição
Obtém os dados de uma pessoa com base no ID.

#### Resposta
- Código 200 (OK) em caso de sucesso, com os dados da pessoa.
- Código 404 (Not Found) se a pessoa com o ID especificado não for encontrada.
- Código 500 (Internal Server Error) em caso de erro interno no servidor.

## 7. Deletar Pessoa por ID

### Rota
- **DELETE** `/pessoas/delete/id/<int:pessoa_id>`

#### Descrição
Deleta uma pessoa com base no ID.

#### Resposta
- Código 200 (OK) em caso de sucesso, com mensagem de exclusão bem-sucedida.
- Código 404 (Not Found) se a pessoa com o ID especificado não for encontrada.
- Código 500 (Internal Server Error) em caso de erro interno no servidor.

## 8. Deletar Pessoa por CPF

### Rota
- **DELETE** `/pessoas/delete/cpf/<string:cpf>`

#### Descrição
Deleta uma pessoa com base no CPF.

#### Resposta
- Código 200 (OK) em caso de sucesso, com mensagem de exclusão bem-sucedida.
- Código 404 (Not Found) se a pessoa com o CPF especificado não for encontrada.
- Código 500 (Internal Server Error) em caso de erro interno no servidor.

## Visual Overview

Dashboard:

![Dashboard](readme/dashboard.png "Dashboard")


### Usage

1 - First, you need to install and download Docker and Docker Compose.

2- Open the project folder.

3- Run docker compose command inside the project folder

```
docker-compose up –-build
```
or
```
docker compose up –-build
```

4- Go to the login URL:

```
http://localhost:3000/
```

If you are not a 42 student:

```
http://localhost:3000/test
```

### What was done in the project?!

<List>
        <li>The website allows users to play real-time multiplayer Pong games with a chat feature and complies with specific rules, including using Node and NestJS for the backend, a TypeScript and React for the frontend, and PostgreSQL for the database.</li>
        <li>The User Account section of the website allows users to log in using the OAuth system of 42 intranet API, choose a unique name and avatar, enable two-factor authentication, add friends, view their status, display their stats, and have a match history including 1v1 games and ladder.</li>
        <li>The website's chat feature allows users to create public, private or password-protected channels, send direct messages and block other users, while channel owners can set a password, remove it, and appoint other administrators who have specific permissions to kick, ban or mute users, as well as invite users to play Pong games and access their profiles.</li>
        <li>The website is designed to allow users to play live Pong games against each other and features a matchmaking system for finding opponents, a customizable Pong game that is true to the original 1972 version, and the ability to select a default version without any extra features. The game is also responsive to ensure optimal gameplay.</li>
        <li>Ensuring full functionality of the website necessitates tackling security concerns such as hashing any stored passwords, safeguarding against SQL injections, and incorporating server-side validation for forms and user input.</li>
</List>

## Index

*  [Summary](#Summary)
*  [Main Technologies](#Main-Technologies)
*  [Visual Overview](#visual-overview)
*  [Usage](#Usage)
*  [What was done in the project?!](#What-was-done-in-the-project)
*  [Requirements](#Requirements)

