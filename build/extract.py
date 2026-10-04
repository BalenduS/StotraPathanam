import re, json
from indic_transliteration import sanscript as S
def body(fn):
    t=open(fn,encoding='utf-8',errors='replace').read()
    return t.split('\\begin{document}',1)[1]
def clean(s):
    s=re.sub(r'\\-[ \t]*\n','-\n',s); s=s.replace('\\-','').replace('\\,','')
    s=re.sub(r'##\s*or\s*##.*','',s)
    s=s.replace('{\\m+}','<GM>')
    return s
def verses_from(text, pat=r'\|\|\s*(\d+)\s*\|\|'):
    # split on markers, keep text before each marker
    out=[];last=0
    for m in re.finditer(pat,text):
        out.append((m.group(1),text[last:m.start()]));last=m.end()
    return out
def lines(chunk):
    ls=[l.strip() for l in chunk.split('\n')]
    ls=[l for l in ls if l and not l.startswith('%') and '##' not in l or (l and l.endswith('##') )]
    return ls
def dev(s):
    s=s.strip()
    d=S.transliterate(s,S.ITRANS,S.DEVANAGARI)
    return d.replace('<GM>','ꣳ').replace('<ग्ं>','ꣳ')
res={}
# Aditya Hrudayam: use stotrapATha section
b=body('ah.itx'); b=b.split('|| atha AdityahR^idayam ||')[1].split('iti AdityahR^idayaM mantram')[0]
b=clean(b)
av=[]
for n,ch in verses_from(b, r'\|\|\s*(\d+)\s*\|\|'):
    ls=[l.strip() for l in ch.split('\n') if l.strip() and 'phalashrutiH' not in l]
    av.append({'n':int(n),'it':ls})
res['aditya']=av
# Guru ashtakam (Shankara)
b=clean(body('gurvashtakam.itx'))
ga=[];cur=[]
blocks=b.split('##')
for blk in blocks:
    if re.search(r'tataH kiM tataH kim|guroraShTakaM',blk):
        ls=[l.strip() for l in blk.split('\n') if l.strip()]
        ga.append(ls)
res['guru']=[{'n':i+1,'it':v} for i,v in enumerate(ga)]
# Bhujangam
b=clean(body('subrabhujanga.itx'))
bv=[]
for blk in b.split('##'):
    if re.search(r'\|\|\s*\d+\s*\|\|',blk):
        ls=[l.strip() for l in blk.split('\n') if l.strip()]
        bv.append(ls)
res['bhujangam']=[{'n':i+1,'it':v} for i,v in enumerate(bv)]
json.dump(res,open('raw.json','w'),ensure_ascii=False,indent=1)
for k,v in res.items():
    print(k,len(v))
    for x in v[:2]+v[-2:]: print('  ',x['n'],x['it'])
