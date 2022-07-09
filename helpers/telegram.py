import json
import requests, os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

def sendMsg(user_id: str, text: str, max_retries: int = 1):
    url = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'
    payload = {
        "chat_id": user_id,
        "text": text
    }
    for i in range(max_retries):
        r = requests.get(url, params=payload)
        isOk = False
        try:
            isOk = r.json()["ok"] == True
        except:
            pass
        if isOk == True:
            return isOk
    return isOk

def sendDocument(user_id: str, file: bytes, caption: str = "", max_retries: int = 1):
    # multipart/form-data
    url = f'https://api.telegram.org/bot{API_TOKEN}/sendDocument'
    payload = {
        "chat_id": user_id,
        "caption": caption,
    }
    for i in range(max_retries):
        r = requests.post(url, params=payload, files={"document": file})
        isOk = False
        try:
            isOk = r.json()["ok"] == True
        except:
            pass
        if isOk == True:
            return isOk
    return isOk