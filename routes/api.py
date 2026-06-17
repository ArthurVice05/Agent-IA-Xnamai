from fastapi import APIRouter
from services.openai_service import perguntar_ia

router = APIRouter()

@router.post("/webhook")
async def webhook(data: dict):

    print("WEBHOOK RECEBIDO:")
    print(data)

    return {"status": "ok"}