from telethon import TelegramClient, events
import json
import os
import subprocess

# Твої дані (вже вписані)
API_ID = 23671886
API_HASH = '9b55bf21d4b9bec2fb4bed3a1a45c566'

client = TelegramClient('sky_monitor_session', API_ID, API_HASH)

# Список каналів для моніторингу
MONITOR_CHANNELS = ['@vanek_nikolaev', '@air_alert_ua', '@povitryany_syly']

# Функція, яка відправляє файл на твій сайт (GitHub)
def push_to_github():
    try:
        subprocess.run(["git", "add", "launches.json"], check=True)
        subprocess.run(["git", "commit", "-m", "⚡️ Авто-оновлення цілей"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ КАРТА ОНОВЛЕНА: Дані відправлені на GitHub!")
    except Exception as e:
        print(f"❌ Помилка синхронізації: {e}")

@client.on(events.NewMessage(chats=MONITOR_CHANNELS))
async def handler(event):
    text = event.raw_text.lower()
    
    # Спрощена база міст для пошуку в тексті
    cities = ["київ", "умань", "одеса", "миколаїв", "дніпро", "харків", "львів", "суми", "кривий ріг"]
    found_targets = []
    
    for city in cities:
        if city in text:
            found_targets.append({
                "id": event.id,
                "type": "🚀 Ціль",
                "location": city.capitalize(),
                "time": "Щойно"
            })
    
    if found_targets:
        with open('launches.json', 'w', encoding='utf-8') as f:
            json.dump(found_targets, f, ensure_ascii=False, indent=4)
        print(f"🎯 Знайдено цілі для: {', '.join([t['location'] for t in found_targets])}")
        push_to_github()

print("🛰 Скрипт запущено. Чекаю на загрози в Telegram...")
client.start()
client.run_until_disconnected()
