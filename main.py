import telebot
from telebot import types
import json

from config import *
from keyboards import *
from texts import *
from db import JSONDatabase

bot = telebot.TeleBot(TOKEN)
database = JSONDatabase('data.json')

@bot.message_handler(commands=['start', 'help', 'menu'])
def greet(message: types.Message):
    sender_user = message.from_user
    userId = str(sender_user.id)
    userFirstName = sender_user.first_name
    userLastName = sender_user.last_name

    db_users: dict = database.get_data('users')
    
    if userId not in db_users.keys():
        print(f'Новый пользователь {userId} зарегистрирован')
        db_users[userId] = {
            'name': [userFirstName, userLastName],
            'xp': 0,
            'chance': 'default',
            'money': 0,
        }
    else:
        print(f'Пользователь {userId} уже зарегистрирован')

    database.update_data('users', db_users)

    bot.send_message(message.chat.id, 
                     GREET_MESSAGE, 
                     parse_mode='markdown', 
                     reply_markup=greet_keyboard())

@bot.callback_query_handler(func=lambda call: call.data == 'donos')
def donos(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, 
                     DONOS_MESSAGE, 
                     parse_mode='html')
    bot.register_next_step_handler(call.message, send_donos)

def send_donos(message):
    user = message.from_user
    username = user.username

    bot.send_message(message.chat.id, 
                     DONOS_SUCCESSFUL, 
                     parse_mode='html')
    
    for admin in ADMIN_IDS:
        bot.send_message(admin, 
                        f'❗ Новый донос от @{username}\n\n<i>{message.text}</i>', 
                        parse_mode='html')
        
@bot.callback_query_handler(func=lambda call: call.data == 'raffles')
def raffles(call):
    bot.answer_callback_query(call.id)

    bot.send_message(call.message.chat.id, 
                     f'🌟 <b>Текущие розыгрыши</b>:', 
                     parse_mode='html',
                     reply_markup=raffles_keyboard())
    
@bot.callback_query_handler(func=lambda call: call.data.startswith('raffle_'))
def raffle_info(call):
    bot.answer_callback_query(call.id)
    
    raffle_name = call.data.split('_')[1]
    
    raffle = next((r for r in database.get_data('raffles') if r['name'] == raffle_name), None)
    
    if raffle:
        raffle_message = f"🎁 *{raffle['name']}*\n\n📅 Заканчивается: {raffle['date_of']}\n📦 Призы"
        bot.send_message(call.message.chat.id, raffle_message, parse_mode='markdown')

@bot.callback_query_handler(func=lambda call: call.data == 'account')
def account(call: types.CallbackQuery):
    bot.answer_callback_query(call.id)
    
    try:
        userId = call.from_user.id
        userData = database.get_data('users')[str(userId)]
        print(str(userId))

        bot.send_message(call.message.chat.id, 
                        ACCOUNT_INFO(userData, userId), 
                        parse_mode='html')
    except Exception as e:
        print(e)

bot.polling()
