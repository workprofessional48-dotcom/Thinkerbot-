import os

# BOT_TOKEN ko environment variable se read karo
# Agar local run kar rahe ho aur env variable nahi hai, to fallback token use hoga
BOT_TOKEN = os.getenv("BOT_TOKEN", "8232368560:AAHd8IOXBBc_siTyi3NvUyxnlnN7ze-cPSQ")  # Yaha apna actual token daalna