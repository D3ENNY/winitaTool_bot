from pyrogram import Client, filters, enums
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
        
    if file is not None:
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
            await message.reply('⚠️ l\' argomento del comando deve essere un numero')
            print('---pwgen error 0---')
            return 0
    except:
        await message.reply('⚠️ il comando deve avere un argomento numerico')
        print('---pwgen error 1---')
        return 1
    
    for i in range(int(lenght)):
        pw.append(rnd.choice(char))
        
    rnd.shuffle(pw)
    pw = ''.join(pw)
    await bot.send_message(message.from_user.id, f'PASSWORD:\n```{pw}```')
    await message.reply('[password mandata in privato](t.me/windowsitaliatool_bot)')
    print('---end pwgen---')
    
@app.on_message(filters.regex(r'^[\.\!\&\/]calc', re.IGNORECASE) & filters.text)
async def calc(bot, message):
    gb = message.text.split(' ')[1]
    gib = ( int(gb) / 1024 ) * 1000
    print(gib,'\t',int(gib))
    await message.reply('gb {}\ngib {}\ngib convertiti {}'.format(gb, gib, math.floor(gib+0.5)))

@app.on_message(filters.regex(r'^[\.\!\&\/]search', re.IGNORECASE) & filters.text)
async def search(bot, message):
    GOOGLE_URL='https://www.google.com/search?q='
    DUCK_URL='https://duckduckgo.com/?q='
    txt = message.split(' ')
        
    

app.run() 