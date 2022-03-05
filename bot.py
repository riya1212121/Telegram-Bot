"""
TODO

"""

import sqlite3
import random
from aiogram import Bot, types
from aiogram.types import ReplyKeyboardMarkup, InputMedia, InputFile, ReplyKeyboardRemove
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, CallbackQuery, ContentType
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from config_file import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


con = sqlite3.connect('new_db.db')
c = con.cursor()
c.execute('CREATE TABLE IF NOT EXISTS gamers ('
          '    gamer_id   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
          '    user_id     INTEGER,'
          '    balance       INTEGER DEFAULT (0)'
          '    );')
c.execute('CREATE TABLE IF NOT EXISTS store ('
          '    item_id   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
          '    rarity    VARCHAR (6),'
          '    link      VARCHAR (30),'
          '    media      VARCHAR (50)'
          '    );')
c.execute('CREATE TABLE IF NOT EXISTS collection ('
          '    collection_id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
          '    user_id     INTEGER,'
          '    item_id       INTEGER,'
          '    FOREIGN KEY (item_id) REFERENCES store (item_id)'
          '    );')
bot = Bot(telegram_token, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

'''
/start
'''


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


class PlayLottery(StatesGroup):
    mode = State()
    bet = State()
    number = State()


class SearchShop(StatesGroup):
    price = State()
    rarity = State()


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


def click_keyboard(user_id):
    keyboard = InlineKeyboardMarkup(one_time_keyboard=True,
                                    resize_keyboard=True)
    actions = {'Click⭐️': 'click', 'Back': 'back'}
    for act in actions:
        keyboard.insert(InlineKeyboardButton(act, callback_data=actions[act]))
    return keyboard


def back_button(user_id):
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True,
                                   resize_keyboard=True)
    keyboard.insert(InlineKeyboardButton('Back', callback_data='_'))
    return keyboard


def lottery_mode(user_id):
    keyboard = ReplyKeyboardMarkup(row_width=2,
                                   one_time_keyboard=True,
                                   resize_keyboard=True)
    modes = {'50% Chance - 2x': '50', '25% Chance - 4x': '25', 'Back': 'back'}
    for mode in modes:
        keyboard.insert(InlineKeyboardButton(mode, callback_data=modes[mode]))
    return keyboard


def check_number(user_id, text):
    try:
        pick = int(text)
        if pick not in range(1, 101):
            return False
        return True
    except ValueError:
        return False


def back_kb(user_id):
    keyboard = InlineKeyboardMarkup(one_time_keyboard=True,
                                    resize_keyboard=True)
    keyboard.insert(InlineKeyboardButton('Back', callback_data='back'))
    return keyboard


def ask_more(user_id):
    keyboard = ReplyKeyboardMarkup(row_width=2,
                                   one_time_keyboard=True,
                                   resize_keyboard=True)
    options = {'Yes!': 'yes', 'Back': 'back'}
    for opt in options:
        keyboard.insert(InlineKeyboardButton(opt, callback_data=options[opt]))
    return keyboard


def choose_rarity(user_id):
    keyboard = ReplyKeyboardMarkup(row_width=3,
                                   one_time_keyboard=True,
                                   resize_keyboard=True)
    options = {'Common': 'common', 'Rare': 'rare', 'Epic': 'epic', 'Back': 'back'}
    for opt in options:
        keyboard.insert(InlineKeyboardButton(opt, callback_data=options[opt]))
    return keyboard


def buy_button(user_id):
    keyboard = InlineKeyboardMarkup(row_width=3)
    options = {'⬅️': 'prev', 'Buy': 'buy',
               '➡️': 'next', 'Back': 'Back'}
    for o in options:
        keyboard.insert(InlineKeyboardButton(o, callback_data=options[o]))
    return keyboard


def search_items(user_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    options = {'⬅️': 'prev', '➡️': 'next',
               'Back': 'Back'}
    for o in options:
        keyboard.insert(InlineKeyboardButton(o, callback_data=options[o]))
    return keyboard


@dp.message_handler(state='*', commands=['game'])
async def on_text(msg: types.Message):
    state = dp.current_state()
    await state.set_state('rules')
    c.execute(f"SELECT user_id FROM gamers WHERE gamers.user_id = {msg.from_user.id}")
    if c.fetchone() is None:
        c.executescript(f"INSERT INTO gamers VALUES (null, {msg.from_user.id}, 0)")
    await bot.send_message(msg.from_user.id, text=rules,
                           reply_markup=game_rules(msg.from_user.id))
    ReplyKeyboardRemove()


@dp.callback_query_handler(state='rules')
async def inline_keyboard(callback_query: CallbackQuery):
    state = dp.current_state()
    await bot.send_message(callback_query.from_user.id, text='Choose an action',
                           reply_markup=game_keyboard(callback_query.from_user.id))
    await state.set_state('game')


@dp.message_handler(lambda message: message.text == 'Play🔥', state='game')
async def on_text(msg: types.Message):
    state = dp.current_state()
    c.execute(f"SELECT balance FROM gamers WHERE gamers.user_id = {msg.from_user.id}")
    score = c.fetchone()[0]
    await bot.send_message(msg.from_user.id, text=f'SCORE: {score}',
                           reply_markup=click_keyboard(msg.from_user.id))
    await state.set_state('clicker')


"""
clicker gameplay 
"""


@dp.callback_query_handler(state='clicker')
async def inline_keyboard(callback_query: CallbackQuery):
    state = dp.current_state()
    if callback_query.data == 'back':
        await bot.send_message(callback_query.from_user.id, text='Choose an action',
                               reply_markup=game_keyboard(callback_query.from_user.id))
        await state.set_state('game')
    else:
        c.execute(f"SELECT balance FROM gamers WHERE gamers.user_id = {callback_query.from_user.id}")
        score = c.fetchone()[0]
        await callback_query.message.edit_text(text=f'SCORE: {score + 1}',
                                               reply_markup=click_keyboard(callback_query.from_user.id))
        c.executescript(f"UPDATE gamers SET balance = {score + 1} WHERE user_id = {callback_query.from_user.id}")


@dp.message_handler(lambda message: message.text == 'Lottery🍀', state='game')
async def on_text(msg: types.Message):
    state = dp.current_state()
    await state.set_state('fortune')
    await bot.send_message(msg.from_user.id, text=lottery_text, reply_markup=lottery_mode(msg.from_user.id))


'''
lottery gameplay
'''


@dp.message_handler(lambda message: message.text in ['50% Chance - 2x', '25% Chance - 4x', 'Yes!'], state='fortune')
async def on_text(msg: types.Message, state: FSMContext):
    prices = {'50% Chance - 2x': 20, '25% Chance - 4x': 40, 'Yes!': 0}
    id = msg.from_user.id
    if msg.text != 'Yes!':
        await state.update_data(mode=prices[msg.text])
    else:
        data = await state.get_data()
        prices[msg.text] = data['mode']
    c.execute(f"SELECT balance FROM gamers WHERE user_id = {id}")
    score = c.fetchone()[0]
    await bot.send_message(msg.from_user.id, text=f'Your balance: {score}')
    if score < prices[msg.text]:
        await bot.send_message(msg.from_user.id, text=f'Click more points, you need at least {prices[msg.text]}! \n'
                                                      f'Choose action',
                               reply_markup=game_keyboard(id))
        await state.set_state('game')
    else:
        await PlayLottery.mode.set()
        await bot.send_message(msg.from_user.id, text=f'Write your bet equal or more than {prices[msg.text]} )',
                               reply_markup=back_button(id))


@dp.message_handler(lambda message: message.text == 'Back', state=PlayLottery.mode)
async def on_text(msg: types.Message, state: FSMContext):
    await bot.send_message(msg.from_user.id, text=lottery_text, reply_markup=lottery_mode(msg.from_user.id))
    await state.set_state('fortune')


@dp.message_handler(state=PlayLottery.mode)
async def on_text(msg: types.Message, state: FSMContext):
    user_data = await state.get_data()
    try:
        bet = int(msg.text)
        c.execute(f"SELECT balance FROM gamers WHERE user_id = {msg.from_user.id}")
        score = c.fetchone()[0]
        if score < bet:
            await bot.send_message(msg.from_user.id,
                                   text='The bet is bigger than your balance. \n Write your bet (in clicks)')
        elif bet < user_data['mode']:
            await bot.send_message(msg.from_user.id,
                                   text=f"Too small bet. Should be equal or more than {user_data['mode']}."
                                        f' \n Write your bet (in clicks)')
        else:
            await bot.send_message(msg.from_user.id, text='Your number (1-100): ')
            await state.update_data(bet=bet)
            await PlayLottery.bet.set()
    except ValueError:
        await bot.send_message(msg.from_user.id,
                               text='Error: incorrect input! \n Write your bet by digits')


@dp.message_handler(lambda message: message.text == 'Back', state=PlayLottery.bet)
async def on_text(msg: types.Message, state: FSMContext):
    await bot.send_message(msg.from_user.id, text=lottery_text, reply_markup=lottery_mode(msg.from_user.id))
    await state.set_state('fortune')


@dp.message_handler(state=PlayLottery.bet)
async def on_text(msg: types.Message, state: FSMContext):
    user_data = await state.get_data()
    id = msg.from_user.id
    areas = [[(1, 50), (51, 100)], [(1, 25), (26, 50), (51, 75), (76, 100)]][int(user_data['mode'] / 20 - 1)]
    lucky_area = random.randint(0, int(user_data['mode'] / 10 - 1))
    c.execute(f"SELECT balance FROM gamers WHERE user_id = {id}")
    score = c.fetchone()[0]
    if check_number(id, msg.text):
        c.executescript(f"UPDATE gamers SET balance = {score - user_data['bet']} WHERE user_id = {id}")
        if int(msg.text) in range(areas[lucky_area][0], areas[lucky_area][1]):
            await bot.send_message(id, text=f"You win, number is in the area {areas[lucky_area]}! Double bet")
            c.executescript(f"UPDATE gamers SET balance = {score + int(user_data['mode'] / 10) * int(user_data['bet'])}"
                            f" WHERE user_id = {id}")
        else:
            await bot.send_message(id, text=f"You lose, number isn't in the area {areas[lucky_area]}")
        await state.set_state('fortune')
        await bot.send_message(id, text="Play one more time? (:", reply_markup=ask_more(id))
    else:
        await bot.send_message(id, text='Error: incorrect input! \n Number should be written by digits and in the '
                                        'range from 1 to 100')


@dp.message_handler(lambda message: message.text == 'Shop💰', state='game')
async def on_text(msg: types.Message):
    state = dp.current_state()
    id = msg.from_user.id
    await bot.send_message(msg.from_user.id, text='Choose rarity', reply_markup=choose_rarity(id))
    await state.set_state('rarity')


@dp.message_handler(lambda message: message.text in ['Common', 'Rare', 'Epic'], state='rarity')
async def on_text(msg: types.Message, state: FSMContext):
    id = msg.from_user.id
    rarity = msg.text
    await state.update_data(current_pic=1, rarity=rarity)
    await bot.send_photo(id, open_pic[rarity], reply_markup=buy_button(id))
    await SearchShop.price.set()


@dp.callback_query_handler(state=SearchShop.price)
async def inline_keyboard(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    prices = {'Common': 10, 'Rare': 25, 'Epic': 100}
    id = callback_query.from_user.id
    c.execute(f"SELECT count(link) FROM store WHERE rarity = '{user_data['rarity']}'")
    board = c.fetchone()[0]
    c.execute(f"SELECT link FROM store WHERE rarity = '{user_data['rarity']}'")
    pic = user_data['current_pic']
    links = []
    for img in c.fetchall():
        links.append(img)
    navigation = ['prev', 'next']
    if callback_query.data in navigation:
        await state.update_data(current_pic=pic + (2 * navigation.index(callback_query.data)) - 1)
        if (navigation.index(callback_query.data) == 0) and (pic == 1):
            await state.update_data(current_pic=board)
        elif (navigation.index(callback_query.data) == 1) and (pic == board):
            await state.update_data(current_pic=1)
        user_data = await state.get_data()
        path = f"{path_to_dir}/{user_data['rarity'][0]}{user_data['current_pic']}.jpg"
        file = InputMedia(media=InputFile(path))
        await callback_query.message.edit_media(file, reply_markup=buy_button(id))
    elif callback_query.data == 'Back':
        await bot.send_message(callback_query.from_user.id, text='Choose rarity', reply_markup=choose_rarity(id))
        await state.set_state('rarity')
    else:
        c.execute(f"SELECT balance FROM gamers WHERE user_id = {id}")
        score = c.fetchone()[0]
        price = prices[user_data['rarity']]
        await bot.send_message(id,
                               text=f"This item costs {price} \n"
                                    f"You have {score}")
        if score < price:
            await bot.send_message(id, text=f"You need {price - score} clicks to buy it.")
            await bot.send_photo(id, open_pic[user_data['rarity']], reply_markup=buy_button(id))
        else:
            user_data = await state.get_data()
            path = f"{path_to_dir}/{user_data['rarity'][0]}{user_data['current_pic']}.jpg"
            c.execute(f"SELECT item_id FROM store WHERE link = '{path}'")
            item_id = c.fetchone()[0]
            c.execute(f"SELECT item_id FROM collection WHERE item_id = '{item_id}'")
            if c.fetchone() is None:
                c.executescript(f"UPDATE gamers SET balance = {score - price} WHERE user_id = {id}")
                c.executescript(f"INSERT INTO collection VALUES (null, {id}, {item_id})")
                await bot.send_message(id, text=f"Transaction completed. Check your collection \n"
                                                f"Now your balance is {score - price}")
            else:
                await bot.send_message(id, text=f"You have already bought this item.")
            await bot.send_message(callback_query.from_user.id, text='Choose rarity', reply_markup=choose_rarity(id))
            await state.set_state('rarity')


@dp.message_handler(lambda message: message.text == 'Leaderboard🏆', state='game')
async def on_text(msg: types.Message):
    state = dp.current_state()
    lp = []
    c.execute(f"SELECT balance from gamers ORDER BY balance DESC")
    for i in range(3):
        lp.append(c.fetchone()[0])
    c.execute(f"SELECT user_id from gamers ORDER BY balance DESC")
    leaders = f'''🥇{c.fetchone()[0]}: {lp[0]}\n
    🥈{c.fetchone()[0]}: {lp[1]}\n
    🥉{c.fetchone()[0]}: {lp[2]}\n
    '''
    await state.set_state('clicker')
    await bot.send_message(msg.from_user.id, text=leaders, reply_markup=back_button(msg.from_user.id))


@dp.message_handler(lambda message: message.text == 'My collection🧸', state='game')
async def on_text(msg: types.Message):
    state = dp.current_state()
    id = msg.from_user.id
    await bot.send_message(id, text='Choose rarity', reply_markup=choose_rarity(id))
    await state.set_state('collection_rarity')


@dp.message_handler(lambda message: message.text in ['Common', 'Rare', 'Epic'], state='collection_rarity')
async def on_text(msg: types.Message, state: FSMContext):
    id = msg.from_user.id
    rarity = msg.text
    c.execute(
        f"select item_id from collection where (item_id in (select item_id from store where rarity = '{rarity}')) and (user_id = {id});")
    item_list = c.fetchall()
    if not item_list:
        await bot.send_message(id, text=f"You don't have any {rarity} items")
        await bot.send_message(id, text='Choose rarity', reply_markup=choose_rarity(id))
    else:
        item_list = [item[0] for item in item_list]
        c.execute(f"select link from store where item_id in ({str(item_list)[1:-1:]});")
        link_list = c.fetchall()
        link_list = [link[0] for link in link_list]
        c.execute(f"SELECT media FROM store WHERE item_id = {item_list[0]}")
        img = c.fetchone()[0]
        await bot.send_photo(id, img, reply_markup=search_items(id))
        await state.update_data(current_pic=item_list[0], items=link_list, rarity=rarity)
        await SearchShop.rarity.set()


@dp.callback_query_handler(state=SearchShop.rarity)
async def inline_keyboard(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    items = user_data['items']
    navigation = ['prev', 'next']
    if callback_query.data in navigation:
        move = 2 * navigation.index(callback_query.data) - 1
        if len(items) != 1:
            items = items[move:] + items[:move]
        await state.update_data(items=items)
        user_data = await state.get_data()
        file = InputMedia(media=InputFile(user_data['items'][0]))
        await callback_query.message.edit_media(file, reply_markup=search_items(id))
    elif callback_query.data == 'Back':
        await bot.send_message(callback_query.from_user.id, text='Choose rarity', reply_markup=choose_rarity(id))
        await state.set_state('collection_rarity')


@dp.message_handler(lambda message: message.text == 'Back', state='*')
async def on_text(msg: types.Message):
    state = dp.current_state()
    await bot.send_message(msg.from_user.id, text='Choose an action',
                           reply_markup=game_keyboard(msg.from_user.id))
    await state.set_state('game')


@dp.message_handler(lambda message: message.text == 'Back🚪', state='game')
async def on_text(msg: types.Message):
    state = dp.current_state()
    await state.finish()
    ReplyKeyboardRemove()
    await bot.send_message(msg.from_user.id, text=start_text)


'''
/cities
'''

class City(StatesGroup):
    name = State()

def give_up(user_id):
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True,
                                   resize_keyboard=True)
    keyboard.insert(InlineKeyboardButton('Give up 🏳️', callback_data='_'))
    return keyboard


@dp.message_handler(state='*', commands=['cities'])
async def on_text(msg: types.Message):
    state = dp.current_state()
    id = msg.from_user.id
    await bot.send_message(id, text=city_rules, reply_markup=game_rules(id))
    await state.set_state('start_game')


@dp.callback_query_handler(state='start_game')
async def inline_keyboard(callback_query: CallbackQuery, state: FSMContext):
    id = callback_query.from_user.id
    await bot.send_message(id, text='Odintsovo \n O', reply_markup=give_up(id))
    named = ['Odintsovo']
    await state.update_data(name='Odintsovo', named=named)
    await City.name.set()


@dp.message_handler(lambda message: message.text == 'Give up 🏳️', state=City.name)
async def on_text(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    id = msg.from_user.id
    await bot.send_message(id, text=f"Your score is {int((len(data['named'])-1)/2)}")
    await state.finish()
    await bot.send_message(msg.from_user.id, text=start_text)


@dp.message_handler(state=City.name)
async def on_text(msg: types.Message, state: FSMContext):
    city = msg.text[0].capitalize() + msg.text[1:].lower()
    id = msg.from_user.id
    data = await state.get_data()
    named = data['named']
    task = data['name'][-1]
    if city[0] not in [task.lower(), task.capitalize()]:
        await bot.send_message(id, text=f"Your task is to send a name of the city begins on '{task[0].capitalize()}'")
    else:
        c.execute(f"select name from cities where name = '{city}'")
        town = c.fetchone()
        if town is None:
            await bot.send_message(id, text=f"There is no {city} city or it's too unpopular. Try again")
        else:
            town = town[0]
            if town in named:
                await bot.send_message(id, text=f"There already was {town} city in this game. Send another")
            else:
                named.append(town)
                nl = town[-1].capitalize()
                c.execute(f"select name from cities where name like('{nl}%')")
                next = c.fetchone()[0]
                while next in named:
                    next = c.fetchone()[0]
                named.append(next)
                await bot.send_message(id, text=f"{next} \n {next[-1].capitalize()}")
                await state.update_data(name=next, named=named)

executor.start_polling(dp, skip_updates=True)
