import telebot
from google import genai
import os
import requests

BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_KEY')

client = genai.Client(api_key=GEMINI_KEY)
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎯 Trade Planner Bot Ready!\nTrade message pathao!")

@bot.message_handler(content_types=['photo'])
def analyze_chart(message):
    bot.reply_to(message, "📊 Chart analyze kaurichu...")
    file_info = bot.get_file(message.photo[-1].file_id)
    file = requests.get(f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}')
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=["Analyze this stock chart and give trade plan in Odia/Hindi/English: Entry, Target, SL, Trend", 
                  {"mime_type": "image/jpeg", "data": file.content}]
    )
    bot.reply_to(message, response.text)

@bot.message_handler(func=lambda m: True)
def analyze_text(message):
    bot.reply_to(message, "⏳ Analyzing...")
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=f"Trade plan in Odia/Hindi/English:\n{message.text}\nGive: Entry, Targets, SL, R:R, Quantity(capital 50000, risk 2%), Analysis"
    )
    bot.reply_to(message, response.text)

bot.polling()
