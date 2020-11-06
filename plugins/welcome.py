from settings import bot,db,bot_id,logs
import utils


async def welcome(msg):
    if msg.get('new_chat_member'):
        if msg['new_chat_member']['id'] == bot_id:
            await bot.sendMessage(msg['chat']['id'], 'Olá pessoal do {}, eu sou o Droidshell!'.format(msg['chat']['title']))
            bot.sendMessage(logs, '''
            O bot foi adicionado em um novo grupo!

            Nome do grupo: {}
            ID do grupo: {}
            
            '''.format(msg['chat']['title'], msg['chat']['id']))
        else:
            welcome = 'Olá *{}*, seja bem-vindo(a) ao *{}*!'.format(msg['new_chat_member']['first_name'], utils.escape_markdown(msg['chat']['title']))

            await bot.sendMessage(msg['chat']['id'], welcome, parse_mode='Markdown', reply_to_message_id=msg['message_id'])

    elif msg.get('left_chat_member'):
        await bot.sendMessage(msg['chat']['id'], 'Tchau {}'.format(msg['left_chat_member']['first_name']), reply_to_message_id=msg['message_id'])



