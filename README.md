# **PUC RIO**

## 🚀 **PROJETO MVP CAMADA BACKEND**

**Curso**: 405-303 - Engenharia de Software

**Disciplina**: Sprint: Desenvolvimento Full Stack Básico

**Autor**: _Paulo Cesar Luna_

### ⭐ BACKEND - Guia de Roteiro de Hospedagem

Sistema tem por objetivo facilitar o compartilhamento de locais e hotéis entre usuários cadastrados na plataforma.

Idéia consiste em um hub de troca de locais e hospedagem entré os colaboradores da plataforma.

## 📌 Estrutura da Aplicação

O projeto está organizado da seguinte forma:

- 📂 **`/`** - Diretório principal da aplicação.
   Contém arquivos que inicializa Flask e registra os recursos da API
  
  - 📁 **`instance/`** - Diretório contendo o arquivo de do banco de dados (sqlite).
  - 📁 **`models/`** - Diretório contendo as implementações das entidades do banco de dados e operações no banco de dados.      
  - 📁 **`resources/`** - Diretório contendo recursos da API.
  - 📁 **`schema/`** - Diretório contendo os schemas de validação que definem as entidades do banco de dados.
  - 📁 **`static/`** - Diretório contendo arquivos UTÉIS que suportam a aplicação. 

## 📌 Responsabilidade da Estrutura

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
> Abra o http://localhost:5000/#/ no navegador para verificar o status da API em execução.



## 📌 Autores

- ✒️ **Desenvolvedor** - Paulo Cesar Luna
- ✒️ **Documentação** - Paulo Cesar Luna
