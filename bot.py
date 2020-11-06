from settings import version
print(r'''
 ____            _     _     _          _ _
|  _ \ _ __ ___ (_) __| |___| |__   ___| | |
| | | | '__/ _ \| |/ _` / __| '_ \ / _ \ | |
| |_| | | | (_) | | (_| \__ \ | | |  __/ | |
|____/|_|  \___/|_|\__,_|___/_| |_|\___|_|_|
                                       v{}
Iniciando...              
'''.format(version))


import asyncio
import json
import html
import traceback
import amanobot.aio

from amanobot.exception import TelegramError, TooManyRequestsError, NotEnoughRightsError
from amanobot.aio.loop import MessageLoop
from colorama import Fore
from urllib3.exceptions import ReadTimeoutError
from settings import bot, na_bot, enabled_plugins, logs, backups_chat
from utils import send_to_dogbin

ep = []
n_ep = []

for num, i in enumerate(enabled_plugins):
    try:
        print(Fore.RESET + 'Carregando plugins... [{}/{}]'.format(num + 1, len(enabled_plugins)), end='\r')
        exec('from plugins.{0} import {0}'.format(i))
        ep.append(i)
    except Exception as erro:
        n_ep.append(i)
        print('\n' + Fore.RED + 'Erro ao carregar o plugin {}:{}'.format(i, Fore.RESET), erro)


async def handle(msg):
    for plugin in ep:
        try:
            p = await globals()[plugin](msg)
            if p:
                break
        except (TooManyRequestsError, NotEnoughRightsError, ReadTimeoutError):
            break
        except Exception as e:
            formatted_update = json.dumps(msg, indent=3)
            res = traceback.format_exc()
            exc_url = send_to_dogbin('Update:\n' + formatted_update + '\n\n\n\nFull Traceback:\n' + res)
            na_bot.sendMessage(logs, '''• <b>Erro:</b>
 » Plugin: <code>{plugin}</code>
 » Tipo do erro: <code>{exc_type}</code>
 » Descrição: <i>{exc_desc}</i>

- <a href="{exc_url}">Erro completo</a>'''.format(plugin=plugin, exc_type=e.__class__.__name__,
                                                  exc_desc=html.escape(e.description if isinstance(e, TelegramError) else str(e)), exc_url=exc_url),
                               parse_mode='html', disable_web_page_preview=True)


if __name__ == '__main__':

    answerer = amanobot.aio.helper.Answerer(bot)
    loop = asyncio.get_event_loop()

    print('\n\nBot iniciado! {}\n'.format(version))


    loop.create_task(MessageLoop(bot, handle).run_forever())



    na_bot.sendMessage(logs, '''Bot iniciado

Versão: {}
Plugins carregados: {}
Ocorreram erros em {} plugin(s){}'''.format(version, len(ep), len(n_ep),
                                            ': ' + (', '.join(n_ep)) if n_ep else ''))

    loop.run_forever()

