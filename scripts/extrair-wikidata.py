import json,urllib.request,urllib.parse,time,urllib.error,re
UA={'User-Agent':'festas-pt-dataset/0.1 (open data compilation)'}
def get(url):
    for i in range(6):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=60))
        except urllib.error.HTTPError as e:
            if e.code in (429,503): time.sleep(20*(i+1)); continue
            raise
D=json.load(open('raw.json'));E,R=D['E'],D['R']
lab=lambda e:(e.get('labels',{}).get('pt') or e.get('labels',{}).get('en') or {}).get('value') or None
desc=lambda e:(e.get('descriptions',{}).get('pt') or e.get('descriptions',{}).get('en') or {}).get('value') or None
def vals(e,p): return [c['mainsnak']['datavalue']['value'] for c in e.get('claims',{}).get(p,[]) if c['mainsnak'].get('datavalue')]
TRAD={'património cultural imaterial','festa','festividades religiosas','feriado','evento recorrente','carnaval','cortejo','festival religioso','romaria','festividade cristã','evento anual','festa popular','festa religiosa','procissão','feira medieval','evento','festival','feira'}
OUTROS={'festival de música','festival de cinema','festival literário','festival de arte','feira do livro','music festival edition','film festival edition','festival occurrence'}
LUGARES={'mercado','edifício','património cultural','capela','igreja','recinto'}
# day-in-year labels
dids={v['id'] for e in E.values() for v in vals(e,'P837')}
DL={}
if dids:
    d=get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode({'action':'wbgetentities','ids':'|'.join(dids),'props':'labels','languages':'pt|en','format':'json'}))
    DL={k:lab(v) for k,v in d['entities'].items()}
fp=lambda f:'https://commons.wikimedia.org/wiki/Special:FilePath/'+urllib.parse.quote(f.replace(' ','_'))
out=[]
for q,e in E.items():
    tipos=[lab(R.get(v['id'],{})) or '' for v in vals(e,'P31')]
    st=set(tipos)
    if not st&(TRAD|OUTROS): continue
    nome=lab(e)
    if not nome or re.search('RTP|Eurovis|Recinto|Mercado Municipal',nome): continue
    if st&LUGARES and not st&(OUTROS|{'festa','festividades religiosas','carnaval','romaria','evento recorrente','património cultural imaterial'}): continue
    grupo='festival' if st&OUTROS else 'tradicional'
    locs=[R.get(v['id'],{}) for v in vals(e,'P276')+vals(e,'P131')]
    coord=vals(e,'P625'); origem='evento' if coord else None
    if not coord:
        for l in locs:
            if vals(l,'P625'): coord=vals(l,'P625'); origem='localidade'; break
    imgs=[fp(i) for i in vals(e,'P18')]
    cat=(vals(e,'P373') or [None])[0]
    if cat and len(imgs)<6:
        d=get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({'action':'query','list':'categorymembers','cmtitle':'Category:'+cat,'cmtype':'file','cmlimit':20,'format':'json'}))
        for m in d['query']['categorymembers']:
            t=m['title'][5:]
            if re.search(r'\.(jpe?g|png|webp)$',t,re.I) and fp(t) not in imgs: imgs.append(fp(t))
            if len(imgs)>=6: break
        time.sleep(1)
    lat=lon=conc=dist=None
    if coord:
        lat,lon=round(coord[0]['latitude'],5),round(coord[0]['longitude'],5)
        a=get(f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=jsonv2&zoom=14&accept-language=pt').get('address',{})
        conc=a.get('municipality') or a.get('city') or a.get('town'); dist=a.get('county') or a.get('state')
        time.sleep(1.1)
    web=(vals(e,'P856') or [None])[0]
    dia=[DL.get(v['id']) for v in vals(e,'P837')]
    out.append({'id':q,'nome':nome,'descricao':desc(e),'grupo':grupo,'tipo':[t for t in tipos if t] or None,
      'localidade':(lab(locs[0]) if locs else None),'concelho':conc,'distrito':dist,
      'lat':lat,'lon':lon,'coord_precisao':origem,
      'data_inicio':None,'data_fim':None,'recorrencia':(', '.join(x for x in dia if x) or None),
      'organizador':None,'site':web,'entrada_livre':None,
      'imagens':imgs[:6] or None,'commons_categoria':('https://commons.wikimedia.org/wiki/Category:'+urllib.parse.quote(cat.replace(' ','_')) if cat else None),
      'fonte':'https://www.wikidata.org/wiki/'+q,'licenca_dados':'CC0 1.0 (Wikidata)',
      'licenca_imagens':('Wikimedia Commons: ver autor e licença na página de cada ficheiro' if imgs else None)})
out.sort(key=lambda r:(r['grupo']!='tradicional',r['nome'].lower()))
json.dump(out,open('festas.json','w'),ensure_ascii=False,indent=2)
gj={'type':'FeatureCollection','features':[{'type':'Feature','id':r['id'],'geometry':({'type':'Point','coordinates':[r['lon'],r['lat']]} if r['lat'] is not None else None),'properties':{k:v for k,v in r.items() if k not in('lat','lon')}} for r in out]}
json.dump(gj,open('festas.geojson','w'),ensure_ascii=False,indent=1)
import csv
with open('festas.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0].keys()));w.writeheader()
    for r in out: w.writerow({k:(' | '.join(v) if isinstance(v,list) else ('' if v is None else v)) for k,v in r.items()})
T=[r for r in out if r['grupo']=='tradicional']
print('total',len(out),'tradicionais',len(T),'com coord',sum(r['lat'] is not None for r in out),'com imagens',sum(bool(r['imagens']) for r in out),'6 imgs',sum(len(r['imagens'] or [])==6 for r in out),'recorrencia',sum(bool(r['recorrencia']) for r in out),'site',sum(bool(r['site']) for r in out))
