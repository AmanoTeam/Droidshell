from settings import bot, version,bot_username
import keyboard
async def start(msg):
    if msg.get('text'):
        if msg['text'] == '/start' or msg['text'] == '!start' or msg['text'].split()[0] == '/start@' + bot_username or msg['text'] == '/start start':
            await bot.sendMessage(msg['chat']['id'], 'Olá, eu sou o Droidshell, para saber meus comandos, clique no botão abaixo.', reply_markup=keyboard.keyboard)

    elif msg.get('data'):
        data = msg['data']
        chat_idf = (msg['message']['chat']['id'], msg['message']['message_id'])

        if data == 'comandos':
            await bot.editMessageText(chat_idf, '''
            Comandos:
            
            - /ping
            - /extras
            - /start
            - /tr
            - rt
            
            ''', reply_markup=keyboard.back)

        if data == 'infos':
            await bot.editMessageText(chat_idf, '''
            
<b>Droidshell</b>

Versão: <i>{}</i>

Desenvolvedores:
<a href="tg://user?id=337730276">Ant2br</a>
<a href="tg://user?id=200097591">Alisson</a>

        '''.format(version), reply_markup=keyboard.back, parse_mode='HTML')

        if data == 'home':
            await bot.editMessageText(chat_idf, 'Olá, eu sou o Droidshell, para saber meus comandos, clique no botão abaixo.',
                                reply_markup=keyboard.keyboard)