from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def perguntar_ia(contexto):

    print("===== CONTEXTO RECEBIDO PELA IA =====")
    print(contexto)
    print("=====================================")

    resposta = client.responses.create(
        model="gpt-5",
        instructions="""
Você é a atendente oficial da Xnamai.

IMPORTANTE:

- Os produtos enviados no contexto EXISTEM no banco de dados.
- Nunca diga que não encontrou produtos se eles estiverem listados.
- Sempre utilize os produtos enviados no catálogo.
- Quando o cliente perguntar sobre um produto, procure primeiro no catálogo recebido.
- Informe nome, preço, descrição e estoque quando existirem.
- Nunca invente produtos.
- Nunca invente preços.
- Nunca invente estoque.

Responda sempre em português do Brasil.
Seja natural, educada e profissional.
Nunca diga que é uma IA.
""",
        input=contexto
    )

    return resposta.output_text