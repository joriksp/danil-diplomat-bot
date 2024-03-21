from telebot import types
from db import JSONDatabase

database = JSONDatabase('data.json')

def greet_keyboard() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()

    donos_btn = types.InlineKeyboardButton('Донос Мизулиной', callback_data='donos')
    raffles_btn = types.InlineKeyboardButton('Розыгрыши', callback_data='raffles')
    account_btn = types.InlineKeyboardButton('Аккаунт', callback_data='account')

    markup.row(donos_btn, raffles_btn)
    markup.row(account_btn)
    
    return markup

def raffles_keyboard(raffles=None) -> types.InlineKeyboardMarkup:
    if raffles == None:
        raffles = database.get_data('raffles')

    markup = types.InlineKeyboardMarkup()
    for raffle in raffles:
        markup.add(types.InlineKeyboardButton(raffle['name'], callback_data=f'raffle_{raffle["name"]}'))

    return markup