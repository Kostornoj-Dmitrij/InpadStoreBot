import sqlite3
import json
from config import airTable_BaseId, airTable_Token
import requests
from datetime import datetime
import pytz
from database import cursor, conn

headers = {
    "Authorization": f"Bearer {airTable_Token}",
    "Content-Type": "application/json",
}

async def create_record(tableName, data):
    endpoint = f"https://api.airtable.com/v0/{airTable_BaseId}/{tableName}"
    r = requests.post(endpoint, json=data, headers=headers)
    print(r.text)

async def update_record(tableName, data, user_id):
    record_id = await get_record_id(tableName, user_id)
    endpoint = f"https://api.airtable.com/v0/{airTable_BaseId}/{tableName}/{record_id}"
    r = requests.patch(endpoint, json=data, headers=headers)
    print(r.text)

async def create_trace_data(user_id, act_type, act):
    return {
        "records": [
            {
                "fields": {
                    "user_id": user_id,
                    "act_type": act_type,
                    "act": act,
                    "created_at": datetime.now(pytz.timezone("Europe/Moscow")).isoformat()
                }
            }
        ]
    }

async def save_trace(user_id, act_type, act):
    cursor.execute("SELECT user_id FROM Users WHERE t_user_chat_id = ?", (user_id, ))
    user_database_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO User_Trace (user_id, act_type, act, created_at) "
                   "VALUES (?, ?, ?, DATETIME('now'))",
                   (user_database_id, act_type, act))
    conn.commit()
    data = await create_trace_data(user_database_id, act_type, act)
    await create_record("User_Trace", data)

async def get_record_id(tableName, user_id):
    endpoint = f"https://api.airtable.com/v0/{airTable_BaseId}/{tableName}"
    response = requests.get(endpoint, headers=headers)
    records = response.json().get('records', [])
    record_id = None
    for record in records:
        if record.get('fields', {}).get('user_id') == user_id:
            record_id = record['id']
            break
    return record_id