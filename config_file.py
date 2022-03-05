telegram_token = '5150738275:AAHM4tvi8_6LbB45A2RkORQBbl-unuarO9U'  # Бота создавать через @Botfather
start_text = '''
    This is a multifunctional bot \t
    It's a part of my portfolio \t
    To hire me, please write in \t
    tg: @ategran \n
    
    You can use these commands to control this bot: \n
    /start \t
    /help \t
    /pets - to see random image \t
    /game - to play a game \t
    /cities - test your erudition
    '''
rules = '''Make clicks to earn points. You can use your points to buy items of various rarities. To increase the 
number of points, you can play the lottery. But be careful, you can lose '''
city_rules = '''
Rules are very simple. Bot Sends you a name of the city and your task is to send a name of the city witch begins of the 
last letter of the previous city. 
'''
actions = {'Play🔥': 'game', 'Lottery🍀': 'lottery', 'Shop💰': 'shop',
            'Leaderboard🏆': 'leaderboard', 'My collection🧸': 'collection', 'Back🚪': 'back'}
lottery_text = '''
Test your luck in the lottery! \n
Here you can easy earn, but easy lose your clicks. \n
The rules are simple - you send the number and if it hits the correct area, you take prise. \n
There are two modes: \n
In the first one the area is 50/100 and the winning case double your bet.
To play you need at least 20 points on your balance. \n
In the second mode the area is 25/100, the prise is 4x! To play you need at least 40 points on your balance. \n
Good luck ;) 
'''
path_to_dir = '/Users/ategran/PycharmProjects/pythonProject2/pictures'
open_pic = {'Common': 'https://disk.yandex.ru/i/lSRjFMd4jyhFZA', 'Rare': 'https://disk.yandex.ru/i/lU402PH_tRw1xg',
            'Epic': 'https://disk.yandex.ru/i/G2_vrhWxnWT9Ug'}