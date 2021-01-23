from settings import bot,version,db,isAdmin,bot_username
import re, time, requests, json
from datetime import date

async def ferramentas(msg):
    if msg.get('text'):
        if msg['text'] == '/info' or msg['text'] == '!info' or msg['text'].split()[0] == '/info@' + bot_username:
            await bot.sendMessage(msg['chat']['id'],'''
            <b>Droidshell</b>

Versão: <i>{}</i>

Desenvolvedores:
<a href="tg://user?id=337730276">Ant2br</a>
<a href="tg://user?id=200097591">Alisson</a>
            '''.format(version),parse_mode='HTML')

        elif msg['text'].lower() == 'rt' and msg.get('reply_to_message'):
            if msg['reply_to_message'].get('text'):
                text = msg['reply_to_message']['text']
            elif msg['reply_to_message'].get('caption'):
                text = msg['reply_to_message']['caption']
            else:
                text = None
            if text:
                if text.lower() != 'rt':
                    if not re.match('🔃 .* retweetou:\n\n👤 .*', text):
                        await bot.sendMessage(msg['chat']['id'], '''🔃 <b>{}</b> retweetou:

        👤 <b>{}</b>: <i>{}</i>'''.format(msg['from']['first_name'], msg['reply_to_message']['from']['first_name'],
                                          text),
                                              parse_mode='HTML',
                                              reply_to_message_id=msg['message_id'])
                return True

        elif msg['text'] == '/ping' or msg['text'] == '!ping':
            first = time.time()
            sent = await bot.sendMessage(msg['chat']['id'], '*Pong!*', 'Markdown',
                                         reply_to_message_id=msg['message_id'])
            second = time.time()
            await bot.editMessageText((msg['chat']['id'], sent['message_id']), '*Pong!* `{}`s'.format(str(second - first)[:5]), 'Markdown')
            return True
        elif msg['text'] == '/cotacao':
            url = "https://api.hgbrasil.com/finance?formt=json"

            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)
            result = json.loads(response.text)
            dolar = float(result["results"]["currencies"]["USD"]["buy"])
            euro = float(result["results"]["currencies"]["EUR"]["buy"])
            dolarf = truncate(dolar, 2)
            eurof = truncate(euro, 2)
            
            data_atual = date.today()
            data_em_texto = data_atual.strftime('%d/%m/%Y')
            
            await bot.sendMessage(msg['chat']['id'], '''
<b>Cotação Atualizada {}</b>
<b> 💵 Dolar: </b> <i>{}</i>
<b> 💶 Euro: </b> <i>{}</i>
            '''.format(data_em_texto,dolarf, eurof),parse_mode='HTML',
                                         reply_to_message_id=msg['message_id'])


def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])


