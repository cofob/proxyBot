def add(name: str, description: str = ''):
    with open('env.sh', 'a+') as file:
        file.write(f'export {name}='+input(f'{name}:\n\t' +
                                        (f'description: {description}\n\t' if description else '')
                                        + 'value: ') + '\n')


f = open('env.sh', 'w')
f.close()

add('API_ID', 'api_id from my.telegram.org app page')
add('API_HASH', 'api_hash from my.telegram.org app page')
add('OWNER_ID', 'bot owner telegram id, from @userinfobot')
add('BOT_TOKEN', 'bot token from @botfather')
