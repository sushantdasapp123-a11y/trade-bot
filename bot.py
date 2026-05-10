import telebot
import google.generativeai as genai
import os
import requests

BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_KEY')

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎯 Trade Planner Bot Ready!\nText ya Chart screenshot pathao!")

@bot.message_handler(content_types=['photo'])
def analyze_chart(message):
    bot.reply_to(message, "📊 Chart analyze kaurichu...")
    file_info = bot.get_file(message.photo[-1].file_id)
    file = requests.get(f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}')
    image_data = file.content
    response = model.generate_content([
        "You are a stock market expert. Analyze this chart and give complete trade plan in Odia/Hindi/English: Entry, Targets, Stop Loss, Trend, R:R ratio",
        {"mime_type": "image/jpeg", "data": image_data}
    ])
    bot.reply_to(message, response.text)

@bot.message_handler(func=lambda m: True)
def analyze_text(message):
    bot.reply_to(message, "⏳ Analyzing...")
    response = model.generate_content(f"Trade plan in Odia/Hindi/English mix:\n{message.text}\nGive: Entry, Targets, SL, R:R, Quantity(capital 50000, risk 2%), Analysis")
    bot.reply_to(message, response.text)

bot.polling()
