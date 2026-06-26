"""Sincroniza produtos da Mercos para o Supabase.

Uso:
    python sync_produtos.py
"""

from dotenv import load_dotenv

load_dotenv()

from services.sync_mercos_service import sincronizar_produtos_mercos


if __name__ == "__main__":
    resultado = sincronizar_produtos_mercos()
    print(resultado)
