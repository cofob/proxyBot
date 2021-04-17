import os
import pickle

try:
    os.remove('database.db')
    os.remove('env.sh')
except:
    pass

import models

os.system('msgfmt locale/ru/LC_MESSAGES/bot.po -o locale/ru/LC_MESSAGES/bot.mo')


def add(name: str, description: str = ''):
    with open('env.sh', 'a+') as file:
        file.write(f'export {name}='+input(f'{name}:\n\t' +
                                        (f'description: {description}\n\t' if description else '')
                                        + 'value: ') + '\n')


def add_to_db(name: str, description: str = ''):
    value = input(f'{name}:\n\t' + (f'description: {description}\n\t' if description else '') + 'value: ')
    m = models.Setting()
    m.name = name
    m.value = pickle.dumps(value)
    m.save()


add_to_db('qiwi_token', 'token from https://qiwi.com/api')
add_to_db('qiwi_phone', 'phone number from qiwi')
add('API_ID', 'api_id from https://my.telegram.org app page')
add('API_HASH', 'api_hash from https://my.telegram.org app page')
add('OWNER_ID', 'bot owner telegram id, from @userinfobot')
add('BOT_TOKEN', 'bot token from @botfather')
