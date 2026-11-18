#!/usr/bin/env python3
"""Edita a lista CARS do site do Maycom (maycomrebolo.github.io/index.html).
Uso: python3 editar.py <index.html> <mudancas.json>
mudancas.json = {"remover":[ids], "precos":{id:preco}, "capas":{id:"data:image/jpeg;base64,..."},
                 "novos":[{id,src,brand,name,year,km,price,tag,specs,bmw,img}]}
Depois: conferir com node que CARS carrega, commit e push; e trocar o bloco CARS do artifact
https://claude.ai/artifact/D64vw943yHECKHxyAVisSz pelo bloco novo (ler a versão publicada antes)."""
import json,re,sys
p,m=sys.argv[1],json.load(open(sys.argv[2]))
s=open(p).read()
for k in m.get('remover',[]):
    s,n=re.subn(r'\n[ \t]*\{id:"%s",[^\n]*'%re.escape(k),'',s); assert n==1,k
for k,v in m.get('precos',{}).items():
    s,n=re.subn(r'(\{id:"%s",[^\n]*?price:)\d+'%re.escape(k),r'\g<1>%d'%v,s); assert n==1,k
for k,v in m.get('capas',{}).items():
    s,n=re.subn(r'(\{id:"%s",[^\n]*?img:)"data:[^"]*"'%re.escape(k),lambda x:x.group(1)+json.dumps(v),s); assert n==1,k
for c in m.get('novos',[]):
    assert c['src'] not in s and f'id:"{c["id"]}"' not in s, c['id']
    J=lambda x:json.dumps(x,ensure_ascii=False)
    e='{id:%s,src:%s,brand:%s,name:%s,year:%s,km:%d,price:%d,tag:%s,specs:%s,ig:%s,bmw:%s,img:%s},'%(J(c['id']),J(c['src']),J(c['brand']),J(c['name']),J(c['year']),c['km'],c['price'],J(c.get('tag','')),J(c['specs']),J(c['src']),'true' if c.get('bmw') else 'false',J(c['img']))
    s=s.replace('const CARS = [\n','const CARS = [\n '+e+'\n',1)
open(p,'w').write(s); print(s.count('{id:"'),'carros')
