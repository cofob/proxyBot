import os

from telethon import TelegramClient, Button
from os import environ
import logging
import teleshell
import gettext
import models
import secrets
import pickle
import requests
import settings
from Light_Qiwi import Qiwi
import time
import shutil
from datetime import datetime


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

langs = {}


def lang_init(l='en'):
    path = './locale'
    lang = gettext.translation('bot', path, [l])
    return lang.gettext


def init():
    for lang in settings.langs:
        langs[lang] = lang_init(l=lang)


def _(text, l='ru'):
    return langs[l](text)


try:
    shutil.rmtree('temp')
except:
    pass
os.mkdir('temp')


init()

client = TelegramClient('bot', int(environ['API_ID']), environ['API_HASH']).start(bot_token=environ['BOT_TOKEN'])

try:
    api = Qiwi(pickle.loads(models.Setting.get(name='qiwi_token').value), settings.qiwi_phone)
except:
    pass


def to_datetime(ts, format='%Y-%m-%d %H:%M:%S'):
    return datetime.utcfromtimestamp(ts).strftime(format)


def to_curr_datetime(ts):
    days = int(ts/86400)
    hours = int(ts/3600)
    return f'{days}d {hours}h'


async def before_invoke(event):
    user = models.User.get_or_none(user_id=event.chat_id)
    chat = await event.get_chat()
    if not user:
        user = models.User(user_id=event.chat_id)
    user.username = chat.username
    user.firstname = chat.first_name
    user.lastname = chat.last_name
    user.save()
    return user


def get_proxy(countries: str = 'all', types: str = 'all', level: str = 'all', speed: str = '0', count: str = '0'):
    r = requests.get(f'https://proxoid.net/api/getProxy?key={pickle.loads(models.Setting.get(name="proxoid").value)}'
                     f'&countries={countries}&types={types}&level={level}&speed={speed}&count={count}')
    name = secrets.token_urlsafe(16)
    path = f'temp/{name}.txt'
    with open(path, 'w') as file:
        file.write(r.text)
    return path


def get_proxy_count(countries: str = 'all', types: str = 'all', level: str = 'all', speed: str = '0', count: str = '0'):
    r = requests.get(f'https://proxoid.net/api/getProxy?key={pickle.loads(models.Setting.get(name="proxoid").value)}'
                     f'&countries={countries}&types={types}&level={level}&speed={speed}&count={count}&getCount=1')
    return r.text


shell = teleshell.ClientShell(client=client, message_first=before_invoke)
handle = shell.handle
button = shell.button


async def start(event, first=None):
    markup = client.build_reply_markup([[Button.text(_('Profile', first.lang), resize=True),
                                        Button.text(_('Proxy', first.lang), resize=True)],
                                        [Button.text(_('Help', first.lang), resize=True)]])
    await event.reply(_('start_text', first.lang), buttons=markup)


async def help(event, first=None):
    markup = client.build_reply_markup([
        [
            Button.text(_('Menu', first.lang), resize=True)
        ]
    ])
    await event.reply(_('help_text', first.lang), buttons=markup)


async def menu(event, first=None):
    first.action = ''
    first.data = None
    first.save()
    markup = client.build_reply_markup([[Button.text(_('Profile', first.lang), resize=True),
                                       Button.text(_('Proxy', first.lang), resize=True)],
                                        [Button.text(_('Buy', first.lang), resize=True)]])
    await client.send_message(first.user_id, _('menu_text', first.lang), buttons=markup)


async def profile(event, first=None):
    markup = client.build_reply_markup([
        [
            Button.text(_('API', first.lang), resize=True)
        ],
        [
            Button.text(_('Top up balance', first.lang), resize=True)
        ],
        [
            Button.text(_('Menu', first.lang), resize=True),
        ]
    ])
    await event.reply(_('profile_text', first.lang).format(
        id=first.user_id, balance=first.balance,
        ends=to_datetime(first.subscription) if first.subscription > time.time() else _('No', first.lang),
        register=to_datetime(first.register_timestamp)), buttons=markup)


async def proxy(event, first=None):
    if first.subscription < time.time():
        return await event.reply(_('subscription_end', first.lang))
    markup = client.build_reply_markup([
        [Button.text(_('HTTP', first.lang), resize=True),
        Button.text(_('HTTPS', first.lang), resize=True)],
        [Button.text(_('SOCKS4', first.lang), resize=True),
         Button.text(_('SOCKS5', first.lang), resize=True)],
        [Button.text(_('Done', first.lang), resize=True)],
        [Button.text(_('Menu', first.lang), resize=True)]
    ])
    first.action = 'proxy_type'
    first.data = pickle.dumps({})
    first.save()
    await event.reply(_('proxy_type_text', first.lang).format(types=_('all', first.lang)), buttons=markup)


async def proxy_type(event, first=None):
    if first.subscription < time.time():
        return await event.reply(_('subscription_end', first.lang))
    data = pickle.loads(first.data)
    data['types'] = data.get('types', [])
    t = event.text.lower()
    if t in data['types']:
        data['types'].remove(t)
    else:
        data['types'].append(t)
    first.data = pickle.dumps(data)
    first.save()
    types_text = ', '.join(data['types']) if data['types'] and len(data['types']) < 4 else _('all', first.lang)
    await event.reply(_('proxy_type_text', first.lang).format(types=types_text))


async def proxy_anonymous(event, first=None):
    if first.subscription < time.time():
        return await event.reply(_('subscription_end', first.lang))
    data = pickle.loads(first.data)
    data['anonymous'] = data.get('anonymous', [])
    t = event.text.lower()
    if t in data['anonymous']:
        data['anonymous'].remove(t)
    else:
        data['anonymous'].append(t)
    first.data = pickle.dumps(data)
    first.save()
    anonymous_text = ', '.join(data['anonymous']) if data['anonymous'] and len(data['anonymous']) < 3\
        else _('all', first.lang)
    await event.reply(_('proxy_anonymous_text', first.lang).format(anonymous=anonymous_text))


async def _api(event, first=None):
    markup = client.build_reply_markup([
        [Button.text(_('Generate token', first.lang), resize=True)],
        [Button.text(_('Menu', first.lang), resize=True)]
    ])
    await event.reply(_('api_text', first.lang)
                      .format(token=first.token if first.token else _('No', first.lang)), buttons=markup)


async def generate_token(event, first=None):
    markup = client.build_reply_markup([Button.text(_('Profile', first.lang), resize=True),
                                        Button.text(_('Proxy', first.lang), resize=True)])
    first.token = secrets.token_urlsafe(24)
    first.save()
    await event.reply(_('generated_token_text', first.lang).format(token=first.token), buttons=markup)


async def top_up_balance(event, first=None):
    markup = client.build_reply_markup([[Button.text(_('QIWI', first.lang), resize=True)],
                                        [Button.text(_('Menu', first.lang), resize=True)]])
    await event.reply(_('top_up_balance_text', first.lang), buttons=markup)


async def top_up_balance_qiwi(event, first=None):
    markup = client.build_reply_markup([[Button.text(_('Cancel', first.lang), resize=True)]])
    await event.reply(_('top_up_balance_qiwi_text', first.lang).format(link=f'https://qiwi.com/payment/'
                                                                            f'form/99?extra[%27account%27]='
                                                                            f'{settings.qiwi_phone}&currency=643&extra'
                                                                            f'[%27comment%27]={first.user_id}'),
                                                                       buttons=markup)


async def cancel(event, first=None):
    first.action = ''
    first.data = None
    first.save()
    await event.reply(_('canceled_text', first.lang))
    await menu(event, first)


async def did_not_understand(event, first=None):
    first.action = ''
    first.data = None
    first.save()
    await event.reply(_('did_not_understand', first.lang))


async def success(event, first=None):
    first.data = None
    first.action = None
    first.save()


async def buy(event, first=None):
    await event.reply(_('tariffs', first.lang))
    tariffs = models.Tariff.select()
    for tariff in tariffs:
        markup = client.build_reply_markup([Button.inline(_('Buy', first.lang), f'buy_{tariff.id}'.encode())])
        await client.send_message(first.user_id, _('tariff_detailed', first.lang).format(
            name=tariff.name,
            description=tariff.description,
            time=to_curr_datetime(tariff.add_time),
            price=tariff.price
        ), buttons=markup)
    await client.send_message(first.user_id, _('select_tariff', first.lang))


async def _exit(event, first=None):
    if first.user_id != settings.owner:
        return await event.reply(_('owner_only', first.lang))
    await exit(0)


async def _set(event, first=None):
    if first.user_id != settings.owner:
        return await event.reply(_('owner_only', first.lang))
    first.action = 'set_name'
    first.data = pickle.dumps({})
    first.save()
    await event.reply(_('set_name', first.lang))


async def add_balance(event, first=None):
    if first.user_id != settings.owner:
        return await event.reply(_('owner_only', first.lang))
    first.action = 'add_balance_id'
    first.data = pickle.dumps({})
    first.save()
    await event.reply(_('add_balance_id', first.lang))


async def add_tariff(event, first=None):
    if first.user_id != settings.owner:
        return await event.reply(_('owner_only', first.lang))
    first.action = 'add_tariff_name'
    first.data = pickle.dumps({})
    first.save()
    await event.reply(_('add_tariff_name', first.lang))


async def text(event, first=None):
    if first.action == 'add_balance_id':
        data = pickle.loads(first.data)
        data['id'] = int(event.text)
        first.data = pickle.dumps(data)
        first.action = 'add_balance_value'
        first.save()
        await event.reply(_('add_balance_value', first.lang))
    elif first.action == 'add_balance_value':
        data = pickle.loads(first.data)
        data['value'] = float(event.text)
        first.data = None
        first.action = None
        first.save()
        t = models.User.get(user_id=data['id'])
        t.balance += data['value']
        t.save()
        await event.reply(_('add_balance_done', first.lang))
    elif first.action == 'set_name':
        data = pickle.loads(first.data)
        data['name'] = event.text
        first.data = pickle.dumps(data)
        first.action = 'set_value'
        first.save()
        await event.reply(_('set_value', first.lang))
    elif first.action == 'set_value':
        data = pickle.loads(first.data)
        data['value'] = event.text
        first.data = None
        first.action = None
        first.save()
        t = models.Setting.get_or_none(name=data['name'])
        if not t:
            t = models.Setting(name=data['name'])
        t.value = pickle.dumps(data['value'])
        t.save()
        await event.reply(_('set_done', first.lang))
    elif first.action == 'add_tariff_name':
        data = pickle.loads(first.data)
        data['name'] = event.text
        first.data = pickle.dumps(data)
        first.action = 'add_tariff_description'
        first.save()
        await event.reply(_('add_tariff_description', first.lang))
    elif first.action == 'add_tariff_description':
        data = pickle.loads(first.data)
        data['description'] = event.text
        first.data = pickle.dumps(data)
        first.action = 'add_tariff_time'
        first.save()
        await event.reply(_('add_tariff_time', first.lang))
    elif first.action == 'add_tariff_time':
        data = pickle.loads(first.data)
        data['time'] = event.text
        first.data = pickle.dumps(data)
        first.action = 'add_tariff_price'
        first.save()
        await event.reply(_('add_tariff_price', first.lang))
    elif first.action == 'add_tariff_price':
        data = pickle.loads(first.data)
        data['price'] = event.text
        first.data = None
        first.action = None
        first.save()
        t = models.Tariff(
            name=data['name'],
            description=data['description'],
            add_time=data['time'],
            price=data['price']
        )
        t.save()
        await event.reply(_('add_tariff_done', first.lang))
    elif first.action == 'proxy_type' and event.text == _('Done', first.lang):
        first.action = 'proxy_anonymous'
        data = pickle.loads(first.data)
        data['types'] = data.get('types', [])
        if len(data['types']) == 0:
            data['types'] = 'all'
        else:
            data['types'] = ','.join(data['types'])
        first.data = pickle.dumps(data)
        first.save()
        markup = client.build_reply_markup([
            [Button.text(_('Transparent', first.lang), resize=True),
             Button.text(_('Anonymous', first.lang), resize=True)],
            [Button.text(_('Elite', first.lang), resize=True)],
            [Button.text(_('Done', first.lang), resize=True)],
            [Button.text(_('Menu', first.lang), resize=True)]
        ])
        await event.reply(_('proxy_anonymous_text', first.lang).format(anonymous=_('all', first.lang)), buttons=markup)
    elif first.action == 'proxy_anonymous' and event.text == _('Done', first.lang):
        first.action = 'proxy_country'
        data = pickle.loads(first.data)
        data['anonymous'] = data.get('anonymous', [])
        if len(data['anonymous']) == 0:
            data['anonymous'] = 'all'
        else:
            data['anonymous'] = ','.join(data['anonymous'])\
                .replace(_('Elite', first.lang).lower(), 'high')\
                .replace(_('Anonymous', first.lang).lower(), 'anonymous')\
                .replace(_('Transparent', first.lang).lower(), 'transparent')
        first.data = pickle.dumps(data)
        first.save()
        markup = client.build_reply_markup([[Button.text(_('Done', first.lang), resize=True)],
                                            [Button.text(_('Menu', first.lang), resize=True)]])
        await event.reply(_('proxy_country_text', first.lang).format(countries=_('all', first.lang)), buttons=markup)
    elif first.action == 'proxy_count':
        data = pickle.loads(first.data)
        data['count'] = data.get('count', 0)
        if event.text == _('Done', first.lang):
            first.data = pickle.dumps(data)
            first.action = 'proxy_speed'
            first.save()
            await event.reply(_('proxy_speed', first.lang).format(speed=_('all', first.lang)))
        else:
            try:
                i = int(event.text)
                if i < 0:
                    raise ValueError
                data['count'] = i
                first.data = pickle.dumps(data)
                first.action = 'proxy_speed'
                first.save()
                await event.reply(_('proxy_speed', first.lang).format(speed=_('all', first.lang)))
            except ValueError:
                await event.reply(_('value_error', first.lang))
    elif first.action == 'proxy_speed':
        if first.subscription < time.time():
            return await event.reply(_('subscription_end', first.lang))
        data = pickle.loads(first.data)
        data['speed'] = data.get('speed', 0)
        if event.text == _('Done', first.lang):
            first.data = None
            first.action = None
            first.save()
            path = get_proxy(data['country'], data['types'], data['anonymous'], data['speed'], data['count'])
            await event.reply(_('proxy_done', first.lang))
            await client.send_file(first.user_id, path)
            os.remove(path)
            await menu(event, first)
        else:
            try:
                i = int(event.text)
                if i < 0:
                    raise ValueError
                data['speed'] = i
                first.data = None
                first.action = None
                first.save()
                print(data)
                await event.reply(_('proxy_done', first.lang))
                await menu(event, first)
            except ValueError:
                await event.reply(_('value_error', first.lang))
    elif first.action == 'proxy_country':
        data = pickle.loads(first.data)
        data['country'] = data.get('country', [])
        if event.text == _('Done', first.lang):
            if len(data['country']) == 0:
                data['country'] = 'all'
            else:
                data['country'] = ','.join(data['country'])
            first.data = pickle.dumps(data)
            first.action = 'proxy_count'
            first.save()

            markup = client.build_reply_markup([[Button.text(_('Done', first.lang), resize=True)],
                                                [Button.text(_('Menu', first.lang), resize=True)]])
            count = get_proxy_count(data['country'], data['types'], data['anonymous'])
            await event.reply(_('proxy_count_text', first.lang).format(count=count, buttons=markup))
        elif event.text.upper() in settings.countries:
            t = event.text.lower()
            if t in data['country']:
                data['country'].remove(t)
            else:
                data['country'].append(t)
            first.data = pickle.dumps(data)
            first.save()
            country_text = ', '.join(data['country']) if \
                data['country'] and len(data['country']) < len(settings.countries) else _('all', first.lang)
            await event.reply(_('proxy_country_text', first.lang).format(countries=country_text))
        else:
            await event.reply(_('not_found', first.lang))
    else:
        await event.reply(_('did_not_understand', first.lang))


def add_text_handler(func, name):
    for lang in settings.langs:
        handle(text=_(name, lang))(func)


def add_command_handler(func, name):
    for lang in settings.langs:
        handle(command=_(name, lang))(func)


@button(command=b'buy_')
async def buy_inline(event):
    await event.answer()
    user = models.User.get(user_id=event.original_update.user_id)
    data = int(event.data.decode().replace('buy_', ''))
    product = models.Tariff.get_by_id(data)
    if product.price > user.balance:
        return await event.respond(_('not_enough_balance', user.lang))
    user.balance -= product.price
    if user.subscription <= time.time():
        user.subscription = time.time()
    user.subscription += product.add_time
    user.save()
    await event.respond(_('buyed', user.lang))


try:
    @api.bind_check()
    def receive(payment):
        amount = payment.amount
        comment = payment.comment
        user = models.User.get(user_id=comment)
        user.balance += amount
        user.save()
except NameError:
    pass


# ADD HANDLERS
add_command_handler(cancel, 'cancel')
add_command_handler(start, 'start')
add_command_handler(help, 'help')
add_command_handler(menu, 'menu')
add_command_handler(_set, 'set')
add_command_handler(_exit, 'exit')
add_command_handler(add_tariff, 'add_tariff')
add_command_handler(add_balance, 'add_balance')
add_text_handler(cancel, 'Cancel')
add_text_handler(profile, 'Profile')
add_text_handler(menu, 'Menu')
add_text_handler(proxy, 'Proxy')
add_text_handler(proxy_type, 'HTTP')
add_text_handler(proxy_type, 'HTTPS')
add_text_handler(proxy_type, 'SOCKS4')
add_text_handler(proxy_type, 'SOCKS5')
add_text_handler(proxy_anonymous, 'Elite')
add_text_handler(proxy_anonymous, 'Transparent')
add_text_handler(proxy_anonymous, 'Anonymous')
add_text_handler(top_up_balance, 'Top up balance')
add_text_handler(top_up_balance_qiwi, 'QIWI')
add_text_handler(buy, 'Buy')
add_text_handler(_api, 'API')
add_text_handler(generate_token, 'Generate token')
handle()(text)


try:
    api.start_threading()
except NameError:
    pass

client.start()
client.run_until_disconnected()
