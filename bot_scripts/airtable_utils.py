import sqlite3
import json
from config import airTable_BaseId, airTable_Token
import requests
from datetime import datetime
import pytz

headers = {
    "Authorization": f"Bearer {airTable_Token}",
    "Content-Type": "application/json",
}

def create_record(tableName, data):
    endpoint = f"https://api.airtable.com/v0/{airTable_BaseId}/{tableName}"
    r = requests.post(endpoint, json=data, headers=headers)
    print(r.json())