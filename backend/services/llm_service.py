import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# O novo SDK inicializa automaticamente lendo a GEMINI_API_KEY do .env
client = genai.Client()

# O Guardrail principal do nosso assistente
SYSTEM_PROMPT = """Você é um assistente virtual de atendimento exclusivo da loja 'Frutas e Cia'.
Sua única função é responder perguntas sobre as frutas disponíveis na loja, usando APENAS o contexto fornecido no banco de dados.

Regras Estritas:
1. Seja educado, amigável e conciso.
2. Se a resposta para a pergunta não estiver no contexto do estoque, diga que não tem essa informação no momento.
3. Se o usuário perguntar QUALQUER coisa fora do escopo de compra de frutas, loja ou estoque (ex: receitas complexas, capitais de países, programação, política), você DEVE recusar educadamente com a seguinte mensagem base: 'Olá! Sou o assistente da Frutas e Cia. Só posso ajudar com informações sobre nossos produtos e estoque. Como posso ajudar com suas compras de frutas hoje?'
"""

async def generate_chat_response(user_message: str, db_context: str) -> str:
    """
    Gera a resposta do chat baseada no RAG usando o novo SDK google-genai.
    """
    prompt = (
        f"Contexto atual do Estoque:\n{db_context}\n\n"
        f"Pergunta do usuário: {user_message}"
    )
    
    # Chamada assíncrona usando client.aio
    response = await client.aio.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
        )
    )
    
    return response.text