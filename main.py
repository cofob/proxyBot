from telethon import TelegramClient, Button
from os import environ
import logging
import teleshell
import gettext
import models
import secrets
import pickle
import settings


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

langs = {}


def lang_init(l='en'):
    path = './locale'
    lang = gettext.translation('bot', path, [l])
    return lang.gettext


def init():
    for lang in ['ru']:
        langs[lang] = lang_init(l=lang)


def _(text, l='ru'):
    return langs[l](text)


init()

client = TelegramClient('bot', int(environ['API_ID']), environ['API_HASH']).start(bot_token=environ['BOT_TOKEN'])


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


shell = teleshell.ClientShell(client=client, message_first=before_invoke)
handle = shell.handle


@handle(command='start')
async def start(event, first=None):
    markup = client.build_reply_markup([Button.text(_('Profile', first.lang), resize=True),
                                        Button.text(_('Proxy', first.lang), resize=True)],
                                        [Button.text(_('Help', first.lang), resize=True)])
    await event.reply(_('start_text', first.lang), buttons=markup)


@handle(command='help')
async def help(event, first=None):
    markup = client.build_reply_markup([
        [
            Button.text(_('Menu', first.lang), resize=True)
        ]
    ])
    await event.reply(_('help_text', first.lang), buttons=markup)


@handle(command='menu')
async def menu(event, first=None):
    markup = client.build_reply_markup([Button.text(_('Profile', first.lang), resize=True),
                                       Button.text(_('Proxy', first.lang), resize=True)])
    await event.reply(_('menu_text', first.lang), buttons=markup)


@handle(text='Профиль')
async def profile(event, first=None):
    markup = client.build_reply_markup([
        [
            Button.text(_('API', first.lang), resize=True)
        ],
        [
            Button.text(_('Menu', first.lang), resize=True),
        ]
    ])
    await event.reply(_('profile_text', first.lang).format(
        id=first.user_id, balance=first.balance,
        ends=first.subscription, register=first.register_timestamp), buttons=markup)


@handle(text='Меню')
async def menu(event, first=None):
    markup = client.build_reply_markup([Button.text(_('Profile', first.lang), resize=True),
                                        Button.text(_('Proxy', first.lang), resize=True)])
    await event.reply(_('menu_text', first.lang), buttons=markup)


@handle(text='Прокси')
async def proxy(event, first=None):
    markup = client.build_reply_markup([
        [Button.text(_('HTTP', first.lang), resize=True),
        Button.text(_('HTTPS', first.lang), resize=True)],
        [Button.text(_('SOCKS4', first.lang), resize=True),
         Button.text(_('SOCKS5', first.lang), resize=True)],
        [Button.text(_('Menu', first.lang), resize=True)]
    ])
    await event.reply(_('proxy_text', first.lang), buttons=markup)


@handle(text='HTTP')
@handle(text='HTTPS')
@handle(text='SOCKS4')
@handle(text='SOCKS5')
async def proxy(event, first=None):
    first.action = 'proxy_country'
    first.data = pickle.dumps(event.text.lower())
    first.save()
    markup = client.build_reply_markup([[Button.text(settings.countries[i], resize=True),
                                         Button.text(settings.countries[i+1], resize=True)]
                                        for i in range(0, len(settings.countries), 2)] +
                                       [[Button.text(_('Menu', first.lang), resize=True)]])
    await event.reply(_('proxy_country_text', first.lang), buttons=markup)


@handle(text='API')
async def api(event, first=None):
    markup = client.build_reply_markup([
        [Button.text(_('Generate token', first.lang), resize=True)],
        [Button.text(_('Menu', first.lang), resize=True)]
    ])
    await event.reply(_('api_text', first.lang)
                      .format(token=first.token if first.token else _('No', first.lang)), buttons=markup)


@handle(text='Выпустить токен')
async def generate_token(event, first=None):
    markup = client.build_reply_markup([Button.text(_('Profile', first.lang), resize=True),
                                        Button.text(_('Proxy', first.lang), resize=True)])
    first.token = secrets.token_urlsafe(16)
    first.save()
    await event.reply(_('generated_token_text', first.lang).format(token=first.token), buttons=markup)


client.start()
client.run_until_disconnected()
