#!/bin/python

from pyrogram import Client, filters, enums, emoji
from pyrogram.types import InlineKeyboardButton as keybutton
from pyrogram.types import InlineKeyboardMarkup as keymarkup
import re, math
import string as st
import random as rnd
import main as ns

app = Client(
    'windows italia tool bot',
    api_id = 18121640,
    api_hash = '586ab19953703193dd8d7ad44ea4f3cb',
    bot_token = '5545133091:AAH6rS895ubCENyB-BzpczesbRcY2f8co9w'
)


file = None
admin = []

@app.on_message(filters.command('start'))
def start(bot, message):
    print('---start---')
    for m in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        admin.append(int(m.user.id))
    print(admin, sep="-")
    print('---end start---')


@app.on_message(filters.regex(r'^[\.\!\&\/]ventoy$', re.IGNORECASE) & filters.text)
async def ventoy(bot, message):
    print('---request file---')

    global file
    chat_id = message.chat.id

    if file:
        await bot.send_document(chat_id, file.document.file_id)
    else:
        with open(ns.getFile(), 'rb') as document:
            file = await bot.send_document(chat_id, document)

    print('---end request file---')


@app.on_message(filters.regex(r'^ping$', re.IGNORECASE) | filters.regex(r'^[\.\!\&\/]ping$', re.IGNORECASE) & filters.text)
async def ping(bot, message):
    if int(message.from_user.id) in admin:
        print('---ping---')
        await message.reply('Pong 🏓')
        print('---end ping---')

@app.on_message(filters.regex(r'^pong$', re.IGNORECASE) | filters.regex(r'^[\.\!\&\/]pong$', re.IGNORECASE) & filters.text)
async def ping(bot, message):
    if int(message.from_user.id) in admin:
        print('---pong---')
        await message.reply('Ping 🏓')
        print('---end pong---')


@app.on_message(filters.regex(r'^[\.\!\&\/]alba$', re.IGNORECASE) & filters.group)
async def kick(bot,message):
    print('---kick---')
    chat_id = message.chat.id
    await bot.ban_chat_member(chat_id, message.from_user.id)
    await bot.send_message(chat_id, '-_-')
    await bot.send_message(chat_id, f'{message.from_user.username} è astato automaticamente terminato')
    await bot.unban_chat_member(chat_id, message.from_user.id)
    link = await app.create_chat_invite_link(chat_id)
    await bot.send_message(message.from_user.id, link.invite_link)
    print('---end kick---')


@app.on_message(filters.regex(r'^[\.\!\&\/]pwgen', re.IGNORECASE) & filters.text)
async def pwgen(bot, message):
    print('---pwgen---')
    pw= []
    char = list(st.ascii_letters+st.digits+'!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
    rnd.shuffle(char)
    lenght = None

    try:
        lenght = message.text.split(' ')[1]
        if not lenght.isdigit():
            await bot.send_message('⚠️ l\' argomento del comando deve essere un numero')
            print('---pwgen error 0---')
            return 0
    except:
        await bot.send_message('⚠️ il comando deve avere un argomento numerico')
        print('---pwgen error 1---')
        return 1

    for i in range(int(lenght)):
        pw.append(rnd.choice(char))

    rnd.shuffle(pw)
    pw = ''.join(pw)
    await bot.send_message(message.from_user.id, f'PASSWORD:\n```{pw}```')
    await message.reply('[password mandata in privato](t.me/windowsitaliatool_bot)')
    print('---end pwgen---')


@app.on_message(filters.regex(r'^[\.\!\&\/]calc', re.IGNORECASE) & filters.text)        #TODO insierie messaggi di errore in caso di mancato input implementazione gib -> gb
async def calc(bot, message):
    txt = message.text.split(' ')
    chat_id = message.chat.id
    unit=None
    n=None
    result=None

    match len(txt):
        case 1:
            bot.send_message(chat_id, '⚠️ il comando deve avere almeno un argomento numerico ed un unità di misura (```gib``` / ```gb```)')
            return 1
        case 2:
            bot.send_message(chat_id, '⚠️ il comando deve avere come secondo argomento un unità di misura (```gib``` / ```gb```)')
            return 2
        case _:
            if txt[1].isdigit():
                n = txt[1]
            else:
                bot.send_message(chat_id, '⚠️ il primo argomento del comando deve essere un numero')
                return 3
            if txt[3] == 'gb' or txt[3] == 'gib':
                unit = txt[3]
            else:
                bot.send_message(chat_id, '⚠️ il secondo argomento deve essere un unità di misura ```gb``` o ```gib```')
                return 4
    
    if unit == 'gb':
        result = math.floor(((int(gb) / 2**30) * 10**9) * 10**3 + 0.5) / 10**3
    elif unit == 'gib':
        result = 'pls alba fammi il calcolo che non so quale sia'
    print(result)
    await message.reply(f'{n} {unit} sono {resul} *capire come inserire l\'altra variabile*')


@app.on_message(filters.regex(r'^[\.\!\&\/]search', re.IGNORECASE) & filters.text)      #TODO messaggi di errore invalid url + modifica messaggio
async def search(bot, message):
    print('---search---')
    GOOGLE_URL='https://www.google.com/search?q='
    DUCK_URL='https://duckduckgo.com/?q='
    txt = re.sub(r'^[\.\!\&\/]search','', message.text.lower()).strip()
    url_txt = txt.replace(' ', '+')
    BTN = [
        [
            keybutton('DUCKDUCKGO', url=DUCK_URL+url_txt),
            keybutton('GOOGLE', url=GOOGLE_URL+url_txt)
        ]
    ]
    await message.reply(
        text=f'ricerca per {txt} 👇',
        reply_markup=keymarkup(BTN),
        disable_web_page_preview = True
    )
    print('--end search---')
    print(message.chat)
TARGET = -1001641675174
MESSAGE = '{} benvenuto capo!'
@app.on_message(filters.chat(TARGET) & filters.new_chat_members)
async def benvenuto(bot, message):
     new_members = [u.mention for u in message.new_chat_members]
     text = MESSAGE.format(emoji.SPARKLES, ", ".join(new_members))
     await message.reply_text(text, disable_web_page_preview=True)

#TODO implementazione rufus


app.run()
