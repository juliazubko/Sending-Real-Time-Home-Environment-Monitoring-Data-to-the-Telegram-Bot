import requests
import json

url = f'https://api.telegram.org/bot{"...your bot token here..."}/getUpdates'
response = requests.get(url)
updates = json.loads(response.text)
chat_id = updates['result'][0]['message']['chat']['id']
print(chat_id)
