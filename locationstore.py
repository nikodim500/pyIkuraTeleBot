import os
import sys
import logging
import MySQLdb
#import datetime

logger = logging.getLogger(__name__)

locz = []
locz_file = ''

# 'locz' table fields: chat_id, chat_title, user_id, user_name, date_time, latitude, longitude


def add_loc(mess):
    locstr = 'chat.id:' + str(mess.chat.id) + ',chat.title:' + str(mess.chat.title) + ',user.id:' + str(mess.from_user.id) + ',user.username:' + str(mess.from_user.username) + ',message.date:' + str(mess.date) + ',location.latitude:' + str(mess.location.latitude) + ',location.longitude:' + str(mess.location.longitude)
    locz.append(locstr)
#    logger.info('locstr: ' + locstr)
    #sql = """insert into locz values({0}, '{1}', {2}, '{3}', '{4}', {5}, {6}).format(mess.chat.id, mess.chat.title, mess.from_user.id, mess.from_user.username, datetime.datetime.strptime(mess.date, '%Y-%m-%d %H:%M:%S'), mess.location.latitude, mess.location.longitude)
    sql = """insert into locz values({0}, '{1}', {2}, '{3}', '{4}', {5}, {6})""".format(mess.chat.id, mess.chat.title, mess.from_user.id, mess.from_user.username, mess.date, mess.location.latitude, mess.location.longitude)
    try:
        db = MySQLdb.connect(host="nikodim.mysql.pythonanywhere-services.com", user="nikodim", passwd="IkuRa700", db="nikodim$ikuradb", charset='utf8')
        try:
            db.query(sql)
            db.commit()
        except:
            logger.error('Location record to DB failure. ' + str(sys.exc_info()[0]) + '. sql: ' + sql)
        finally:
            db.close()
    except:
        logger.error('DB connection error. ' + str(sys.exc_info()[0]))

    save_loc()
    logger.info('Location added. ' + locstr)

def select_locz(chat_id, user_id):
    sql = """select latitude, longitude, date_time from locz where chat_id = {0} and user_id = {1} order by date_time""".format(chat_id, user_id)
    try:
        db = MySQLdb.connect(host="nikodim.mysql.pythonanywhere-services.com", user="nikodim", passwd="IkuRa700", db="nikodim$ikuradb", charset='utf8')
        try:
            db.query(sql)
            r = db.store_result()
            rows = r.fetch_row(maxrows=0)
        except:
            logger.error('Select locations from DB failure. ' + str(sys.exc_info()[0]) + '. sql: ' + sql)
        finally:
            db.close()
        if not rows:
            return 'нет локов'
        else:
            res = ''
            for tup in rows:
                res = res + '|' + str(tup[0]) + ',' + str(tup[1])
            return res
    except:
        logger.error('DB connection error. ' + str(sys.exc_info()[0]))
        return 'ошибка'

def init_locz():
    global locz
    global locz_file
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    locz_file = os.path.join(THIS_FOLDER, '-locs', 'locz.tdb')
    lf = open(locz_file, 'r', encoding='utf-8')
    locz = lf.readlines()
    lf.close()
    locz = [l.replace('\n', '') for l in locz]


def save_loc():
    global locz
    global locz_file
    locz = list(set(locz))
    loczz = [l + '\n' for l in locz]
    lf = open(locz_file, 'w')
    lf.writelines(loczz)
    lf.close()
#    print('locz.db saved')

init_locz()
