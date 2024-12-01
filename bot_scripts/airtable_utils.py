import sqlite3
import json
from config import airTable_BaseId, airTable_Token
import requests

headers = {
    "Authorization": f"Bearer {airTable_Token}",
    "Content-Type": "application/json",
}

async def create_record(tableName, data):
    endpoint = f"https://api.airtable.com/v0/{airTable_BaseId}/{tableName}"
    r = requests.post(endpoint, json=data, headers=headers)
    print(r.text)