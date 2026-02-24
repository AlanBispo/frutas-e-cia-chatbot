import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

SYSTEM_PROMPT = """Você é o assistente virtual da 'Frutas e Cia'.
Sua função é usar o contexto do banco de dados para responder sobre produtos e a loja.

Regras:
1. Use os dados de estoque fornecidos para responder quantidades e preços.
2. Se a informação não estiver no contexto, diga que não sabe.
3. Se perguntarem algo fora de frutas/loja, use o Guardrail: 'Olá! Sou o assistente da Frutas e Cia. Só posso ajudar com informações sobre nossos produtos e estoque. Como posso ajudar com suas compras hoje?'
"""

async def generate_chat_response(user_message: str, context_data: str) -> str:
    prompt = (
        f"CONTEXTO DO BANCO DE DADOS:\n{context_data}\n\n"
        f"PERGUNTA DO USUÁRIO: {user_message}"
    )
    
    response = await client.aio.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
        )
    )
    
    return response.text