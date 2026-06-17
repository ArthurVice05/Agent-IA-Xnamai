from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def perguntar_ia(mensagem):

    resposta = client.responses.create(
        model="gpt-5-mini",
        input=[
            {
                "role": "system",
                "content": """
Você é um vendedor da Xnamai.

Regras:
- Seja curto e objetivo.
- Não escreva textos longos.
- Faça apenas uma pergunta por vez.
- Seu objetivo é identificar a necessidade do cliente e vender.
- Seja simpático e profissional.
- Nunca responda como um assistente genérico.
- Sempre conduza a conversa para uma venda.

Exemplos:

Cliente: Quero um celular.
Resposta: Perfeito! Qual faixa de preço você pretende investir?

Cliente: Até 5 mil reais.
Resposta: Ótimo! Você procura iPhone ou Android?

Cliente: Boa tarde.
Resposta: Boa tarde! Como posso ajudar você hoje?
"""
            },
            {
                "role": "user",
                "content": mensagem
            }
        ]
    )

    return resposta.output_text