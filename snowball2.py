# -*- coding: UTF-8 -*-
import codecs, wikipedia, sys
langs = ['en', 'el']
with codecs.open('/data/project/dexbot/pywikipedia-git/snowball2_%s_%s.txt' % (langs[0], langs[1]), 'r', 'utf-8') as f:
    aa = f.read().split('\n')
with codecs.open('/data/project/dexbot/pywikipedia-git/snowball_%s_%s.txt' % (langs[0], langs[1]), 'r', 'utf-8') as f:
    the_dict = eval(f.read())
def sep(lang):
    if lang == 'ja':
       return u'・'
    if lang == 'zh':
       return u'·'
    return ' '
nc = '--nc' in '|'.join(sys.argv)
for name in aa:
    if not name:
        continue
    print name
    data = wikipedia.DataPage(int(name.split('Q')[1]))
    try:
        items = data.get()
    except:
        continue
    P31 = []
    P27 = []
    for claim in items['claims']:
        if claim['m'][1] == 31:
            try:
                P31.append(claim['m'][3]['numeric-id'])
            except:
                pass
        if claim['m'][1] == 27:
            try:
                P27.append(claim['m'][3]['numeric-id'])
            except:
                pass
    if not 5 in P31:
        continue
    if len(P27) != 1 and not nc:
        continue
    label_dict = {}
    for lang in langs:
        if lang in items['label']:
            label_dict[lang] = items['label'][lang]
    if not len(label_dict) == 1:
        if ' ' in label_dict.get('ja',''):
            pass
        else:
            continue
    label_dict = {}
    for lang in langs:
        if lang + 'wiki' in items['links']:
            label_dict[lang] = items['links'][lang + 'wiki']['name'].split(" (")[0]
    if not len(label_dict) == 1:
        continue
    cons = ''
    lang2 = None
    if nc:
        P27 = [1]
    for lang in label_dict:
        for word in label_dict[lang].split(sep(lang)):
            if (word, lang, P27[0]) in the_dict:
                lang2 = the_dict[(word, lang, P27[0])][1]
                cons += the_dict[(word, lang, P27[0])][0] + sep(lang2)
            else:
                cons += 'SKIP '
    if not cons or 'SKIP ' in cons:
        continue
    data.setitem(summary='Bot: Auto-transliteration for %s based on %s: %s' % (lang2, lang, cons[:-1]),
                 items={'type': u'item', 'label': lang2, 'value': cons[:-1]})
