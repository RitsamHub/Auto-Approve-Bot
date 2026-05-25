import os
from typing import List

API_ID = os.environ.get("API_ID", "29296297")
API_HASH = os.environ.get("API_HASH", "477a9529cfd84f4088539c6ab94351fc")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8152839662:AAHfUpLrgxpCtrmDDyvkclN2StFU-OtHzO0")
ADMIN = int(os.environ.get("ADMIN", "5094080507"))
PICS = (os.environ.get("PICS", "https://i.ibb.co/zVwBJ9Sd/IMG-20260331-124835-571.jpg")).split()
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1003615234781"))
NEW_REQ_MODE = os.environ.get("NEW_REQ_MODE", "True").lower() == "true"
DB_URI = os.environ.get("DB_URI", "mongodb+srv://Vebanu:Vebhav21218219@cluster0.u1oeiv8.mongodb.net/")
DB_NAME = os.environ.get("DB_NAME", "Cluster0")
IS_FSUB = os.environ.get("IS_FSUB", "True").lower() == "true"  # Set "True" For Enable Force Subscribe
AUTH_CHANNELS = list(map(int, os.environ.get("AUTH_CHANNELS", "-1003622658538 -1001891364637 -1003713022234").split())) # Add Multiple channel ids
AUTH_REQ_CHANNELS = list(map(int, os.environ.get("AUTH_REQ_CHANNELS", "-1003713022234").split())) # Add Multiple channel ids
FSUB_EXPIRE = int(os.environ.get("FSUB_EXPIRE", 2))  # minutes, 0 = no expiry
