
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance as ndld, normalized_damerau_levenshtein_distance_ndarray as ndldn
import talkzstore as ts
from talkzstore import talkz
import numpy as np
import timeit

def search_talk(talk = None):
    if talk == None: return None
    i = 0
    mindist = 1
    minndx = None
    for t in ts.talkz:
        t = t.replace('\n', '')
        tt = t.split(' ')
        npa = np.array(tt)
        d = ndldn(talk, npa)
        if np.amin(d) < mindist:
            mindist = np.amin(d)
            minndx = i
#        print(str(tt) + ' == ' + str(d) + ' min: ' + str(np.amin(d)))
        i += 1
 #       if i > 30: break
    return minndx
#    dldists = normalized_damerau_levenshtein_distance_ndarray(talk, np.ndarray(ts.talkz))
#    print(ts.talkz)
#    print(dldists)
#    i = 0
#    for d in dldists:
#        print('[' + str(i) + '] = ' +str(d))
#        i += 1
#        if i > 30: break

def search_talkz(talk = None, howmuch = 50):
    if talk == None: return None
    i = 0
    talkztuples = [(500, '')]
    for t in ts.talkz:
        t = t.replace('\n', '')
        tt = t.split(' ')
        npa = np.array(tt)
        d = ndldn(talk, npa)
        mind = np.amin(d)
        if mind < 1: talkztuples.append((mind, t))
        i += 1
    l = len(talkztuples) - 1
    if l < 1: return None
    talkztuples = sorted(talkztuples, key=lambda tk: tk[0])
    talkztuples.pop()
    if l < howmuch: howmuch = l
    return talkztuples[0:howmuch]

def add_talk(talk = None):
    if talk == None: return False
    if not isinstance(talk, str): return False
    if len(talk) < 10: return False
    ts.talkz.append(talk + '\n')
    return True

ts.init_talkz()

while True:
    talk = input('@Ikura >')
    if talk == '*': break
    if talk[0:2] == '+ ':
        print(add_talk(talk[2:]))
        continue
#    ndx = search_talk(talk)
#    if ndx == None: print('None!')
#    else: print('[' + str(ndx) + '] ' + ts.talkz[ndx])
    res = search_talkz(talk, 5)
    if res == None: print('None!')
    else: print(res)