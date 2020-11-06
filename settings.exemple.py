import amanobot
import amanobot.aio
import asyncio
import redis

version = '2.0.1 BETA'

loop = asyncio.get_event_loop()

tokenb = '' #token
token = '' #token beta

bot = amanobot.aio.Bot(token)
na_bot = amanobot.Bot(token)


me = loop.run_until_complete(bot.getMe())
bot_username = me['username']
bot_id = me['id']



backups_chat = -1001051721856
backup_hours = ['02:00', '04:00', '06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00', '00:00']


db = redis.StrictRedis(host='', port=, password='') #Conecte no seu servidor redis

logs = 1234 #coloque o id do servidor de logs
su = ["Coloque os id se su"]

keys = dict(
    yandex = '' # coloque os token necessarios
)



enabled_plugins = [
    'start',
    'sudos',
    'welcome',
    'ferramentas',
    'translate',
    'extras'
]

async def isAdmin(chat_id, user_id, reply_id=None):
    adms = await bot.getChatAdministrators(chat_id)
    adm_id = []
    dic = {}
    for ids in adms:
        adm_id.append(ids['user']['id'])

    if user_id in adm_id:
        dic['user'] = True
    else:
        dic['user'] = False

    if reply_id in adm_id:
        dic['reply'] = True
    else:
        dic['reply'] = False

    if bot_id in adm_id:
        dic['bot'] = True
    else:
        dic['bot'] = False

    return dic
