from settings import bot,db, isAdmin

async def extras(msg):
    if msg.get('text'):
        text = msg['text']

        chat_id = msg['chat']['id']
        if msg['text'].startswith('/extras '):
            chat_id = msg['chat']['id']

            if (await isAdmin(chat_id, msg['from']['id']))['user']:
                if 'reply_to_message' in msg:
                    try:
                        reply = msg['reply_to_message']['sticker']
                        doc = 'sticker'
                    except:
                        try:
                            reply = msg['reply_to_message']['document']
                            doc = 'document'
                        except:
                            try:
                                reply = msg['reply_to_message']['photo']
                                doc = 'photo'
                            except:
                                try:
                                    reply = msg['reply_to_message']['audio']
                                    doc = 'audio'
                                except:
                                    try:
                                        reply = msg['reply_to_message']['video']
                                        doc = 'video'
                                    except:
                                        doc = 'text'

                    if doc != 'text':
                        file = msg['reply_to_message'][doc]['file_id']
                    else:
                        file = msg['reply_to_message']['text']
                    tag = text.split(' ')[1]
                    db.hset('{}_tags'.format(str(chat_id)), str(tag), str(file))
                    await bot.sendMessage(chat_id, '🏷O comando "{}" foi salvo com sucesso!'.format(tag),
                                    reply_to_message_id=msg['message_id'])
                else:
                    tag = text.split(' ')[1]
                    txt = text.split(tag, 1)[1]
                    db.hset('{}_tags'.format(str(chat_id)), str(tag), str(txt))
                    await bot.sendMessage(msg['chat']['id'], '🏷O comando "{}" foi salvo com sucesso!'.format(tag),
                                    reply_to_message_id=msg['message_id'])

        elif text.startswith('/rmnota '):

            if (await isAdmin(msg['chat']['id'], msg['from']['id']))['user']:
                tag = text.replace('/rmnota ', '')

                for num, i in enumerate(tag.split()):
                    db.hdel('{}_tags'.format(chat_id), i)
                    num = num
                if num == 0:
                    await bot.sendMessage(msg['chat']['id'], '🏷O comando {} foi deletado!'.format(tag))
                else:
                    await bot.sendMessage(msg['chat']['id'],
                                    '🏷Os comandos {} foram deletados!'.format(', '.join(tag.split())))

        elif text == '/notas':

            a = []
            tag = db.hgetall('{}_tags'.format(str(chat_id)))

            for (i, tag) in enumerate(tag):
                a.append(tag.decode())
            b = '\n'.join(a)
            if len(a) == 0:
                await bot.sendMessage(chat_id, '🏷Nenhum comando disponível.\n\n{}'.format(b))
            else:
                await bot.sendMessage(chat_id, '🏷Comandos disponíveis:\n\n{}'.format(b))

        else:
            try:
                tag = db.hgetall('{}_tags'.format(msg['chat']['id']))[msg['text'].encode()]
                try:
                    await bot.sendDocument(msg['chat']['id'], tag.decode(), reply_to_message_id=msg['message_id'])
                except:
                    await bot.sendMessage(msg['chat']['id'], tag.decode(), reply_to_message_id=msg['message_id'])
            except:
                pass
