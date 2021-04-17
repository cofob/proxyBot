from os import environ
import models
import pickle

try:
    qiwi_phone = pickle.loads(models.Setting.get(name='qiwi_phone').value)
except:
    pass
owner = int(environ['OWNER_ID'])
countries = ['Russia', 'USA', 'Ukraine', 'Germany', 'China', 'Belgia']
langs = ['ru']
