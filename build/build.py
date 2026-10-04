import re, json
from indic_transliteration import sanscript as S
from m_guru import GURU; from m_aditya import ADITYA; from m_bhujangam import BHUJ
from m_rudram import *
from m_shambhu import SHAMBHU
raw=json.load(open('raw.json')); rr=json.load(open('rudram_raw.json'))
FIX=[('.h',''),('\\','')]
def prep(s):
    s=s.strip()
    s=re.sub(r'(\|\||\.\.)\s*\d*\s*(\|\||\.\.)\s*$','',s)   # trailing verse number
    s=re.sub(r'\|\|$','',s).strip()
    s=re.sub(r'\s\.\.$',' ||',s); s=re.sub(r'\s\.$',' |',s)
    for a,b in FIX: s=s.replace(a,b)
    s=s.replace('<GM>','\u0001')
    return re.sub(r'\s+',' ',s).strip()
def dev(s):
    d=S.transliterate(prep(s),S.ITRANS,S.DEVANAGARI)
    return d.replace('\u0001','ग्ं').replace(' -','-')
def tel(d):
    return S.transliterate(d,S.DEVANAGARI,S.TELUGU)
def num(n,last=True):
    d=S.transliterate(str(n),S.ITRANS,S.DEVANAGARI); return '॥ '+d+' ॥'
def mkunit(lines,label,meaning,gl=None,numlabel=None):
    dl=[dev(l) for l in lines if prep(l)]
    if numlabel is not None: dl[-1]=dl[-1].rstrip(' ।|॥')+' '+numlabel
    u={'label':label,'dev':dl,'tel':[tel(x) for x in dl],'m':meaning}
    if gl: u['g']=[{'dev':dev(w),'tel':tel(dev(w)),'m':m} for w,m in gl]
    return u
out=[]
# Guru
units=[]
for i,(r,(m,g)) in enumerate(zip(raw['guru'],GURU['v'])):
    lab='Verse %d'%(i+1) if i<8 else 'Phalashruti'
    units.append(mkunit(r['it'],lab,m,g,num(i+1) if i<8 else '॥'))
out.append({'id':'guru','name':'Guru Ashtakam','dev':'गुर्वष्टकम्','tel':'గుర్వష్టకమ్','by':'Adi Shankaracharya','intro':GURU['intro'],'refrain':GURU['refrain'],'groups':[{'name':'Verses','units':units}]})
# Aditya
units=[]
for i,(r,(m,g)) in enumerate(zip(raw['aditya'],ADITYA['v'])):
    units.append(mkunit(r['it'],'Verse %d'%(i+1),m,g,num(i+1)))
grp=[{'name':'Setting · 1–5','units':units[:5]},{'name':'The hymn · 6–24','units':units[5:24]},{'name':'Result · 25–31','units':units[24:]}]
out.append({'id':'aditya','name':'Aditya Hrudayam','dev':'आदित्यहृदयम्','tel':'ఆదిత్యహృదయమ్','by':'Valmiki Ramayana, Yuddha Kanda','intro':ADITYA['intro'],'groups':grp})
# Bhujangam
bj=[r for r in raw['bhujangam'] if not any('chapter' in l for l in r['it'])]
assert len(bj)==33,len(bj)
units=[]
for i,(r,(m,g)) in enumerate(zip(bj,BHUJ['v'])):
    units.append(mkunit(r['it'],'Verse %d'%(i+1),m,g,num(i+1)))
grp=[{'name':'Invocation · 1–7','units':units[:7]},{'name':'Form of the Lord · 8–19','units':units[7:19]},{'name':'Prayers · 20–33','units':units[19:]}]
out.append({'id':'bhujangam','name':'Karthikeya Bhujangam','dev':'सुब्रह्मण्यभुजङ्गम्','tel':'సుబ్రహ్మణ్యభుజఙ్గమ్','by':'Adi Shankaracharya','intro':BHUJ['intro'],'note':'Also known as Subrahmanya Bhujangam.','groups':grp})
# Rudram
def reflow(u):
    t=' '.join(u['dev'])
    parts=re.split(r'(?<=\sमे)\s|(?<=।)\s',t)
    lines=[];cur=''
    for p in parts:
        cur=(cur+' '+p).strip()
        if cur.count(' मे')>=2 or len(cur)>48 or cur.endswith('।'): lines.append(cur);cur=''
    if cur: lines.append(cur)
    if lines[-1].startswith('॥'):
        last=lines.pop(); lines[-1]=lines[-1]+' '+last
    u['dev']=lines;u['tel']=[tel(x) for x in lines];return u
grps=[]
cur={}
for u in rr['namakam']:
    a,s=u['a'],u['s']
    if a==2 and s==0: a,s=1,16
    key=(a,s)
    cur.setdefault(a,[]).append(mkunit(u['it'],'%d.%d'%(a,s),NAMAKAM[key],numlabel='॥'))
for a in range(1,12):
    grps.append({'name':'Namakam · Anuvaka %d'%a,'theme':ANUVAKA_THEMES[a],'units':cur[a]})
grps[-1]['units']+= [mkunit(c,'Closing %d'%(i+1),CLOSING[i],numlabel='॥') for i,c in enumerate(rr['closing'])]
ch=[reflow(mkunit(c,'Anuvaka %d'%(i+1),CHAMAKAM[i],numlabel=num(i+1))) for i,c in enumerate(rr['chamakam'])]
ch.append(mkunit(rr['chtail'],'Closing',CHAMAKAM_CLOSING,numlabel='॥'))
grps.append({'name':'Chamakam','theme':"The 'cha me' prayer: eleven anuvakas asking for every good thing in life, and that all of it be offered back in sacrifice.",'units':ch})
out.append({'id':'rudram','name':'Sri Rudram','dev':'श्रीरुद्रम्','tel':'శ్రీరుద్రమ్','by':'Krishna Yajur Veda, Taittiriya Samhita','intro':RUDRAM_INTRO,'groups':grps})
# Shambhu Stuti
units=[]
for i,(r,(m,g)) in enumerate(zip(raw['shambhu'],SHAMBHU['v'])):
    units.append(mkunit(r['it'],'Verse %d'%(i+1),m,g,num(i+1)))
out.append({'id':'shambhu','name':'Shiva Stuti','dev':'शम्भुस्तुतिः','tel':'శమ్భుస్తుతిః','by':'Shri Rama · Brahma Purana','intro':SHAMBHU['intro'],'note':'Also known as Shambhu Stuti or Rama-krita Shiva Stotram.','groups':[{'name':'Verses','units':units}]})
# reorder: Rudram, Guru, Aditya, Bhujangam (user's order)
order={'rudram':0,'guru':1,'aditya':2,'bhujangam':3,'shambhu':4}
out.sort(key=lambda x:order[x['id']])
json.dump(out,open('data.json','w'),ensure_ascii=False,separators=(',',':'))
for s in out:
    print(s['id'],sum(len(g['units']) for g in s['groups']))
