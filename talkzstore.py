
talkz = None

def init_talkz():
    global talkz
    tf = open('talkz.tdb', 'r', encoding='utf-8')
    talkz = tf.readlines()
    tf.close()
    print(len(talkz))

def save_talkz():
    global talkz
    tf = open('talkz.tdb', 'w')
    tf.writelines(talkz)
    tf.close()