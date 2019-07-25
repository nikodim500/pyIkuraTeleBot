
import os
import pickle

talkz = None
talkz_file = ''
tconf = None
talkz_conf = ''

def init_talkz():
    global talkz
    global talkz_file
    global tconf
    global talkz_conf

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    talkz_file = os.path.join(THIS_FOLDER, '-dbs', 'talkz.tdb')
    tf = open(talkz_file, 'r', encoding='utf-8')
    talkz = tf.readlines()
    tf.close()
    talkz = [t.replace('\n', '') for t in talkz]

    talkz_conf = os.path.join(THIS_FOLDER, '-dbs', 'talkz.cfg')
    tconf = pickle.load(open(talkz_conf, 'rb'))
    print(tconf)

def save_talkz():
    global talkz
    global talkz_file
    tlkz = [t + '\n' for t in talkz]
    tf = open(talkz_file, 'w')
    tf.writelines(tlkz)
    tf.close()
    print('Talkz.db saved')

def read_conf(key):
    global tconf
    try:
        return tconf[key]
    except:
        return 0