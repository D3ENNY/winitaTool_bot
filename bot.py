#!/bin/python

from pyrogram import Client, filters, enums, emoji
from pyrogram.types import InlineKeyboardButton as keybutton
from pyrogram.types import InlineKeyboardMarkup as keymarkup
from pyrogram.types import Message
from os.path import basename
import namespace as ns
import string as st
import random as rnd
import re, math, main

app = Client(
    'windows italia tool bot',
    api_id = 18121640,
    api_hash = '586ab19953703193dd8d7ad44ea4f3cb',
    bot_token = '5545133091:AAH6rS895ubCENyB-BzpczesbRcY2f8co9w'
)

#global variable
status = False
admin = [398290777, 77889335, 828056346]  #denny, alba, kaki
TARGET = -1001641675174
MESSAGE = '{} benvenuto capo!'

#custom filter
def status_filter():
    async def func(_,__,___):
        global status
        return True if not status else False
    return filters.create(func)

def admin_filter():
    async def func(_,__,msg:Message):
        return True if msg.from_user.id in admin else False
    return filters.create(func)

#async def admin_filter(_, c: Client, m: Message):
#    user = await c.get_chat_member(\
#        chat_id=m.chat.id,
#        user_id=m.from_user.id,
#    )
#    return bool(
#        user.status == enums.ChatMemberStatus.OWNER
#        or user.status == enums.ChatMemberStatus.ADMINISTRATOR
#    )
#check_admin = filters.create(admin_filter)

#function      
def getAdmin(message):
    for m in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        admin.append(int(m.user.id))
        
def resetFile():
    if ns.getFile():
        with open(main.getFile(), 'r') as file:
            if ns.getFile().document.file_name != basename(file.name):
                ns.setFile(None)
                print('--> reupload')

#bot function
@app.on_message(filters.command('start', prefixes=['!', '.', '&', '/']) & filters.text & status_filter())
def start(bot, message):
    print('---start---')
    global status 
    getAdmin(message)
    status = True
    print(admin)
    print('---end start---')


@app.on_message(filters.command('reload', prefixes=['!', '.', '&', '/']) & filters.text & admin_filter())
def reload(bot, message):
    print('---reload---')
    getAdmin(message)
    print(admin)
    print('---end reload---')

@app.on_message(filters.command('ventoy', prefixes=['!', '.', '&', '/']) & filters.text)     #TODO send documents message...
async def ventoy(bot, message):
    print('---request file---')

    chat_id = message.chat.id
    resetFile()
    
    if ns.getFile():
        await bot.send_document(chat_id, ns.getFile().document.file_id)
    else:
        with open(main.getFile(), 'rb') as document:
            file= await bot.send_document(chat_id, document, file_name=main.getFile().replace('download/', '').strip())
            ns.setFile(file)
    print('---end request file---')


@app.on_message(filters.regex(r'^ping$', re.IGNORECASE) | filters.regex(r'^[\.\!\&\/]ping$', re.IGNORECASE) & filters.text & admin_filter())
async def ping(bot, message):
    print('---ping---')
    await message.reply('Pong 🏓')
    print('---end ping---')

@app.on_message(filters.regex(r'^pong$', re.IGNORECASE) | filters.regex(r'^[\.\!\&\/]pong$', re.IGNORECASE) & filters.text & admin_filter())
async def ping(bot, message):
    print('---pong---')
    await message.reply('Ping 🏓')
    print('---end pong---')


@app.on_message(filters.command('alba', prefixes=['!', '.', '&', '/']) & filters.group)
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


@app.on_message(filters.command('pwgen', prefixes=['!', '.', '&', '/']) & filters.text)
async def pwgen(bot, message):
    print('---pwgen---')
    pw= []
    char = list(st.ascii_letters+st.digits+'!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
    typus = (await app.get_chat(message.chat.id)).type
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
    if typus != enums.ChatType.PRIVATE:
        await message.reply('[password mandata in privato](t.me/windowsitaliatool_bot)')
    print('---end pwgen---')


@app.on_message(filters.regex(r'^[\.\!\&\/]calc', re.IGNORECASE) & filters.text)    #TODO modifica messaggio
async def calc(bot, message):
    txt = message.text.lower().split(' ')
    chat_id = message.chat.id
    unit=None
    unit2=None
    n=None
    result=None

    match len(txt):
        case 1:
            await bot.send_message(chat_id, '⚠️ il comando deve avere almeno un argomento numerico ed un unità di misura\n```(GiB/GB)```')
            return 1
        case 2:
            if re.search(r'^[0-9]+[a-z]+$', txt[1]):
                await bot.send_message(chat_id, '⚠️ il comando deve avere come secondo argomento, staccato dal primo, un unità di misura\n```(GiB/GB)```')
                return 2
            elif not txt[1].isdigit():
                await bot.send_message(chat_id, '⚠️ il primo argomento del comando deve essere un numero')
                return 4
            else:
                await bot.send_message(chat_id, '⚠️ il comando deve avere come secondo argomento un unità di misura\n```(GiB/GB)```')
            return 3
        case _:
            if txt[1].isdigit():
                n = txt[1]
            else:
                await bot.send_message(chat_id, '⚠️ il primo argomento del comando deve essere un numero')
                return 4
            if txt[2] == 'gb' or txt[2] == 'gib':
                unit = txt[2]
            else:
                await bot.send_message(chat_id, '⚠️ il comando deve avere come secondo argomento un unità di misura\n```(GiB/GB)```')
                return 5
    
    if unit == 'gb':
        unit='GB'
        unit2='GiB'
        result = math.floor(((int(n) / 2**30) * 10**9) * 10**3 + 0.5) / 10**3
    elif unit == 'gib':
        unit = 'Gi'
        unit2='GB'
        result = math.floor(((int(n) / 10**9) * 2**30) * 10**3 + 0.5) / 10**3
    await message.reply(f'{n} {unit} sono {result} {unit2}')


@app.on_message(filters.regex(r'^[\.\!\&\/]search', re.IGNORECASE) & filters.text)      #TODO modifica messaggio
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
    try:
        await message.reply(
            text=f'ricerca per {txt} 👇',
            reply_markup=keymarkup(BTN),
            disable_web_page_preview = True
        )
    except:
        await bot.send_message(message.chat.id, '⚠️ invalid Url')

    print('--end search---')
    

@app.on_message(filters.chat(TARGET) & filters.new_chat_members)
async def benvenuto(bot, message):
     new_members = [u.mention for u in message.new_chat_members]
     text = MESSAGE.format(emoji.SPARKLES, ", ".join(new_members))
     await message.reply_text(text, disable_web_page_preview=True)


@app.on_message(filters.command('rufus', prefixes=['!', '.', '&', '/']) & filters.text)
async def rufus(bot, message):
    print('---rufus---')
    with open('volevi.gif', 'rb') as troll:
        await bot.send_animation(message.chat.id, troll)
    print('---end rufus---')
    
#TODO implementazione rufus.
#TODO Pannello consigli
#TODO commands command
#TODO sistemare gestione degli errori
#TODO implementazione JSON
#TODO beer pong

app.run()
