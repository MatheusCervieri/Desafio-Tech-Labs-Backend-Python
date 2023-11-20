# Desafio Back-End: Api em Python Usando Flask para realizar operações CRUD com funcionários de uma empresa.

### Contexto!

Você está atuando como estagiário em uma empresa de tecnologia que está desenvolvendo uma API simples para cadastro e gestão de pessoas. O projeto surgiu em resposta a uma solicitação específica do cliente, que busca uma aplicação capaz de cadastrar informações básicas sobre funcionários e realizar operações de consulta, atualização e exclusão desses registros. A API será construída em Python, utilizando o framework de escolha do desenvolvedor (FastAPI, Flask, Django, etc.).

## Passo a Passo para Executar a Aplicação Localmente:

### Pré-requisitos:
1. Certifique-se de ter o Python instalado em sua máquina. Você pode baixá-lo em [python.org](https://www.python.org/downloads/).
2. Instale o gerenciador de pacotes pip, que geralmente é incluído com a instalação do Python.

### Passos:

```bash
# 1. Clone o Repositório:
git clone https://github.com/seu-usuario/seu-repositorio.git

# 2. Acesse o Diretório do Projeto:
cd seu-repositorio

# 3. Instale as Dependências:
pip install -r requirements.txt

# 4. Configure o Ambiente:
# Dependendo do framework escolhido, pode ser necessário configurar variáveis de ambiente ou ajustar configurações específicas do projeto. Consulte a documentação do framework para obter detalhes.

# 5. Execute a Aplicação:
python app.py
# O servidor será iniciado e a aplicação estará acessível localmente.

# 6. Teste as Funcionalidades:
# Abra um navegador e acesse http://localhost:5000 (ou outra porta configurada).
# Utilize a interface da aplicação ou ferramentas como curl ou Postman para testar as operações de CRUD.

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

