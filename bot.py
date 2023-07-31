#!/bin/python

from pyrogram import Client, filters, enums, emoji
from pyrogram.types import InlineKeyboardButton as keybutton
from pyrogram.types import InlineKeyboardMarkup as keymarkup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram.types import ChatPermissions, Message
from os.path import basename, isfile
from os import remove
from datetime import datetime, timedelta, date
import string as st
import random as rnd
import re, math, ast, json

import ventoy as ventoyScript
import rufus as rufusScript
import namespace as ns

app = Client(
    'windows italia tool bot',
    api_id = 18121640,
    api_hash = '586ab19953703193dd8d7ad44ea4f3cb',
    bot_token = '5545133091:AAH6rS895ubCENyB-BzpczesbRcY2f8co9w'
)

#global variable
status = False
admin = []
dev = [398290777,828056346]
TARGET = -1001641675174        #win ita debloat betatest
#TARGET = -742830246
scheduler = AsyncIOScheduler()

#JSON Time
with open("resources/JSON/message.json", 'r') as file:
    jFile = json.load(file)

#custom filter
def status_filter():
    async def func(_,__,___):
        global status
        return True if not status else False
    return filters.create(func)

def admin_filter():
    async def func(_,__,message):
        return True if message.from_user.id in admin else False
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
    global admin
    admin = [77889335]  #kaki
    admin += dev         #denny - alba4k
    for m in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        admin.append(int(m.user.id))
        
        
def resetFile(url):
    if 'ventoy' in url and ns.ventoy:
        with open(url, 'r') as file:
            if ns.ventoy.document.file_name != basename(file.name):
                ns.ventoy = None
                print('--> reupload')
    elif 'rufus' in url and ns.rufus :
        with open(url, 'r') as file:
            if ns.rufus.document.file_name != basename(file.name):
                ns.rufus = None
                print('--> reupload')


def generateCaptcha():
    try:
        '''ritorna un captcha matematico
            @returns dictionary
            @keys
                    ans_n1 : string  
                    ans_n2 : string
                    ans_n3 : string
                    question : string
                    rightAns : string
        '''
        captcha = {
            'ans_n1': None,
            'ans_n2': None,
            'ans_n3': None,
            'question': None,
            'right_Ans': None

        }
        operator = ['+', '-', '*']
        wrongAns = []
        sign = operator[rnd.randint(0, len(operator))]
        cnt=0

        while True:
            n1 = str(rnd.randint(0, 10))
            n2 = str(rnd.randint(0, 10))
            rightAns = eval(n1 + sign + n2)
            if rightAns >= 0:
                break
        
        while cnt < 3:
            n = rnd.randint(rightAns-10, rightAns+10)
            if n in wrongAns or n < 0 or n == rightAns:
                print(n)
                pass
            wrongAns.append(n)
            cnt+=1

        captcha['ans_n1'] = wrongAns[0]
        captcha['ans_n2'] = wrongAns[1]
        captcha['ans_n3'] = wrongAns[2]
        captcha['question'] = n1 + sign + n2
        captcha['right_Ans'] = rightAns

        return captcha
    except:
        print('--Ritento--')
        return generateCaptcha()
            
            
def saveCaptcha(user_id):
    with open(f'tmp/{user_id}', 'w') as file:
        file.write(str(generateCaptcha()))


def getCaptcha(user_id, param='all'):
    with open(f'tmp/{user_id}', 'r') as file:
        if param == 'all':
            return ast.literal_eval(file.read())
        else:
            return ast.literal_eval(file.read())[param]


def removeCaptcha(user_id):
    remove(f'tmp/{user_id}')


async def kick(user_id):
    scheduler.remove_job('countdown')
    await app.ban_chat_member(TARGET, user_id)
    await app.unban_chat_member(TARGET, user_id)
    removeCaptcha(user_id)
             
      
#def saveBestemmia(chat_id):
#    path = f'resources/commands/bestemmie/{chat_id}'
#    if not isfile(path):
#        with open(f'resources/commands/bestemmie/{chat_id}', 'w') as file:
#            file.write(date.today())
#        
#
#def getBestemmia(chat_id):
#    with open(f'resources/commands/bestemmie/{chat_id}', 'r') as file:
#        date = intfile.read().split("-")
#    return datetime(date[0], date[1], date[2])
#    
#    
#def removeBestemmia(chat_id):
#    remove(f'resources/commands/bestemmie/{chat_id}')  

    
#bot function
@app.on_message(filters.command('start', prefixes=['!', '.', '&', '/']) & filters.text & status_filter())
def start(bot, message):
    print('---start---')
    global status 
    getAdmin(message)
    status = True
    print(admin)
    print('-->', message.chat.id)
    print('---end start---')


@app.on_message(filters.command('reload', prefixes=['!', '.', '&', '/']) & filters.text & admin_filter())
def reload(bot, message):
    print('---reload---')
    global admin
    admin.clear()
    getAdmin(message)
    print(admin)
    print('-->', message.chat.id)
    print('---end reload---')
    
    
@app.on_message(filters.command('adminTool', prefixes=['!', '.', '&', '/']) & filters.text & filters.group)
async def getAdminTool(bot, message):
    print('---admin---')
    global admin
    global dev
    txt =jFile["message"]["caption"]["admin_tool"]["txt"]
    mod = await app.get_users(admin)
    for i in mod:
        if i.id in dev:
            txt += jFile["message"]["caption"]["admin_tool"]["dev"] % (emoji.MAN_TECHNOLOGIST, i.username)
    for i in mod: 
        if i.id in admin and i.id not in dev and not i.is_bot:
            txt += jFile["message"]["caption"]["admin_tool"]["admin"] % (emoji.MAN_POLICE_OFFICER, i.username)
    txt.strip()
    await bot.send_message(message.chat.id, txt)
    print('---end admin---')
    
    
@app.on_message(filters.command('ventoy', prefixes=['!', '.', '&', '/']) & filters.text)     #TODO send documents message
async def ventoy(bot, message):
    print('---request ventoy---')
    chat_id = message.chat.id
    resetFile(ventoyScript.getFile())
    
    if ns.ventoy:
        await bot.send_document(chat_id, ns.ventoy.document.file_id)
    else:
        with open(ventoyScript.getFile(), 'rb') as document:
            file= await bot.send_document(chat_id, document, file_name=ventoyScript.getFile().replace('download/ventoy/', '').strip())
            ns.ventoy = file
    print('---end request ventoy---')


@app.on_message(filters.command('rufus', prefixes=['!', '.', '&', '/']) & filters.text)     #TODO send documents message
async def rufus(bot, message):
    print('---request rufus---')
    chat_id = message.chat.id
    resetFile(rufusScript.getFile())

    if ns.rufus:
        await bot.send_document(chat_id, ns.rufus.document.file_id)
    else:
        with open(rufusScript.getFile(), 'rb') as document:
            file = await bot.send_document(chat_id, document, file_name=rufusScript.getFile().replace('download/rufus/','').strip())
            ns.rufus = file
    print('---end request rufus---')
    
    
@app.on_message((filters.regex(r'^ping$', re.IGNORECASE) | filters.regex(r'^[\.\!\&\/]ping$', re.IGNORECASE)) & filters.text & (admin_filter() | filters.private))
async def ping(bot, message):
    print('---ping---')
    await message.reply(jFile["message"]["caption"]["ping"]["output"] % (emoji.PING_PONG))    
    print('---end ping---')

@app.on_message((filters.regex(r'^pong$', re.IGNORECASE) | filters.regex(r'^[\.\!\&\/]pong$', re.IGNORECASE)) & filters.text & (admin_filter() | filters.private))
async def ping(bot, message):
    print('---pong---')
    await message.reply(jFile["message"]["caption"]["pong"]["output"] % (emoji.PING_PONG))    
    print('---end pong---')

@app.on_message((filters.regex(r'^beer$', re.IGNORECASE) | filters.regex(r'^[\.\!\&\/]beer$', re.IGNORECASE)) & filters.text & (admin_filter() | filters.private))
async def beer(bot, message):
    print('---beer---')
    await message.reply(jFile["message"]["caption"]["beer"]["reply"][rnd.randint(0, len(jFile["message"]["caption"]["beer"]["reply"])-1)])
    print('---end beer---')
    


@app.on_message(filters.command('freekey', prefixes=['!', '.', '&', '/']) & filters.group)
async def autoKick(bot,message):
    print('---autoKick---')
    chat_id = message.chat.id
    await bot.ban_chat_member(chat_id, message.from_user.id)
    await bot.send_message(chat_id, '-_-')
    await bot.send_message(chat_id, f'{message.from_user.username} è astato automaticamente terminato')
    await bot.unban_chat_member(chat_id, message.from_user.id)
    link = await app.create_chat_invite_link(chat_id)
    await bot.send_message(message.from_user.id, link.invite_link)
    print('---end autoKick---')


@app.on_message(filters.command('pwgen', prefixes=['!', '.', '&', '/']) & filters.text)
async def pwgen(bot, message):
    print('---pwgen---')
    print(message.text)
    pw = []
    char = list(st.ascii_letters+st.digits+'!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
    typus = (await app.get_chat(message.chat.id)).type
    rnd.shuffle(char)
    lenght = None

    try:
        lenght = message.text.split(' ')[1]
        if not lenght.isdigit():
            await bot.send_message(message.chat.id, jFile["message"]["error"]["pwgen"]["number_error"])
            print('---pwgen error 0---')
            return 1
    except:
        await bot.send_message(message.chat.id, jFile["message"]["error"]["pwgen"]["number_error"])
        print('---pwgen error 1---')
        return 1

    for i in range(int(lenght)):
        pw.append(rnd.choice(char))

    rnd.shuffle(pw)
    pw = ''.join(pw)
    await bot.send_message(message.from_user.id, jFile["message"]["caption"]["pwgen"]["output"] % pw)
    if typus != enums.ChatType.PRIVATE:
        await message.reply(jFile["message"]["caption"]["pwgen"]["dm"])
    print('---end pwgen---')


@app.on_message(filters.regex(r'^[\.\!\&\/]calc', re.IGNORECASE) & filters.text)
async def calc(bot, message):
    print('---calc---')
    txt = message.text.lower().split(' ')
    chat_id = message.chat.id
    unit=None
    unit2=None
    n=None
    result=None

    match len(txt):
        case 1:
            await bot.send_message(chat_id, jFile["message"]["error"]["calc"]["example_error"])
            return 1
        case 2:
            if re.search(r'^[0-9]+[a-z]+$', txt[1]):
                await bot.send_message(chat_id, jFile["message"]["error"]["calc"]["second_args_error"])
                return 1
            elif not txt[1].isdigit():
                await bot.send_message(chat_id,jFile["message"]["error"]["calc"]["numeric_first_args_error"])
                return 1
            else:
                await bot.send_message(chat_id, jFile["message"]["error"]["calc"]["second_args_error"])
            return 1
        case _:
            if txt[1].isdigit():
                n = txt[1]
            else:
                await bot.send_message(chat_id, jFile["message"]["error"]["calc"]["numeric_first_args_error"])
                return 1
            if txt[2] == 'gb' or txt[2] == 'gib':
                unit = txt[2]
            else:
                await bot.send_message(chat_id, jFile["message"]["error"]["calc"]["unity_second_args_error"])
                return 1
    
    if unit == 'gb':
        unit='GB'
        unit2='GiB'
        result = math.floor(((int(n) / 2**30) * 10**9) * 10**3 + 0.5) / 10**3
    elif unit == 'gib':
        unit = 'GiB'
        unit2='GB'
        result = math.floor(((int(n) / 10**9) * 2**30) * 10**3 + 0.5) / 10**3
    await message.reply(jFile["message"]["caption"]["calc"]["output"] % (n, unit, str(result), unit2))
    print('---end calc---')


@app.on_message(filters.regex(r'^[\.\!\&\/]search', re.IGNORECASE) & filters.text)
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
            text=jFile["message"]["caption"]["search"]["output"] % (txt, emoji.BACKHAND_INDEX_POINTING_DOWN),
            reply_markup=keymarkup(BTN),
            disable_web_page_preview = True
        )
    except:
        await bot.send_message(message.chat.id, jFile["message"]["error"]["search"]["invalid_url_error"])

    print('---end search---')
#    
#
#@app.on_message(filters.chat(TARGET) & filters.new_chat_members)
#async def welcome(bot, message):
#    print('---welcome---')
#    user_name = message.from_user.first_name
#    user_id = message.from_user.id
#    await app.restrict_chat_member(TARGET, user_id, ChatPermissions())
#    saveCaptcha(user_id)
#    captcha = getCaptcha(user_id)
#    case = [captcha['ans_n1'], captcha['ans_n2'], captcha['ans_n3'], captcha['right_Ans']]
#    rnd.shuffle(case)
#    
#    BTN = keymarkup([
#        [
#            keybutton(f'{case[0]}', callback_data=f'captcha_{case[0]}'),
#            keybutton(f'{case[1]}', callback_data=f'captcha_{case[1]}')],
#        [
#            keybutton(f'{case[2]}', callback_data=f'captcha_{case[2]}'),
#            keybutton(f'{case[3]}', callback_data=f'captcha_{case[3]}')]
#    ])
#    
#    await message.reply(jFile["message"]["caption"]["captcha"]["output"], reply_markup=BTN)
#    scheduler.add_job(kick, args=[user_id], id='countdown', trigger='interval', minutes=10)
#    
#    @app.on_callback_query()
#    async def answer(client, callback_query):
#        query = callback_query.data
#        query_id = callback_query.id
#        user = callback_query.from_user.id
#        if 'captcha_' in query:
#            if query == f"captcha_{getCaptcha(user_id, 'right_Ans')}":
#                await app.restrict_chat_member(
#                    TARGET,
#                    user_id,
#                    ChatPermissions(
#                        can_send_messages=True,
#                        can_send_media_messages=True,
#                        can_send_other_messages=True,
#                        can_send_polls=True,
#                        can_add_web_page_previews=True,
#                    ),
#                    datetime.now() + timedelta(minutes=10)
#                )
#                removeCaptcha(user)
#                await callback_query.edit_message_text(jFile["message"]["caption"]["captcha"]["welcome"])
#                scheduler.remove_job('countdown')
#            else:
#                await app.answer_callback_query(query_id, text='Captcha non corretto, riprova!', show_alert=True)
#
#    print('---end welcome---')
#    
#@app.on_message(filters.command('bestemmia') | filters.text)
#async def bestemmia(bot, message):
#    print('---bestemmia---')
#    chat_id = message.chat.it
#    
#    saveBestemmia(chat_id)
#    bestemmia = bst.filtred_random()
#    
#    lastDate = getBestemmia(chat_id)
#    today = date.today()
#    nextDate = today + timedelta( days= 1)
#
#    if lastDate < today:
#        await bot.send_message(chat_id, jFile['message']['caption']['bestemmia']['output'] % bestemmia, str(nextDate))
#        
#    elif lastDate == today:
        

    
    
#@app.on_message(filters.regex(r'^helpme$', re.IGNORECASE) | filters.regex(r'^[\.\!\&\/]helpme$', re.IGNORECASE) & filters.text & admin_filter())
#async def helpme(bot, message):
#        print('---saveme---')
#        await app.restrict_chat_member(TARGET, 398290777 , ChatPermissions(
#            can_send_messages=True,
#            can_send_media_messages=True,
#            can_send_other_messages=True,
#            can_send_polls=True,
#            can_add_web_page_previews=True,
#        ))
#        await bot.send_message(TARGET, 'pirla smutato dalla \'console\'')
    
    
#TODO Pannello consigli
#TODO sistemare welcomeBot
#TODO avviso manda file
scheduler.start()
app.run()