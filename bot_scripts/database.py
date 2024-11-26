import sqlite3
import json
import os


project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Поднимаемся на уровень выше
dbfile = os.path.join(project_dir, 'data', 'database.db')

conn = sqlite3.connect(dbfile, check_same_thread=False)

cursor = conn.cursor()

with open(os.path.join(project_dir, 'data', 'plugins.json'), encoding='utf-8') as f:
    plugins_data = json.load(f)

plugin_descriptions = "\n".join(
    [f"{plugin['name']} ({plugin['category']}): {plugin['description']}" for plugin in plugins_data['plugins']]
)

plugin_short_descriptions = "\n".join(
    [f"{plugin['name']} ({plugin['category']}): {plugin['description'][:250]}..." for plugin in plugins_data['plugins']]
)