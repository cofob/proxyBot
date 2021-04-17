from flask import Flask
import json
import models
from time import time

app = Flask(__name__)
proxy_types = ['http', 'https', 'socks4', 'socks5']
countries = ['russia', 'usa', 'ukraine', 'germany', 'china', 'belgia']


@app.route('/api/<token>/proxy/')
def proxy(token):
    user = models.User.get_or_none(token=token)
    if not user:
        ret = {'error': 2, 'description': 'User does not exist or bad token'}
        return json.dumps(ret)
    if user.subscription < time():
        ret = {'error': 3, 'description': 'Renew subscription'}
        return json.dumps(ret)
    ret = {
        'success': True,
        'data': [
            {
                'type': proxy_type,
                'host': '0.0.0.0',
                'port': 1234,
                'country': 'russia'
            }
        ]
    }
    return json.dumps(ret)


@app.route('/api/<token>/proxy/<proxy_type>')
def proxy_type(token, proxy_type):
    user = models.User.get_or_none(token=token)
    if not user:
        ret = {'error': 2, 'description': 'User does not exist or bad token'}
        return json.dumps(ret)
    if user.subscription < time():
        ret = {'error': 3, 'description': 'Renew subscription'}
        return json.dumps(ret)
    if proxy_type not in proxy_types:
        ret = {'error': 1, 'description': 'Unknown proxy protocol'}
        return json.dumps(ret)
    ret = {
        'success': True,
        'data': [
            {
                'type': proxy_type,
                'host': '0.0.0.0',
                'port': 1234,
                'country': 'russia'
            }
        ]
    }
    return json.dumps(ret)


@app.route('/api/<token>/proxy/<proxy_type>/<country>')
def proxy_type_country(token, proxy_type, country):
    user = models.User.get_or_none(token=token)
    if not user:
        ret = {'error': 2, 'description': 'User does not exist or bad token'}
        return json.dumps(ret)
    if user.subscription < time():
        ret = {'error': 3, 'description': 'Renew subscription'}
        return json.dumps(ret)
    if proxy_type not in proxy_types:
        ret = {'error': 1, 'description': 'Unknown proxy protocol'}
        return json.dumps(ret)
    if country not in countries:
        ret = {'error': 3, 'description': 'Unknown country'}
        return json.dumps(ret)
    ret = {
        'success': True,
        'data': [
            {
                'type': proxy_type,
                'host': '0.0.0.0',
                'port': 1234,
                'country': 'russia'
            }
        ]
    }
    return json.dumps(ret)


app.run()
