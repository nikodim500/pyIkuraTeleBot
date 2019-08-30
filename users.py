# User storage and managing

import os
import json
import datetime as dt
from copy import deepcopy


userz = None
userz_file = 'no file'

def init():
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
        with open(userz_file, 'r', encoding='utf-8') as uf:
            luserz = json.load(uf)
        if luserz is None:
            add_user(97835760, 'nikodim', 'O', dt.date(1973, 2, 24), 'здраствой, папа')
        else:
            for u in luserz:
#                u['uid'] = int(u['uid'])
                u['ubd'] = dt.datetime.strptime(u['ubd'], '%d-%m-%Y')
            userz = luserz.copy()
            print('Userz.db loaded')
    else:
        print('File users.db does not exist')
        add_user(97835760, 'nikodim', 'O', dt.date(1973, 2, 24), 'здраствой, папа')

def save_userz():
    global userz
    global userz_file
    suserz = deepcopy(userz)
    for u in suserz:
#        u['uid'] = str(u['uid'])
        if isinstance(u['ubd'], dt.date):
            u['ubd'] = u['ubd'].strftime('%d-%m-%Y')
    with open(userz_file, 'w') as uf:
        json.dump(suserz, uf)
    print('Userz.db saved')

def add_user(uid, uname, utype, ubd, utext):
    global userz
    if userz is None:
        userz = []
    if userz == [] or find_user('uid', uid) is None:
        userz.append({'uid':uid, 'uname':uname, 'utype':utype, 'ubd':ubd, 'utext':utext})
        save_userz()
        return True
    return False

def find_user(key, value):
    global userz
    for u in userz:
        if u[key] == value:
            return {'uid':u['uid'], 'uname':u['uname'], 'utype':u['utype'], 'ubd':u['ubd'], 'utext':u['utext']}
    return None

def str_user(u):
    if u == None:
        return ''
    else:
        return str(u['uid']) + ' ' + u['uname'] + ' ' + u['utype'] + ' ' + u['ubd'].strftime('%d-%m-%Y') + ' ' + u['utext']

def usertype_is(uid, utype):
    u = find_user('uid', uid)
    if u != None:
        if u['utype'] == utype:
            return True
    return False

def change_attr(uname, uattr, value):
    u = find_user('uname', uname)
    if u != None:
        u[uattr] = value
        return True
    return False

def list_userz():
    global userz
    luserz = ''
    for u in userz:
        luserz = luserz + str_user(u) + '\n'
    return luserz