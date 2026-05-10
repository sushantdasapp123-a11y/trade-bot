import telebot
import requests
import json
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')
ANTHROPIC_KEY = os.environ.get('ANTHROPIC_KEY')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎯 Trade Planner Bot Ready!\n\nWhatsApp trade message paste karo - AI plan banaideba!")

@bot.message_handler(func=lambda m: True)
def analyze(message):
    bot.reply_to(message, "⏳ Analyzing...")
    
    prompt = f"""Analyze this trade message and give complete plan in simple Odia/Hindi/English:

Message: {message.text}

Give:
1. Entry price
2. Targets (T1, T2, T3)
3. Stop Loss
4. Risk:Reward ratio
5. Quantity suggestion (capital 50000, risk 2%)
6. Short analysis"""

    response = requests.post(
        'https://api.anthropic.com/v1/messages',
        headers={
            'x-api-key': ANTHROPIC_KEY,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json'
        },
        json={
            'model': 'claude-sonnet-4-20250514',
            'max_tokens': 1000,
            'messages': [{'role': 'user', 'content': prompt}]
        }
    )
    
    result = response.json()
    reply = result['content'][0]['text']
    bot.reply_to(message, reply)

bot.polling()
