#!/usr/bin/env python3
"""Arte "Em trânsito" do repasse (carro sem foto). Uso: foto_transito.py "<titulo>" "<ano · km · cor>" "<R$ preço>" saida.jpg"""
import sys,os
from PIL import Image,ImageDraw,ImageFont
base=os.path.join(os.path.dirname(os.path.abspath(__file__)),'transito_base.jpg')
tit,sub,preco,out=sys.argv[1:5]
im=Image.open(base).convert('RGB'); d=ImageDraw.Draw(im); W,H=im.size
for y in range(384,562):                      # apaga o texto antigo, linha a linha, com a cor do fundo (sem tocar no logo)
    c=im.getpixel((8,y)); d.line([(30,y),(790 if y<505 else 565,y)],fill=c)
F=lambda w,s:ImageFont.truetype(f'/usr/share/fonts/opentype/inter/Inter-{w}.otf',s)
ft=F('Bold',44)
while d.textlength(tit,font=ft)>700 and ft.size>28: ft=F('Bold',ft.size-2)
d.text((52,395),tit,font=ft,fill=(245,245,245))
d.text((52,455),sub,font=F('Regular',24),fill=(170,170,178))
d.text((52,502),preco,font=F('SemiBold',34),fill=(240,196,72))
im.save(out,quality=88)
