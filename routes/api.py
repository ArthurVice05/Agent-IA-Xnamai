from fastapi import APIRouter

router = APIRouter()

@router.post("/webhook")
async def webhook(data: dict):

    print("WEBHOOK RECEBIDO:")
    print(data)

    return {"status": "ok"}