# **PUC RIO**

## 🚀 **PROJETO MVP CAMADA BACKEND**

**Curso**: 405-303 - Engenharia de Software

**Disciplina**: Sprint: Desenvolvimento Full Stack Básico

**Autor**: _Paulo Cesar Luna_

---

## ⭐ BACKEND - Guia de Roteiro de Hospedagem

Sistema tem por objetivo facilitar o compartilhamento de locais e hotéis entre usuários cadastrados na plataforma.

Idéia consiste em um hub de troca de locais e hospedagem entré os colaboradores da plataforma.

### 🌍 DEMO
> [Aplicação Roteiro de Hospedagem](https://api.hotel-mvp.club).  


> Entendendo o Projeto:

## 📌 Estrutura da Aplicação

O projeto está organizado da seguinte forma:

- 📂 **`/`** - Diretório principal da aplicação.
   Contém arquivos que inicializa Flask e registra os recursos da API
  
  - 📁 **`instance/`** - Diretório contendo o arquivo de do banco de dados (sqlite).
  - 📁 **`models/`** - Diretório contendo as implementações das entidades do banco de dados e operações no banco de dados.      
  - 📁 **`resources/`** - Diretório contendo recursos da API.
  - 📁 **`schema/`** - Diretório contendo os arquivos de validação, validando os schemas das entidades nas requisições GET, POST, PUT e DELETE.
  - 📁 **`static/`** - Diretório contendo arquivos ÚTEIS que suportam a aplicação. 

## 📌 Responsabilidade da Estrutura

### 📂 `/`

- 📄 **app.py**: Arquivo que inicializa Flask e registra os recursos da API.
- 📄 **sql_alchemy.py**: Arquivo que inicializa SQLAlchemy para o acesso a dados.
- 📄 **blacklist.py**: Arquivo responsável por gerenciar os JWT tokens expirados.
- 📄 **requirements.txt**: Arquivo responsável por gerenciar os pacotes/bibliotecas da aplicação (instalar, restaurar).

### 📂 `instance/`

- 📄 **db.sqlite3**: Arquivo de banco de dados, caso não exista será gerado no primeiro acesso as rotas.

### 📂 `models/`

- 📄 **__init__.py**:Arquivo inicial para models.
- 📄 **hotel.py**: Define a estrutura do modelo da entidade hotel.
- 📄 **user.py**: Define a estrutura do modelo da entidade usuário.

### 📂 `resources/`

- 📄 **__init__.py**: Arquivo inicial para recursos.
- 📄 **auth_resource.py**: Define os recursos da API relacionados a autenticação de usuários.
- 📄 **hotel_resource.py**: Define os recursos da API relacionados aos hotéis.
- 📄 **register_resource.py**: Define os recursos da API relacionados ao cadastro de login de usuários.
- 📄 **user_resource.py**: Define os recursos da API relacionados aos usuários.

### 📂 `schema/`

- 📄 **__init__.py**: Arquivo inicial para schema.
- 📄 **global_schema.py**: Define os schemas para validação de dados genérico.
- 📄 **hotel_schema.py**: Define os schemas para validação de dados relacionados ao hotel.
- 📄 **user_schema.py**: Define os schemas para validação de dados relacionados ao usuário.

### 📂 `static/`

- 📄 **Enum.py**: Define os Enum padrões para uso global.
- 📄 **swagger.json**: Arquivo de configuração swagger.

## 📌 Executando o Projeto
  > Para este trabalho foi utilizada a versão do python 3.9.

Para executar o projeto localmente, siga os passos abaixo:

- ✒️ **Clonar o repositório:**


   ```bash
   ⌨️ command line:
   git clone https://github.com/anjdric/sprint1-mvp-backend
   cd nome-do-repositorio
   ```

- ✒️ **Instalar as dependências/bibliotecas do arquivo requirements.txt.**
  > É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).
  
     ```bash
     ⌨️ command line:
     (env)$ pip install -r requirements.txt
     ```


- ✒️ **Para executar a API basta executar:**

   ```bash
   ⌨️ command line:
   (env)$ flask run --host 0.0.0.0 --port 5000
   ```

- ✒️ **Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload**

   ```bash
   ⌨️ command line:
   (env)$ flask run --host 0.0.0.0 --port 5000 --reload
   ```

- ✒️ **Rodar no Browser**  
   > Abra o [http://localhost:5001/](http://127.0.0.1:5001) no navegador para verificar o status da API em execução.

## 📌 Tecnologias Utilizadas

- Linguagem de programação: Python 3.9
- Banco de Dados: SQLite

## 📌 Dependências/Bibliotecas
> Objetivo é apenas externalizar as principais dependencias do projeto.
> 
> Não é necessário instalar manualmente, siga os passos na sessão instalar -> requirements.txt

- flask==2.2.5
- flask-apispec==0.11.4
- Flask-Cors==4.0.0
- Flask-JWT-Extended==4.5.2
- Flask-RESTful==0.3.10
- flask-restful-swagger-3==0.5.1
- Flask-SQLAlchemy==3.0.3
- SQLAlchemy==2.0.21
- marshmallow==3.20.1
- Werkzeug==3.0.1  


## 📌 Backlogs Features
> Funcionalidades que continuarão sendo implementadas, devido ao prazo não foi possível 


- [ ] Resource POST - Cadastrar Hotel
- [ ] Resource PUT - Editar Hotel
- [ ] Resource DELETE - Deletar Hotel
- [ ] Resource GET - confirmação por email


## 📌 Autores

- ✒️ **Desenvolvedor** - Paulo Cesar Luna
- ✒️ **Documentação** - Paulo Cesar Luna
