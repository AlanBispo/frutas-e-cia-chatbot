## 🍎 Frutas & Cia - Hortifruti Inteligente

O Frutas & Cia é uma aplicação Full Stack desenvolvida a fins de estudo.

O sistema oferece um chatbot inteligente que utiliza RAG (Retrieval-Augmented Generation) para responder clientes com base nos dados reais do banco de dados. Além de permitir administrar produtos e ofertas em tempo real.

## 🚀 Funcionalidades principais

- Chatbot com IA (Gemini): Assistente virtual que consulta o estoque e as promoções para responder aos usuários.
- Contexto Inteligente: O bot prioriza automaticamente os preços de oferta em vez dos preços originais.
- Interface Responsiva: Design moderno construído com Tailwind CSS e feedback visual via Toasts.
- Arquitetura Assíncrona: Backend construído com FastAPI e SQLAlchemy 2.0 (Async) para alta performance.
- Painel Administrativo: CRUD completo de produtos e sistema de "Ofertas Relâmpago" com validação de preços.
  
## 🛠️ Tecnologias Utilizadas
### Frontend
- React (com TypeScript)
- Vite (Build tool ultra-rápida)
- Tailwind CSS (Estilização)
- Lucide React (Ícones)
- React Hot Toast (Notificações)
  
### Backend
- Python 3.12
- FastAPI (Framework web)
- SQLAlchemy 2.0 (ORM Assíncrono)
- Pydantic (Validação de dados)
- Google GenAI (Integração com Gemini Flash)
- MySQL (Banco de dados relacional)

### Infraestrutura
- Docker & Docker Compose

## 📦 Como Rodar o Projeto
### 1. Pré-requisitos
- Possuir o Docker e o Docker Compose instalados na máquina.
- Uma chave de API do Google Gemini (pode ser obtida gratuitamente no Google AI Studio).

### 2. Configuração do Ambiente
Na raiz do projeto, copie o arquivo .env.example e renomeie para .venv, adicionando sua chave de API do Google Gemini e alterando a senha conforme preferir.

### 3. Subindo os Containers
Execute o comando abaixo para construir e iniciar todos os serviços (Frontend, Backend e Banco de Dados):

``` 
  docker-compose up -d --build
```
### 4. Rodando as migrates

``` 
  docker exec -it frutas_api alembic upgrade head
```

### 5. Povoando o Banco de Dados (Seed)
Com os containers rodando, você precisa inserir os dados iniciais (produtos e informações da loja) para o Chatbot funcionar corretamente. Fiz um arquivo para popular os dados inicialmente, para facilitar o uso, execute o comando:

``` 
  docker exec -it frutas_api python seed.py
```

## 🖥️ Acesso ao Sistema

#### Frontend (Aplicação): http://localhost:5173

#### Backend (Docs Swagger): http://localhost:8000/docs
