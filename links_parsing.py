import sqlite3
import requests
from bs4 import BeautifulSoup

dbfile = 'data\database.db'

conn = sqlite3.connect(dbfile, check_same_thread=False)

cursor = conn.cursor()
cursor.execute('SELECT plugin_link FROM plugins')
links = cursor.fetchall()

with open('links.txt', 'w', encoding='utf-8') as f:
    
    try:
        response = requests.get('https://inpad.store/plug-ins/KEO_erwm/')
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        description = soup.get_text(separator=' ', strip=True)
        
        print(description)
        f.write(f"{description}\n")
    except Exception as e:
        print(f"Ошибка при обработке {'https://inpad.store/plug-ins/KEO_erwm/'}: {e}")

print("Сбор описаний завершён.") 