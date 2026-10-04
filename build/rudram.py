import re, json
t=open('rudram.itx',encoding='utf-8').read()
nam=t.split('|| OM namo bhagavate rudrAya ||')[1].split('\\section{|| chamakaprashnaH ||}')[0]
cham=t.split('\\section{|| chamakaprashnaH ||}')[1].split('##')[0]
fixes=[('girisha~njtA','girishantA'),('girisha~njta','girishanta'),('~nj','M'),('{\\m+}','<GM>'),
('vruNaktu','vR^iNaktu'),('mruDA','mR^iDA'),('mruDaya','mR^iDaya'),('mrugayubhyaH','mR^igayubhyaH'),
('grutsapatibhyashcha','gR^itsapatibhyashcha'),('vrukSha','vR^ikSha'),('utta pUruShaghne','uta pUruShaghne'),
('teShAsahasrayojane','teShA<GM> sahasrayojane'),('devAnA hR^idayebhyo','devAnA<GM> hR^idayebhyo'),
('.aya shivAbhimarshanaH','.aya<GM> shivAbhimarshanaH'),('dhanustva sahasrAkSha','dhanustva<GM> sahasrAkSha'),
('vibhradAgahi','bibhradAgahi'),('imArudrAya','imA rudrAya'),('ye chemArudrA','ye chemA<GM> rudrA'),
('rudrotano','rudrota no'),('namH ','namaH '),('nam UrmyAya','nama UrmyAya'),('pAt_nIvatashcha','pAtnIvatashcha'),
('paribbhuja','paribhuja'),('pariNo','pari No'),('stiShThadbhyo','stiShThadbhyo'),('  ',' '),
('mAnastoke','mA nastoke'),('ArAtte goghna','ArAtte goghna'),('mR^iganna','mR^igaM na'),('gahvareShThAya','gahvareShThAya'),
('Akhkhidate cha prakhkhidate','Akkhidate cha prakkhidate'),('chatvari{','chatvAri{'),('udahAryaH','udahAryaH')]
def fx(s):
    for a,b in fixes: s=s.replace(a,b)
    return s
nam=fx(nam); cham=fx(cham)
units=[]
last=0
for m in re.finditer(r'\|\|\s*(\d+)\\\.(\d+)\|\|',nam):
    txt=nam[last:m.start()]; last=m.end()
    units.append({'a':int(m.group(1)),'s':int(m.group(2)),'it':[l.strip() for l in txt.strip().split('\n') if l.strip()]})
tail=nam[last:]
closing=[]
l2=0
for m in re.finditer(r'\|\|\s*(\d+)\|\|',tail):
    txt=tail[l2:m.start()]; l2=m.end()
    closing.append([l.strip() for l in txt.strip().split('\n') if l.strip()])
ch=[];l3=0
for m in re.finditer(r'\|\|\s*(\d+)\|\|',cham):
    txt=cham[l3:m.start()]; l3=m.end()
    ch.append([l.strip() for l in txt.strip().split('\n') if l.strip()])
chtail=[l.strip() for l in cham[l3:].split('OM shAntiH')[0].strip().split('\n') if l.strip()]
json.dump({'namakam':units,'closing':closing,'chamakam':ch,'chtail':chtail},open('rudram_raw.json','w'),ensure_ascii=False,indent=1)
print(len(units),len(closing),len(ch)); print([ (u['a'],u['s']) for u in units]); print(closing[-1]); print(chtail)
print(re.findall(r'~n?j?\w*',nam)[:20])
