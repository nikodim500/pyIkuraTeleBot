
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance as ndld, normalized_damerau_levenshtein_distance_ndarray as ndldn
import talkzstore as ts
import numpy as np


def can_answer(chat_id):
    return ts.read_conf(chat_id) == 1

def can_talk(chat_id):
    return ts.read_conf(chat_id) == 2

def init():
    ts.init_talkz()

last_message = (-1, '')

def compare_talk(talk = None):
    if talk is None: return (-1, 1)
    mindist = 1
    minndx = -1
    i = 0
    for t in ts.talkz:
        t = t.replace('\n', '')
        d = ndld(talk, t)
        if d < mindist:
            mindist = d
            minndx = i
        i += 1
    return (minndx, mindist)

def search_talk(talk = None):
    global last_message
    if talk is None: return 'хуй'
    i = 0
    mindist = 1
    minndx = -1
    for t in ts.talkz:
        t = t.replace('\n', '')
        tt = t.split(' ')
        npa = np.array(tt)
        d = ndldn(talk, npa)
        if np.amin(d) < mindist:
            mindist = np.amin(d)
            minndx = i
        i += 1
    if minndx > -1: last_message = (minndx, ts.talkz[minndx])
    return ts.talkz[minndx]

def search_talkz(talk = None, howmuch = 50):
    if talk is None: return [(-500, "низуя не ношол", '')]
    i = 0
    talkztuples = [(500, '', '')]
    for t in ts.talkz:
#        t = t.replace('\n', '')
        tt = t.split(' ')
        npa = np.array(tt)
        d = ndldn(talk, npa)
        mini = np.argmin(d)
        mind = d[mini]
        if mind < 1: talkztuples.append((mind, t, tt[mini]))
        i += 1
    l = len(talkztuples) - 1
    if l < 1: return [(-500, "низуя не ношол", '')]
    talkztuples = sorted(talkztuples, key=lambda tk: tk[0])
    talkztuples.pop()
    if l < howmuch: howmuch = l
    return talkztuples[0:howmuch]

def add_talk(talk = None):
    if talk is None: return (False, '')
    if not isinstance(talk, str): return False
    if len(talk) < 10: return (False, '')
    sch = compare_talk(talk)
    print ('index: ' + str(sch[0]) + '  dist ' + str(sch[1]))
    if sch[1] < 0.5: return (False, ts.talkz[sch[0]])
    ts.talkz.append(talk + '\n')
    ts.save_talkz()
    return (True, '')

def del_talk(talk_index = None):
    if talk_index >=0 and talk_index < len(ts.talkz):
        res = ts.talkz.pop(talk_index)
        ts.save_talkz()
        return res



