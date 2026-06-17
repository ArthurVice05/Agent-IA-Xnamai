from fastapi import APIRouter
from services.openai_service import perguntar_ia

router = APIRouter()

@router.get("/chat")
def chat(mensagem: str):

    resposta = perguntar_ia(mensagem)

    return {
        "pergunta": mensagem,
        "resposta": resposta
    }