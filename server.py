from flask import Flask
from flask import request
import models
import requests
import pickle
from time import time

app = Flask(__name__)
proxy_types = ['http', 'https', 'socks4', 'socks5']
countries = ['russia', 'usa', 'ukraine', 'germany', 'china', 'belgia']


def get_proxy(countries=None, types=None, level=None, speed=None, count=None):
    if not countries:
        countries = 'all'
    if not types:
        types = 'all'
    if not level:
        level = 'all'
    if not speed:
        speed = 0
    if not count:
        count = 0
    r = requests.get(f'https://proxoid.net/api/getProxy?key={pickle.loads(models.Setting.get(name="proxoid").value)}'
                     f'&countries={countries.upper()}&types={types.lower()}&level={level.lower()}'
                     f'&speed={speed}&count={count}')
    return r.text


@app.route('/api/<token>/proxy/')
def proxy(token):
    user = models.User.get_or_none(token=token)
    ans = None
    if not user:
        ans = 'Неверный запрос!'
    if user.subscription < time():
        ans = 'Подписка закончилась!'
    country = request.args.get('country')
    types = request.args.get('types')
    level = request.args.get('level')
    speed = request.args.get('speed')
    count = request.args.get('count')
    if ans is None:
        ans = get_proxy(countries=country, types=types, level=level, speed=speed, count=count)
    return ans


app.run()
