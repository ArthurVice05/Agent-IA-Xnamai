from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("https://eccvlqovbjtyzbuvisba.supabase.co")
SUPABASE_KEY = os.getenv("sb_publishable_xsafkH3rgOhZl3aSgApapQ_E1xGXgl1")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)