#!/usr/bin/python3.6

from bottle import default_app, route, view, request, static_file, template
#import urllib.request
import talkzsearch as tsr
import locationstore as locz
import users
import telegram
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
import datetime as dt
from uuid import uuid4
import logging
from logging.handlers import RotatingFileHandler
import os
import sarah

TOKEN = '225635767:AAGEvQKd4Cj8wNN24wM5hpd8FlgiJPmky0A'  #IkuraBot
#TOKEN = '468664268:AAEtyHluK_EpOyoWANgB8X74YxGf5TpvKXY'  #IkuraJrBot
APPNAME = 'nikodim'
PAPAID = 97835760

bot_aliases = ['Ikura-san', 'Ikura', 'ikura', 'Икура-сан', 'Икура', 'икура', 'brehf', 'Brehf', 'Brehf-cfy', 'икурасан', 'Икурасан']

mAdd = False
command_message = None
this_path = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(this_path, '-logs', __name__ + '.log')

# Enable logging
#logging.basicConfig(filename = log_file, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                    level=logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = RotatingFileHandler(log_file, maxBytes=4194304, backupCount=3)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

tsr.init()
users.init()

logger.debug('----------------==============>>>>>>>>>>>>>> STARTED <<<<<<<<<<<<<<<=============---------------------')


@route('/setWebhook')
def setWebhook():
    bot = telegram.Bot(TOKEN)
    botWebhookResult = bot.setWebhook(webhook_url='https://{}.pythonanywhere.com/botHook'.format(APPNAME))
    return str(botWebhookResult)

@route('/botHook', method='POST')
def botHook():
    bot = telegram.Bot(TOKEN)
    update = telegram.update.Update.de_json(request.json, bot)

    if update.inline_query is not None and update.inline_query.query:       # We've got an inline query
        tlkz = tsr.search_talkz(update.inline_query.query, 50)
        results = []
        for t in tlkz:
            txt = ''
            if t[0] != -500: txt = t[1]
#            results.append(InlineQueryResultArticle(id = uuid4(), title = '(' + str(t[0]) + ') ' + t[2], input_message_content = InputTextMessageContent(txt), description = t[1]))
            results.append(InlineQueryResultArticle(id = uuid4(), title = txt, input_message_content = InputTextMessageContent(txt)))

        bot.answerInlineQuery(update.inline_query.id, results)
        return 'OK'


    if update.message is not None:                                          # We've got a message
        global mAdd
        global command_message
#        global tstconf
#        logger.info('message: ' + update.message.text)

        if users.add_user(update.message.from_user.id, update.message.from_user.username, 'U', dt.date(1901,1,1), 'Added ' + dt.datetime.now().isoformat()):
            bot.sendMessage(chat_id = PAPAID, text = 'добавил копа. ' + update.message.from_user.username + ' (' + str(update.message.from_user.id) + ')')

        if update.message.location is not None:
            locz.add_loc(update.message)
            #logger.info('location %s, %s', update.message.location.longitude, update.message.location.latitude)
            return 'OK'

        if update.message.text == '/listusers':
            command_message = update.message
            if not users.usertype_is(update.message.from_user.id, 'O'):
                bot.sendMessage(chat_id = update.message.chat_id, text = 'Иди нухай, коп')
                return 'Access denied'
            bot.sendMessage(chat_id = update.message.chat_id, text = users.list_userz())
            return 'OK'

        if isinstance(update.message.text, str):
            mtext = update.message.text
            command = mtext.split()[0]
            user_name = ""
            if len(mtext.split()) > 1:
                user_name = mtext.split()[1]
            if command == '/makeowner':
                if not (update.message.from_user.id == PAPAID):
                    bot.sendMessage(chat_id = update.message.chat_id, text = 'иди нухай, коп. ты непапа')
                    return 'Access denied'
                if users.change_attr(user_name, 'utype', 'O'):
                    bot.sendMessage(chat_id=update.message.chat_id, text=users.str_user(users.find_user('uname', user_name)))
                    return 'OK'
                else:
                    bot.sendMessage(chat_id = update.message.chat_id, text = 'нету такого копа')
                    return 'OK'

            if command == '/makemoder':
                if not (users.usertype_is(update.message.from_user.id, 'O') or update.message.from_user.id == PAPAID):
                    bot.sendMessage(chat_id = update.message.chat_id, text = 'иди нухай, коп')
                    return 'Access denied'
                if users.change_attr(user_name, 'utype', 'M'):
                    bot.sendMessage(chat_id=update.message.chat_id, text=users.str_user(users.find_user('uname', user_name)))
                    return 'OK'
                else:
                    bot.sendMessage(chat_id = update.message.chat_id, text = 'нету такого копа')
                    return 'OK'


            if command == '/makeuser':
                if not (users.usertype_is(update.message.from_user.id, 'O') or update.message.from_user.id == PAPAID):
                    bot.sendMessage(chat_id = update.message.chat_id, text = 'иди нухай, коп')
                    return 'Access denied'
                if users.change_attr(user_name, 'utype', 'U'):
                    bot.sendMessage(chat_id=update.message.chat_id, text=users.str_user(users.find_user('uname', user_name)))
                    return 'OK'
                else:
                    bot.sendMessage(chat_id = update.message.chat_id, text = 'нету такого копа')
                    return 'OK'

            if command == '/set':
                user_attr = mtext.split()[2]
                user_value = mtext[len(mtext.split()[0]) + len(mtext.split()[1]) + len(mtext.split()[2]) + 3:]
                if not (users.usertype_is(update.message.from_user.id, 'O') or update.message.from_user.id == PAPAID):
                    bot.sendMessage(chat_id = update.message.chat_id, text = 'иди нухай, коп')
                    return 'Access denied'
                if users.find_user('uname', user_name) is None:
                    bot.sendMessage(chat_id = update.message.chat_id, text = 'нету такого копа')
                    return 'Not found'
                if users.change_attr(user_name, user_attr, user_value):
                    bot.sendMessage(chat_id=update.message.chat_id, text=users.str_user(users.find_user('uname', user_name)))
                    return 'OK'
                else:
                    bot.sendMessage(chat_id=update.message.chat_id, text='хуйню сказал, папаша')
                    return 'Error'

        if update.message.text == '/add':
            command_message = update.message
            u = users.find_user('uid', update.message.from_user.id)
            if u is None or not (u['utype'] == 'O' or u['utype'] == 'M'):
                bot.sendMessage(chat_id = update.message.chat_id, text = 'иди нухай, коп')
                return 'Access denied'
            bot.sendMessage(chat_id = update.message.chat_id, text = 'Пезди давай. Но токо больше 10 букв и ченть новенькое')
            mAdd = True
            return 'OK'

        if update.message.text == '/del':
            command_message = update.message
            u = users.find_user('uid', update.message.from_user.id)
            if u is None or not (u['utype'] == 'O' or u['utype'] == 'M'):
                bot.sendMessage(chat_id = update.message.chat_id, text = 'иди нухай, коп')
                return 'Access denied'
            if tsr.last_message[0] == -1:
                bot.sendMessage(chat_id = update.message.chat_id, text = 'нехуя удалять')
                return 'OK'
            keyboard = [[InlineKeyboardButton('удалить впезду "' + tsr.last_message[1] + '"', callback_data=tsr.last_message[0])], [InlineKeyboardButton("или нуево нахуй", callback_data=-1)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('Ну чо, ', reply_markup=reply_markup)
            return 'OK'

        if mAdd:
            mAdd = False
            res = tsr.add_talk(update.message.text)
            if res[0]:
                bot.sendMessage(chat_id = update.message.chat_id, text = 'зопомнел')
                logger.info('ADDTALK. User:%s in chat:%s added talk:%s', update.message.from_user, update.message.chat, update.message.text);
            else:
                if res[1]: txt = 'уже есть такая хуета: ' + res[1]
                else: txt = 'хуйню сказал, папаша'
                bot.sendMessage(chat_id = update.message.chat_id, text = txt)
            return 'OK'

        bot_called = False
        if update.message.text is not None:
            bot_called = (update.message.text.partition(' ')[0] in bot_aliases)

            if bot_called:
                message_text = update.message.text.partition(' ')[2]

                if message_text == 'локи':
                    logger.info('локи')
                    logger.debug('локи')
                    lres = locz.select_locz(update.message.chat_id, update.message.from_user.id)
                    if lres[0] == '|':
                        bot.sendMessage(chat_id = update.message.chat_id, text = "http://maps.googleapis.com/maps/api/staticmap?size=800x800&path={0}".format(lres[1:]))
                    else:
                        bot.sendMessage(chat_id = update.message.chat_id, text = lres)
                    return 'OK'
            else:
                message_text = update.message.text

            if update.message.chat.type == 'private' or tsr.can_talk(update.message.chat.id) or (tsr.can_answer(update.message.chat.id) and bot_called):
                if message_text == '':
                    bot.sendMessage(chat_id = update.message.chat_id, text = 'чево?')
                else:
                    bot.sendMessage(chat_id = update.message.chat_id, text = tsr.search_talk(message_text))
            return 'OK'

    if update.callback_query is not None:                                   # We've got a callback query
        query = update.callback_query
        ndx = int(query.data)
        if ndx == -1:
            bot.edit_message_text(text='ну ок', chat_id=query.message.chat_id, message_id=query.message.message_id)
        else:
            tsr.last_message = (-1, '')
            res = tsr.del_talk(ndx)
            bot.edit_message_text(text='удалил "' + res + '"', chat_id=query.message.chat_id, message_id=query.message.message_id)
            logger.info('DELTALK. User:%s in chat:%s deleted talkid:%s talk:%s', command_message.from_user, query.message.chat, ndx, res);
        return 'OK'

@route('/')
@route('/home')
@view('home')
def home():
    """Renders the home page."""
    return dict(
        year=dt.date.today().year
    )

@route('/log')
def log():
    return static_file(log_file, root = this_path)

@route('/locs')
#@route('/locs/<name>')
def locs(name='World'):
    return template(os.path.join(this_path, '-locs', 'locs.tpl'), name=name)


# ========================================== Sarah section ===========================================

# moved to sarah.py

# --------------------------------------- End of Sarah Section ----------------------------------------

application = default_app()

