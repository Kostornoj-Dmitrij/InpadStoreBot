import sqlite3
import json
from bot_scripts.config import airTable_BaseId, airTable_Token
import requests
from datetime import datetime
import pytz

tableName = "Questions"
endpoint = f"https://api.airtable.com/v0/{airTable_BaseId}/{tableName}"

headers = {
    "Authorization": f"Bearer {airTable_Token}",
    "Content-Type": "application/json",
}

data = {
    "records": [
        {
            "fields": {
                "user_id": 1,
                "question": "Вопрос...",
                "answer": "Ответ",
                "created_at": datetime.now(pytz.timezone('Europe/Moscow')).isoformat()
            }
        }
    ]
}

r = requests.post(endpoint, json=data, headers=headers)
print(r.json())