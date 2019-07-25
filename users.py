# User storage and managing

import os
import json
import datetime as dt


userz = None
userz_file = 'no file'

def init_userz():
    global userz
    global userz_file
    userz = []
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    userz_file = os.path.join(THIS_FOLDER, '-dbs', 'userz.db')
    load_userz()

def load_userz():
    global userz
    global userz_file
    if os.path.exists(userz_file):
        uf = open(userz_file, 'r', encoding='utf-8')
        userz = json.load(uf)
        uf.close()
        if userz == None:
            add_user(97835760, 'nikodim', 'O', dt.date(1973, 2, 24), 'здраствой, папа')
        else:
            for u in userz:
#                u['uid'] = int(u['uid'])
                u['ubd'] = dt.datetime.strptime(u['ubd'], '%d-%m-%Y')
            print('Userz.db loaded')
    else:
        print('File users.db does not exist')

def save_userz():
    global userz
    global userz_file
    for u in userz:
#        u['uid'] = str(u['uid'])
        u['ubd'] = u['ubd'].strftime('%d-%m-%Y')
    uf = open(userz_file, 'w')
    json.dump(userz, uf)
    uf.close()
    print('Userz.db saved')

def add_user(uid, uname, utype, ubd, utext):
    global userz
    if userz == None:
        userz = []
    if find_user('uid', uid) == None:
        userz.append({'uid':uid, 'uname':uname, 'utype':utype, 'ubd':ubd, 'utext':utext})
        save_userz()

def find_user(key, value):
    global userz
    for u in userz:
        if u[key] == value:
            return {'uid':u['uid'], 'uname':u['uname'], 'utype':u['utype'], 'ubd':u['ubd'], 'utext':u['utext']}
    return None

def user_is(uid, utype):
    u = find_user('uid', uid)
    if u != None:
        if u['utype'] == utype:
            return True
    return False

def change_utype(uid, new_utype):
    u = find_user('uid', uid)
    if u != None:
        u['utype'] = new_utype
        return True
    return False