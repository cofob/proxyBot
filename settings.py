from os import environ
import models
import pickle

try:
    qiwi_phone = pickle.loads(models.Setting.get(name='qiwi_phone').value)
except:
    pass
owner = int(environ['OWNER_ID'])
countries = ['AF', 'AX', 'IR', 'HR', 'BA', 'MD', 'RS', 'MK', 'ZA', 'MU', 'LY', 'AL', 'DZ', 'AS', 'AD', 'AO',
             'AI', 'AQ', 'AG', 'AR', 'AM', 'AW', 'AU', 'AT', 'AZ', 'BS', 'BH', 'BD', 'BB', 'BY', 'BE', 'BZ',
             'BJ', 'BM', 'BT', 'BO', 'BW', 'BV', 'BR', 'BN', 'BG', 'BF', 'BI', 'KH', 'CM', 'CA', 'CV', 'KY',
             'TD', 'CL', 'CN', 'CX', 'CO', 'KM', 'CK', 'CR', 'CI', 'CU', 'CY', 'CZ', 'DK', 'DJ', 'DM', 'DO',
             'EC', 'EG', 'SV', 'GQ', 'ER', 'EE', 'ET', 'FO', 'FJ', 'FI', 'FR', 'GA', 'GM', 'GE', 'DE', 'GH',
             'GI', 'GR', 'GL', 'GD', 'GP', 'GU', 'GT', 'GN', 'GW', 'GY', 'HT', 'HN', 'HK', 'HU', 'IS', 'IN',
             'ID', 'IQ', 'IE', 'IL', 'IT', 'JM', 'JP', 'JO', 'KZ', 'KE', 'KI', 'KW', 'KG', 'LV', 'LB', 'LS',
             'LR', 'LI', 'LT', 'LU', 'MO', 'MG', 'MW', 'MY', 'MV', 'ML', 'MT', 'MH', 'MQ', 'MR', 'MU', 'YT',
             'MX', 'MC', 'MN', 'MS', 'MA', 'MZ', 'MM', 'NA', 'NR', 'NP', 'NL', 'AN', 'NC', 'NZ', 'NI', 'NE',
             'NG', 'NU', 'NO', 'OM', 'PK', 'PW', 'PA', 'PG', 'PY', 'PE', 'PH', 'PN', 'PL', 'PT', 'PR', 'QA',
             'RE', 'RO', 'RU', 'RW', 'SH', 'KN', 'LC', 'WS', 'SM', 'SA', 'SN', 'SC', 'SL', 'SG', 'SK', 'SI',
             'SB', 'SO', 'ZA', 'ES', 'LK', 'SD', 'SR', 'SJ', 'SZ', 'SE', 'CH', 'SY', 'TW', 'TJ', 'TH', 'TL',
             'TG', 'TK', 'TO', 'TN', 'TR', 'TM', 'TV', 'UG', 'UA', 'AE', 'GB', 'US', 'UY', 'UZ', 'VU', 'VE',
             'VN', 'EH', 'YE', 'ZM', 'ZW']
langs = ['ru']
