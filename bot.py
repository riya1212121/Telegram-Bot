"""
TODO
:сделать единый back - ???
:написать lambda
"""


import sqlite3
import random
from aiogram import Bot, types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.dispatcher import Dispatcher
from aiogram.utils.markdown import text
from aiogram.dispatcher.filters import state
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, CallbackQuery, ContentType
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from config_file import *
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import wikipedia

#
# PATH = '/Users/ategran/PycharmProjects/pythonProject3/chromedriver'
# options = webdriver.ChromeOptions()
# ser = Service('/Users/ategran/PycharmProjects/pythonProject3/chromedriver')
# driver = webdriver.Chrome(options=options, service=ser)

con = sqlite3.connect('new_db.db')
c = con.cursor()
c.execute('CREATE TABLE IF NOT EXISTS gamers ('
          '    gamer_id   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
          '    user_id     INTEGER,'
          '    balance       INTEGER,'
          '    common      INTEGER,'
          '    rare      INTEGER,'
          '    epic      INTEGER,'
          '    legendary      INTEGER'
          '    );')

bot = Bot(telegram_token, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

'''
/start
'''


# @dp.message_handler(commands=['start', 'help'])
# async def start(msg: types.Message):
#     state = dp.current_state()
#     await state.set_state('non_state')

@dp.message_handler(state='*', commands=['start', 'help'])
async def start(msg: types.Message):
    await bot.send_message(msg.from_user.id, text=start_text)


'''
/pets
'''


def return_pet_img(pet):
    n = random.randint(1, 100)
    if pet == 'cats':
        c.execute(f"SELECT link FROM cats WHERE cats.cat_id={n}")
    else:
        c.execute(f"SELECT link FROM dogs WHERE dogs.dog_id={n}")
    img = c.fetchone()
    return img[0]


def keyboard_menu(user_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    pets = {'🐱': 'cats', '🐶': 'dogs', 'Back': 'back'}
    for pet in pets:
        keyboard.insert(InlineKeyboardButton(pet, callback_data=pets[pet]))
    return keyboard


def pets_cmd(user_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    cmds = {'More': 'more', 'Back': 'back'}
    for cmd in cmds:
        keyboard.insert(InlineKeyboardButton(cmd, callback_data=cmds[cmd]))
    return keyboard


@dp.message_handler(state='*', commands=['pets'])
async def pets(msg: types.Message):
    state = dp.current_state()
    text = 'Which one tou want to see? (:'
    await bot.send_message(msg.from_user.id, text=text, reply_markup=keyboard_menu(msg.from_user.id))
    await state.set_state('pets')


@dp.callback_query_handler(state='pets')
async def inline_keyboard(callback_query: CallbackQuery):
    state = dp.current_state()
    if callback_query.data == 'back':
        await bot.send_message(callback_query.from_user.id, text=start_text)
        await state.finish()
    else:
        await state.set_state(callback_query.data)
        img = return_pet_img(callback_query.data)
        await bot.send_photo(callback_query.from_user.id, img, reply_markup=pets_cmd(callback_query.from_user.id))


@dp.callback_query_handler(state='cats')
async def inline_keyboard(callback_query: CallbackQuery):
    state = dp.current_state()
    if callback_query.data == 'back':
        text = 'Which one tou want to see? (:'
        await bot.send_message(callback_query.from_user.id, text=text,
                               reply_markup=keyboard_menu(callback_query.from_user.id))
        await state.set_state('pets')
    else:
        callback_query.data = 'cats'
        img = return_pet_img(callback_query.data)
        await bot.send_photo(callback_query.from_user.id, img, reply_markup=pets_cmd(callback_query.from_user.id))


@dp.callback_query_handler(state='dogs')
async def inline_keyboard(callback_query: CallbackQuery):
    state = dp.current_state()
    if callback_query.data == 'back':
        text = 'Which one tou want to see? (:'
        await bot.send_message(callback_query.from_user.id, text=text,
                               reply_markup=keyboard_menu(callback_query.from_user.id))
        await state.set_state('pets')
    else:
        callback_query.data = 'dogs'
        img = return_pet_img(callback_query.data)
        await bot.send_photo(callback_query.from_user.id, img, reply_markup=pets_cmd(callback_query.from_user.id))


'''
/game
'''


def game_keyboard(user_id):
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True,
                                       resize_keyboard=True)
    for act in actions:
        keyboard.insert(InlineKeyboardButton(act, callback_data=actions[act]))
    return keyboard

def game_rules(user_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.insert(InlineKeyboardButton('Understand', callback_data='_'))
    return keyboard

@dp.message_handler(state='*', commands=['game'])
async def on_text(msg: types.Message):
    state = dp.current_state()
    await state.set_state('rules')
    await bot.send_message(msg.from_user.id, text=rules,
                           reply_markup=game_rules(msg.from_user.id))


@dp.callback_query_handler(state='rules')
async def inline_keyboard(callback_query: CallbackQuery):
    state = dp.current_state()
    await bot.send_message(callback_query.from_user.id, text='Choose an action',
                               reply_markup=game_keyboard(callback_query.from_user.id))
    await state.set_state('game')


@dp.message_handler(state='game')
async def on_text(msg: types.Message):
    state = dp.current_state()
    await bot.send_message(msg.from_user.id, text='game')

@dp.message_handler(lambda x: x.from_user.id, state='game')
async def on_text(msg: types.Message):
    state = dp.current_state()
    await bot.send_message(msg.from_user.id, text='lotter')

@dp.message_handler(lambda x: x.from_user.id, state='game')
async def on_text(msg: types.Message):
    state = dp.current_state()
    await bot.send_message(msg.from_user.id, text='shop')

@dp.message_handler(lambda x: x.from_user.id, state='game')
async def on_text(msg: types.Message):
    state = dp.current_state()
    await bot.send_message(msg.from_user.id, text='lead')

@dp.message_handler(lambda x: x.from_user.id, state='game')
async def on_text(msg: types.Message):
    state = dp.current_state()
    await bot.send_message(msg.from_user.id, text='collec')

@dp.message_handler(lambda x: x.from_user.id, state='game')
async def on_text(msg: types.Message):
    state = dp.current_state()
    await bot.send_message(msg.from_user.id, text='back')



'''
/wiki - шляпа
'''

# @dp.message_handler(commands=['wiki'])
# async def wiki(msg: types.Message):
#     state = dp.current_state()
#     keyboard = InlineKeyboardMarkup(row_width=2)
#     text = 'Send me your query'
#     keyboard.insert(InlineKeyboardButton('Back', callback_data='back'))
#     await bot.send_message(msg.from_user.id, text=text, reply_markup=keyboard)
#     await state.set_state('query')
#
#
# @dp.message_handler(state='query')
# async def on_text(msg: types.Message):
#     wikipedia.set_lang("en")
#     results = wikipedia.search(msg.text)
#     match = wikipedia.suggest(msg.text)
#     if (len(results) == 0) or (match is not None):
#         text = "This page doesn't exist"
#     else:
#         text = wikipedia.summary(msg.text, sentences=6)
#     keyboard = InlineKeyboardMarkup(row_width=2)
#     keyboard.insert(InlineKeyboardButton('Back', callback_data='back'))
#     await bot.send_message(msg.from_user.id, text=text, reply_markup=keyboard)
#
#
# @dp.callback_query_handler(state='query')
# async def inline_keyboard(callback_query: CallbackQuery):
#     state = dp.current_state()
#     await bot.send_message(callback_query.from_user.id, text=start_text)
#     await state.finish()
#

'''
/tic_tac_toe - шляпа
'''

# def keyboard_tic(user_id, inp=None):
#     keyboard = InlineKeyboardMarkup(row_width=3)
#     for i in range(9):
#         if inp is not None:
#             if i == int(inp):
#                 keyboard.insert(InlineKeyboardButton('❌', callback_data='x'+str(i)))
#             else:
#                 keyboard.insert(InlineKeyboardButton('⬜️️️', callback_data=str(i)))
#         else:
#             keyboard.insert(InlineKeyboardButton('⬜️️️', callback_data=str(i)))
#     return keyboard

#
# def choose_side(user_id):
#     keyboard = InlineKeyboardMarkup(row_width=2)
#     cmds = {'❌': 'x', '⭕️': 'o'}
#     for cmd in cmds:
#         keyboard.insert(InlineKeyboardButton(cmd, callback_data=cmds[cmd]))
#     return keyboard
#
#
# @dp.message_handler(commands=['tic_tac_toe'])
# async def tic_tac_toe(msg: types.Message):
#     state = dp.current_state()
#     await bot.send_message(msg.from_user.id, text='Choose your side',
#                            reply_markup=choose_side(msg.from_user.id))
#     await state.set_state('side')
#
#
# @dp.callback_query_handler(state='side')
# async def inline_keyboard(callback_query: CallbackQuery):
#     state = dp.current_state()
#     await state.set_state(callback_query.data)
#     print(callback_query.data)
#     await bot.send_message(callback_query.from_user.id, text='Use buttons to make gambits',
#                            reply_markup=keyboard_tic(callback_query.from_user.id))
#
#
# @dp.callback_query_handler(state='x')
# async def inline_keyboard(callback_query: CallbackQuery):
#     c.execute(f"INSERT INTO tic_players VALUES (NULL, {callback_query.from_user.id}, "
#               f"SELECT )")
#
#     await bot.send_message(callback_query.from_user.id, text='Use buttons to make gambits',
#                            reply_markup=keyboard_tic(callback_query.from_user.id, callback_query.data))
#     if callback_query.data != '4':
#         pass
#
#
# @dp.callback_query_handler(state='o')
# async def inline_keyboard(callback_query: CallbackQuery):
#     print(callback_query.data)
#

"""
работает и без этого
"""

# def open_pet_url(pet):
#     if pet == 'cats':
#         driver.get('https://pixabay.com/ru/images/search/%D0%BA%D0%BE%D1%82%D1%8F%D1%82%D0%B0/')
#     else:
#         driver.get('https://www.google.com/search?q=dogs&tbm=isch&ved=2ahUKEwjq5aGUg_X1AhXEgSoKHfUvACkQ2-cCegQIABAA&oq=dogs&gs_lcp=CgNpbWcQAzIECAAQQzIECAAQQzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgQIABBDMgUIABCABDIFCAAQgAQ6BwgAELEDEEM6CAgAEIAEELEDULsJWLkQYNgSaABwAHgAgAGAAYgBnQSSAQMyLjOYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=_fUEYqrzMsSDqgH134DIAg&rlz=1C5GCEA_enRU988RU988&hl=ru')
#     time.sleep(2)
#     return

# @dp.callback_query_handler(state='next')
# async def inline_keyboard(callback_query: CallbackQuery):
#     state = dp.current_state()
#     if callback_query.data == 'back':
#         text = 'Which one tou want to see? (:'
#         await bot.send_message(callback_query.from_user.id, text=text,
#                                reply_markup=keyboard_menu(callback_query.from_user.id))
#         await state.set_state('pets')
#     else:
#         print(callback_query.data)
#         await state.set_state(callback_query.data)
#         img = return_pet_img(callback_query.data)
#         await bot.send_photo(callback_query.from_user.id, img, reply_markup=pets_cmd(callback_query.from_user.id))

'''
 написал лучше
'''
# def open_pet_url(pet):
#     if pet == 'cats':
#         driver.get('https://pixabay.com/ru/images/search/%D0%BA%D0%BE%D1%82%D1%8F%D1%82%D0%B0/')
#         time.sleep(2)
#         img = driver.execute_script("return document.getElementsByClassName('link--h3bPW')[0].href")
#         print(img)
#     else:
#         driver.get('https://www.google.com/search?q=dogs&tbm=isch&ved=2ahUKEwjq5aGUg_X1AhXEgSoKHfUvACkQ2-cCegQIABAA&oq=dogs&gs_lcp=CgNpbWcQAzIECAAQQzIECAAQQzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgQIABBDMgUIABCABDIFCAAQgAQ6BwgAELEDEEM6CAgAEIAEELEDULsJWLkQYNgSaABwAHgAgAGAAYgBnQSSAQMyLjOYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=_fUEYqrzMsSDqgH134DIAg&rlz=1C5GCEA_enRU988RU988&hl=ru')
#     return img

# @dp.callback_query_handler(state='cats')
# async def inline(callback_query: CallbackQuery):
#     state = dp.current_state()
#     if callback_query.data == 'cats':
#         driver.get('https://www.google.com/search?q=cats&tbm=isch&chips=q:cats,online_chips:kitten:FofJYT_e7Tg%3D&rlz=1C5GCEA_enRU988RU988&hl=ru&sa=X&ved=2ahUKEwiD3KeTg_X1AhUNCHcKHcAyAUEQ4lYoAHoECAEQGw')
#         time.sleep(2)
#     await state.set_state('dogs')

# @dp.callback_query_handler(state='dogs')
# async def inline(callback_query: CallbackQuery):
#     state = dp.current_state()
#     if callback_query.data == 'dogs':
#         driver.get('https://www.google.com/search?q=dogs&tbm=isch&ved=2ahUKEwjq5aGUg_X1AhXEgSoKHfUvACkQ2-cCegQIABAA&oq=dogs&gs_lcp=CgNpbWcQAzIECAAQQzIECAAQQzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgQIABBDMgUIABCABDIFCAAQgAQ6BwgAELEDEEM6CAgAEIAEELEDULsJWLkQYNgSaABwAHgAgAGAAYgBnQSSAQMyLjOYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=_fUEYqrzMsSDqgH134DIAg&rlz=1C5GCEA_enRU988RU988&hl=ru')
#         time.sleep(2)
#     await state.set_state('next')
#
#


'''
говно, переделывай
'''
# @dp.message_handler(commands=['start'])
# async def menu(msg: types.Message):
#     print('я родился')
#     state = dp.current_state()
#     await state.set_state('chose')
#     c.execute('SELECT user_id FROM baza')
#     u = c.fetchall()
#     if not str(msg.from_user.id) in str(u):
#         c.executescript(f"INSERT INTO baza VALUES ({msg.from_user.id}, '{msg.from_user.username}', 0)")
#     # await bot.send_message(msg.from_user.id, text='Ку, вот что умеет бот', reply_markup=keyboard_menu(msg.from_user.id))
#
#
# @dp.callback_query_handler()
# async def start(callback_query: CallbackQuery):
#     await bot.send_message(callback_query.from_user.id, text='Ку, вот что умеет бот', reply_markup=keyboard_menu(callback_query.from_user.id))
#
#
#
# def keyboard_menu(user_id):
#     keyboard = InlineKeyboardMarkup(row_width=2)
#     c.execute(f'SELECT balance FROM baza WHERE user_id = {user_id}')
#     services = {'Pets images': 'pets', 'Google Query': 'google'}
#     for service in services:
#         keyboard.insert(InlineKeyboardButton(service, callback_data=services[service]))
#     return keyboard
#
# @dp.callback_query_handler(state='chose')
# async def any_query(callback_query: CallbackQuery):
#     state = dp.current_state()
#     print('ccchhoo')
#     await state.set_state(callback_query.data)
#
# @dp.callback_query_handler(state='pets')
# async def any_query(callback_query: CallbackQuery):
#     print('pets')
#     state = dp.current_state()
#     await state.set_state('chose')
#
# @dp.callback_query_handler(state='google')
# async def any_query(callback_query: CallbackQuery):
#     print('google')
#     state = dp.current_state()
#     await state.set_state('chose')

'''
ээ тут что то другое уже
'''

# @dp.callback_query_handler(state='l')
# async def inline_keyboard(callback_query: CallbackQuery):
#     state = dp.current_state(user=callback_query.from_user.id)
#     if callback_query.data == 'l':
#         await state.set_state('ok')
#         await bot.send_photo(callback_query.from_user.id, 'https://i.ytimg.com/vi/Ikg21BVWPVw/hqdefault.jpg', 'либерашка')
#         keyboard = InlineKeyboardMarkup(row_width=2)
#         await bot.send_message(callback_query.from_user.id, keyboard.insert(InlineKeyboardButton('OK', callback_data='ok')))
#     await state.set_state('r')
#
#
# @dp.callback_query_handler(state='r')
# async def inline_keyboard(callback_query: CallbackQuery):
#     state = dp.current_state()
#     await state.set_state('ok')
#     await bot.send_photo(callback_query.from_user.id, 'https://lurkmore.so/images/thumb/8/87/Vatnik_33.jpg/662px-Vatnik_33.jpg', 'милый правачок')
#     keyboard.insert(InlineKeyboardButton('OK', callback_data='ok'))

executor.start_polling(dp, skip_updates=True)
