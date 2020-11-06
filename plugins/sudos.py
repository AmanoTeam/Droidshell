from settings import bot, su, bot_id, bot_username, db


import os,sys, asyncio,re,html
from datetime import datetime
from utils import backup_sources


async def sudos(msg):
    if  msg.get('text'):
        text = msg['text']
        if  msg['from']['id'] in su:
            if msg['text'].split()[0] == '~backup':
                sent = await bot.sendMessage(msg['chat']['id'], '⏰ Fazendo backup...',
                                             reply_to_message_id=msg['message_id'])

                if 'pv' in msg['text'].lower() or 'privado' in msg['text'].lower():
                    msg['chat']['id'] = msg['from']['id']

                cstrftime = datetime.now().strftime('%d/%m/%Y - %H:%M:%S')

                fname = backup_sources()

                if not os.path.getsize(fname) > 52428800:
                    await bot.sendDocument(msg['chat']['id'], open(fname, 'rb'), caption="📅 " + cstrftime)
                    await bot.editMessageText((sent['chat']['id'], sent['message_id']), '✅ Backup concluído!')
                    os.remove(fname)
                else:
                    await bot.editMessageText((sent['chat']['id'], sent['message_id']),
                                              f'Ei, o tamanho do backup passa de 50 MB, então não posso enviá-lo aqui.\n\nNome do arquivo: `{fname}`',
                                              parse_mode='Markdown')

                return True
            if msg['text'] == '~sudos':
                await bot.sendMessage(msg['chat']['id'], '''
                Estes são sudos:
                {}
                '''.format(su))

            #if text.split()[0] == "/set":
               # text = text[5:]
               # db.hset('rules', str(msg['chat']['id']), text)
               # await bot.sendMessage(msg['chat']['id'], 'Setado')



            if msg['text'] == '~restart':
                await bot.sendMessage(msg['chat']['id'], 'Reiniciando')
                await asyncio.sleep(3)
                os.execl(sys.executable, sys.executable, *sys.argv)

            elif msg['text'].split()[0] == '!cmd':
                text = msg['text'][5:]
                if re.match('(?i).*poweroff|halt|shutdown|reboot', text):
                    res = 'Comando proibido.'
                else:
                    proc = await asyncio.create_subprocess_shell(text,
                                                                 stdout=asyncio.subprocess.PIPE,
                                                                 stderr=asyncio.subprocess.PIPE)
                    stdout, stderr = await proc.communicate()
                    res = (f"<b>Output:</b>\n<code>{html.escape(stdout.decode())}</code>"  if stdout else '') + (
                           f"\n\n<b>Errors:</b>\n<code>{html.escape(stderr.decode())}</code>"  if stderr else '')

                await bot.sendMessage(msg['chat']['id'], res or 'Comando executado.',
                                      parse_mode="HTML",
                                      reply_to_message_id=msg['message_id'])
                return True


