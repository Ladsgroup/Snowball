# -*- coding: UTF-8 -*-
import wikipedia, xmlreader, codecs, re, json, sys
dump = xmlreader.XmlDump("/data/project/dexbot/pywikipedia-git/wikidatawiki-20150603-pages-articles.xml.bz2")
langs = ['en', 'fa']
a = 0
db = {}
with codecs.open('/data/project/dexbot/pywikipedia-git/snowball2_%s_%s.txt' % (langs[0], langs[1]),'w','utf-8') as f:
    f.write('')
def sep(lang):
    if lang == 'ja':
       return u'・'
    if lang == 'zh':
       return u'·'
    return ' '
   
def _make_old_dict(_contents):
        """Convert the new dictionary to the old one for consistency."""
        if isinstance(_contents.get('claims', {}), list) and not _contents.get('sitelinks'):
            return _contents
        old_dict = _contents
        new_dict = {
            'links': {}, 'claims': [], 'description': old_dict.get('descriptions', []),
            'label': {}}
        for site_name in old_dict.get('sitelinks', []):
            new_dict['links'][site_name] = {
                'name': old_dict['sitelinks'][site_name].get('title'),
                'badges': old_dict['sitelinks'][site_name].get('badges', [])
            }
        for claim_name in old_dict.get('claims', []):
            for claim in old_dict['claims'][claim_name]:
                new_claim = {'m': ['value', int(claim_name[1:]), 'value']}
                new_claim['refs'] = claim.get('references', [])
                new_claim['g'] = claim['id']
                new_claim['q'] = claim.get('qualifiers', [])
                new_claim['m'].append(claim.get('mainsnak', {}).get('datavalue', {}).get('value'))
                new_dict['claims'].append(new_claim)
        for label in old_dict.get('labels', {}):
            new_dict['label'][label] = old_dict['labels'][label]['value']
        return new_dict
if '-nc' in '|'.join(sys.argv):
    country_check = False
else:
    country_check = True
for entry in dump.new_parse():
    if entry.ns == '0':
        if entry.title.endswith('00'):
            print entry.title
        items = json.loads(entry.text)
        items = _make_old_dict(items)
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
        if len(P27) != 1 and country_check:
            continue
        label_dict = {}
        for lang in langs:
            if lang + 'wiki' in items['links']:
                label_dict[lang] = items['links'][lang + 'wiki']['name'].split(" (")[0]
        if not label_dict:
            continue
        if len(label_dict) == 1:
            with codecs.open('/data/project/dexbot/pywikipedia-git/snowball2_%s_%s.txt' % (langs[0], langs[1]),'a','utf-8') as f:
               f.write('%s\n' % entry.title)
        lengths = []
        for lang in label_dict:
            lengths.append(len(label_dict[lang].split(sep(lang))))
        lengths = set(lengths)
        if len(lengths) != 1:
            continue
        for lang in label_dict:
            for name2 in label_dict[lang].split(sep(lang)):
                if country_check:
                    if (name2, lang, P27[0]) not in db:
                        db[(name2, lang, P27[0])] = set()
                    db[(name2, lang, P27[0])].add(entry.title)
                else:
                    if (name2, lang, 1) not in db:
                        db[(name2, lang, 1)] = set()
                    db[(name2, lang, 1)].add(entry.title)
res = {}
db_nee = {}
#with codecs.open('/data/project/dexbot/pywikipedia-git/snowball_test.txt','w','utf-8') as f:
#    f.write(str(db))
for s in db:
    if s in res:
        continue
    fv = {}
    for l in db:
        if l[1] == s[1]:
            continue
        nn = len(db[l].intersection(db[s]))
        if nn == 0:
            continue
        if l[2] != s[2]:
            continue
        fv[l] = nn
    if not fv:
        continue
    a = fv.values()
    a.sort()
    a.reverse()
    if a[0] < 5:
        continue
    if a[0] == 1 or a[0] == a[1]:
        continue
    for i in fv:
        if fv[i] == a[0]:
            rrr = i
    # NEVER EVER DO THIS:
    #res[rrr] = s
    res[s] = rrr

with codecs.open('/data/project/dexbot/pywikipedia-git/snowball_%s_%s.txt' % (langs[0], langs[1]),'w','utf-8') as f:
    f.write(str(res))

