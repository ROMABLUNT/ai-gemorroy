import telebot;
from telebot import types
import requests
from gigachat import GigaChat
import os
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))



name = '';
surname = '';
age = 0;



def if_exist_gemorroy(message):
    global if_gemorroy;

    if message.text == "Да" or message.text == "да" or message.text == "Ага":
        if_gemorroy = 1;
    else: 
        if_gemorroy = 0;
    
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?');
    bot.register_next_step_handler(message, get_surname);

def get_surname(message):
    global surname;
    surname = message.text;
    bot.send_message(message.from_user.id, 'Сколько тебе лет?');
    bot.register_next_step_handler(message, get_age);

def get_age(message):
    global age;
    while age == 0:
        try: 
            age = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста');
        keyboard = types.InlineKeyboardMarkup();
        key_yes = types.InlineKeyboardButton(text='Да', callback_data = 'yes');
        keyboard.add(key_yes);
        key_no= types.InlineKeyboardButton(text='Нет', callback_data='no');
        keyboard.add(key_no);
        
        end_gemorroy_text = ""

        if if_gemorroy == 1:
            end_gemorroy_text = "Похоже у вас гемморой, соболезную"
        else: 
            end_gemorroy_text = "У вас ещё нет геморроя, но, вдруг, он появится, срочно в битву с гемороооем!!"    

        question = 'Тебе ' +str(age)+' лет, тебя зовут '+surname+'? ' + end_gemorroy_text
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/gemorroy':
        bot.send_message(message.from_user.id, "У вас что, гемоРРой??");
        bot.register_next_step_handler(message, if_exist_gemorroy);
    elif message.text == '/start':
        bot.send_message(message.from_user.id, "Добро пожаловать! Я АнтиГемороройAI Бот! Я объединяю людей в борьбе с геморроем! напиши /gemorroy")
    else:
        with GigaChat(credentials=os.getenv('GIGACHAT_CREDENTIALS'), verify_ssl_certs=False) as giga:
            response = giga.chat(message.text)
            bot_response = response.choices[0].message.content
        bot.send_message(message.chat.id, bot_response)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Запомню : )');
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Попробуйте ещё раз заполнить анкету.')


bot.polling(none_stop=True, interval = 0)