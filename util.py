
from dotenv import load_dotenv
import os

load_dotenv()
admin_ids_str = os.getenv("ADMINS", "")
ADMINS = [int(admin_id.strip()) for admin_id in admin_ids_str.split(",") if admin_id.strip()]

def isAdmin(id):
    return id in ADMINS