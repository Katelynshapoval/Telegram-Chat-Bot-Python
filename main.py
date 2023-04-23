import requests
import random
from bs4 import BeautifulSoup
from pathlib import Path
import logging
import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ContextTypes, MessageHandler, filters, JobQueue
TOKEN = "6247451197:AAHOHz7enZC0zG8gb-nNkB_5ZqQv2o2c-5s"
chat_id = []
user_agent = [
    'Windows 10/ Edge browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
    'Windows 7/ Chrome browser: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/47.0.2526.111 Safari/537.36',
    'Mac OS X10/Safari browser: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, '
    'like Gecko) Version/9.0.2 Safari/601.3.9',
    'Linux PC/Firefox browser: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
    'Chrome OS/Chrome browser: Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/51.0.2704.64 Safari/537.36']

# Parsing a website
def Euro():
    global user_agent
    url = "https://minfin.com.ua/ua/company/privatbank/currency/"
    data = requests.get(url, headers={"User-Agent":random.choice(user_agent)}).text
    soup = BeautifulSoup(data, 'html.parser')
    td_elements = soup.find_all('td')
    number = td_elements[22].text.split()
    return [float(n) for n in number]

def funnyAnswer(euro):
    textpos = ["LETS BUY A HOUSE", "Go on, now that candy is 0,0001% cheaper", "DANCING OMG", "You're rich now"]
    textneu = ["Life is shit, but at least euro hasn't risen", "Another bad day, let's hope it'll be better tomorrow",
               "Whatever"
               ]
    textneg = ["Shit, you're a loser", "Crying", "Good luck with that", "GUESS WHAT? You're doomed!", "Hey....well"]
    if euro[1] == 0:
        text = random.choice(textneu)
    elif euro[1] > 0:
        text = f"{random.choice(textneg)}, it has changed by {euro[1]}"
    else:
        text = random.choice(textpos)
    info = f"{text}. Euro: €{euro[0]}."
    return info
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ChatBot
async def send(context: ContextTypes.DEFAULT_TYPE):
    if chat_id !=[]:
        for id in chat_id:
            euro = Euro()
            reply = funnyAnswer(euro)
            global TOKEN
            await telegram.Bot(TOKEN).send_message(id, text=reply)
            await telegram.Bot(TOKEN).send_photo(id, photo=randomImage())
def randomImage():
    image_strings = [f"cat{x}.jpg" for x in range(17)]
    return random.choice(image_strings)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Hi! I'm a chatbot made for those who depend on Euro currency."
    global chat_id
    id_u= update.effective_chat.id
    if id_u not in chat_id:
        chat_id.append(id_u)
    await context.bot.send_message(chat_id=id_u, text=text)

async def rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    euro = Euro()
    reply = funnyAnswer(euro)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    job_queue = application.job_queue

    rate_handler = CommandHandler("rate", rate)
    start_handler = CommandHandler("start", start)

    application.add_handler(start_handler)
    application.add_handler(rate_handler)

    #job_minute = job_queue.run_repeating(send, interval=86400, first=10)

    application.run_polling()
    application.stop()
