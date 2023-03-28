from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import string as st
import random as rnd
import re
import main as ns

TOKEN = '5545133091:AAH6rS895ubCENyB-BzpczesbRcY2f8co9w'
REGEX = '^[\.\!\&\/]'
upd = Updater(TOKEN)
file=None


def ventoy(bot, update):
    cmd = bot.message.text.lower()
    chat_id = bot.message.chat_id
    user = bot.message.from_user
    
    print('======= NEW COMMAND =======')
    
    if re.search(r'^[\.\!\&\/]+ventoy$', cmd):
        
        print('---request file---')
        global file
        
        if not file:
            update.bot.send_document(chat_id, file.document.file_id, caption='beccate sto file')
        else:
            with open(ns.getFile(), 'rb') as document:
                file = update.bot.send_document(chat_id, document, caption='beccate sto file')
        print('---end request file---')
        
    elif re.search(r'^[\.\!\&\/]+ping$', cmd):
        
        print('---ping---')
        bot.message.reply_text('pong🏓')
        print('---end ping---')
        
    elif re.search(r'^[\.\!\&\/]+pwgen', cmd):
        
        print('---pwgen---')
        pw = []
        char = list(st.ascii_letters+st.digits+'!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
        rnd.shuffle(char)
        user_ID = user['id']
        username = user['username']
        lenght = None
 
        try:
            lenght = cmd.split(' ')[1]
            if not lenght.isdigit():
                bot.message.reply_text('⚠️ l\' argomento del comando deve essere un numero')
                return 0
        except:
            bot.message.reply_text('⚠️ il comando deve avere un argomento numerico')
            return 1
        
        for i in range(int(lenght)):
            pw.append(rnd.choice(char))
            
        rnd.shuffle(pw)
        pw = ''.join(pw)
        bot.message.reply_text(f'PASSWORD:\n```{pw}```', parse_mode='MarkdownV2')
        print('---end pwgen---')
        
    elif re.search(r'^[\.\!\&\/]+calc', cmd):
        
        gb = cmd.split(' ')[1]
        gib = ( int(gb) / 1024 ) * 1000
        print(gib,'\t',int(gib))
        bot.message.reply_text('gb {}\ngib {}\ngib convertiti {}'.format(gb, gib, int(gib)))
        
        
upd.dispatcher.add_handler(MessageHandler(Filters.text & Filters.regex((r'^[\.\!\&\/]')), ventoy))
upd.start_polling() 