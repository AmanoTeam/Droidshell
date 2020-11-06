from amanobot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
#[start]
keyboard = InlineKeyboardMarkup(inline_keyboard=[
 [dict(text=' Comandos', callback_data='comandos')]+
 [dict(text=' Informações', callback_data='infos')]
])

back = InlineKeyboardMarkup(inline_keyboard=[
    [dict(text='voltar', callback_data='home')]
    ])
###############
