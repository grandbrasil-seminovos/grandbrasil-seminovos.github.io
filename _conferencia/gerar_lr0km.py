#!/usr/bin/env python3
"""Gera a página Land Rover 0km de cada vendedora a partir do modelo da Michele (Denza).
Uso: python3 gerar_lr0km.py <michele/index.html> <lr_imgs.json> <raiz do repo>"""
import json,re,sys,html
from urllib.parse import quote
tpl,imgs,root=sys.argv[1],json.load(open(sys.argv[2])),sys.argv[3]
T=open(tpl).read()
head=T[:T.index('<body>')+len('<body>')]
svg=T[T.index('<svg width="0"'):T.index('</svg>',T.index('<svg width="0"'))+6]
MOD=[
 dict(id="rr",nome="Range Rover",tipo="O SUV de luxo original, feito no Reino Unido",ano="0km",preco=1773950,foto="rr",specs=["Tração integral","Suspensão pneumática","Versões híbridas plug-in","Projetado e fabricado no Reino Unido"]),
 dict(id="rrs",nome="Range Rover Sport",tipo="Esportividade com luxo · versão Dynamic",ano="0km · 2027",preco=1063950,foto="rrs",specs=["Tração integral","Suspensão pneumática","Versões diesel e híbrida plug-in","Range Rover Sport Dynamic 2027"]),
 dict(id="velar",nome="Range Rover Velar",tipo="Design minimalista · Autobiography",ano="0km · 2026",preco=773069,foto="velar",specs=["Híbrido plug-in P400e","Tração integral","Acabamento Autobiography","Range Rover Velar 2026"]),
 dict(id="def130",nome="Defender 130",tipo="O Defender com até 8 lugares",ano="0km · 2026",preco=969990,foto="def130",specs=["3.0 D350 diesel MHEV","Tração 4x4","Até 8 lugares","Versão Defender 130 X"]),
 dict(id="def110",nome="Defender 110",tipo="O off-road icônico, 5 portas",ano="0km · 2026",preco=844990,foto="def110",specs=["3.0 D350 diesel MHEV","Tração 4x4","5 portas","Versão X-Dynamic HSE"]),
 dict(id="def90",nome="Defender 90",tipo="O off-road icônico, 3 portas",ano="0km · 2026",preco=799490,foto="def90",specs=["3.0 D350 diesel MHEV","Tração 4x4","3 portas","Versão X-Dynamic HSE"]),
 dict(id="disco",nome="Discovery",tipo="7 lugares para a família e para a aventura",ano="0km · 2026",preco=797990,foto="disco",specs=["3.0 D350 diesel MHEV","7 lugares","Tração 4x4","Metropolitan Edition"]),
 dict(id="dsport",nome="Discovery Sport",tipo="SUV compacto premium · edição Landmark",ano="0km · 2026",preco=None,foto="dsport",specs=["2.0 P250 flex","Tração 4x4","Até 7 lugares (5+2)","Nova edição Landmark"]),
]
VEND=[dict(slug="debora",nome="Débora Cohen",primeiro="Débora",cargo="Executiva de Vendas",fone="5511989518590",fonefmt="(11) 98951-8590",ig="jlr.grandbrasil.deborah"),
      dict(slug="sandraferreira",nome="Sandra Ferreira",primeiro="Sandra",cargo="Executiva de Vendas",fone="5511982024122",fonefmt="(11) 98202-4122",ig="jlr.grandbrasil_sandraferreira")]
brl=lambda n:"R$ "+f"{n:,.0f}".replace(",",".")
gb=re.search(r'class="gblogo" src="(data:image/png;base64,[^"]+)"',T).group(1)
LR='<svg class="lr-logo" viewBox="0 0 220 24" role="img" aria-label="Land Rover"><text x="0" y="19" fill="#fff" font-family="Montserrat,Arial,sans-serif" font-weight="700" font-size="19" letter-spacing="5">LAND ROVER</text></svg>'
CSS='''<style>
.lr-nav{display:flex;gap:6px;margin:14px 0 4px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:12px;padding:5px;width:max-content;max-width:100%}.lr-nav a{padding:10px 18px;border-radius:8px;font-weight:800;text-transform:uppercase;letter-spacing:.04em;font-size:14px;color:#fff;text-decoration:none;white-space:nowrap}.lr-nav a.on{background:#ffd400;color:#111}@media(max-width:520px){.lr-nav{width:100%}.lr-nav a{flex:1;text-align:center;padding:10px 8px;font-size:13px}}
.lr-logos{display:inline-flex;align-items:center;gap:16px;flex-wrap:wrap}.lr-sep{width:1px;height:32px;background:rgba(255,255,255,.35)}.lr-logo{height:20px;width:auto}
@media(max-width:520px){.lr-logos{gap:10px}.lr-logos .gblogo{width:140px;height:auto}.lr-logo{height:14px}.lr-sep{height:22px}}
.lr-tag{position:absolute;top:12px;left:12px;background:var(--accent,#ffd400);color:#111;font-weight:800;font-size:12px;letter-spacing:.06em;text-transform:uppercase;padding:6px 10px;border-radius:8px}
.card .photo img{aspect-ratio:16/10;object-fit:cover;width:100%}
.lr-cons{font-family:var(--display);font-weight:800;font-size:24px;line-height:1.1}
</style>'''
for v in VEND:
    w=lambda t:"https://wa.me/"+v['fone']+"?text="+quote(t)
    cards=[]
    for m in MOD:
        preco=f'<div class="price"><small>A partir de</small>{brl(m["preco"])}</div>' if m['preco'] else '<div class="price"><small>Preço</small><span class="lr-cons">Consulte condições</span></div>'
        cards.append(f'''<article class="card" data-id="{m['id']}">
      <div class="photo"><img src="{imgs[m['foto']]}" alt="Land Rover {html.escape(m['nome'])}" loading="lazy"><span class="lr-tag">0km</span></div>
      <div class="body">
        <div class="top"><span class="brand">Land Rover</span><span class="meta">{m['ano']}</span></div>
        <h2 class="name">{html.escape(m['nome'])}</h2>
        <p class="perks" style="margin-top:4px">{html.escape(m['tipo'])}</p>
        <ul class="specs">{''.join(f"<li>{html.escape(s)}</li>" for s in m['specs'])}</ul>
        <div class="foot">
          {preco}
          <div class="actions">
            <a class="btn btn-wa" href="{w(f"Olá {v['primeiro']}! Tenho interesse no Land Rover {m['nome']} 0km. Pode me passar condições e disponibilidade?")}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>Quero esse</a>
            <a class="btn btn-line" href="{w(f"Olá {v['primeiro']}! Quero agendar um test drive do Land Rover {m['nome']}.")}" target="_blank" rel="noopener">Test drive</a>
          </div>
        </div>
      </div></article>''')
    page=head.replace('Denza 0km em Alphaville com Michele Nakano, Consultora de Vendas. B5, Z9 GT e D9. Chame no WhatsApp.',f"Land Rover 0km com {v['nome']}, {v['cargo']} da Grand Brasil. Range Rover, Defender e Discovery. Chame no WhatsApp.")
    page=page.replace('Denza Alphaville · Michele Nakano',f"Land Rover 0km · {v['nome']}").replace('Denza 0km: B5, Z9 GT e D9. Pronta entrega e pré-venda.','Land Rover 0km: Range Rover, Defender e Discovery.')
    page=page.replace('</head>',CSS+'\n</head>')
    page+=f'''
{svg}
<section class="hero pad">
  <div class="inner">
    <div class="brandbar"><span class="lr-logos"><img class="gblogo" src="{gb}" alt="Grand Brasil" width="208" height="50"><i class="lr-sep"></i>{LR}</span><span class="loc">Alphaville · São Paulo</span></div>
    <nav class="lr-nav" aria-label="Páginas"><a class="on" href="./">Land Rover 0km</a><a href="../">Seminovos</a></nav>
    <h1>Land Rover 0km<span>Range Rover · Defender · Discovery</span></h1>
    <div class="consultor"><span class="ci"><b id="v-nome">{v['nome']}</b><em id="v-cargo">{v['cargo']}</em></span></div>
    <p>Conheça a linha Land Rover 0km. Escolha o seu modelo e fale comigo direto no WhatsApp para condições, disponibilidade e test drive.</p>
    <div class="ctas">
      <a class="btn btn-wa" href="{w(f"Olá {v['primeiro']}! Vi o catálogo Land Rover 0km e quero saber mais.")}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>Chamar no WhatsApp</a>
      <a class="btn btn-ig" href="{w(f"Olá {v['primeiro']}! Quero agendar um test drive Land Rover.")}" target="_blank" rel="noopener">Agendar test drive</a>
      <a class="btn btn-line" href="../" style="border:1px solid rgba(255,255,255,.35);color:#fff">Ver seminovos</a>
    </div>
  </div>
</section>
<main class="pad">
  <div class="inner">
    <div class="grid" id="grid">
      {''.join(cards)}
    </div>
    <section class="troca" aria-label="Avaliar meu carro na troca">
      <div class="ico"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7h11l-3-3M17 17H6l3 3" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
      <div><h2>Tem um veículo na troca?</h2><p>Me manda modelo, ano e km pelo WhatsApp que eu faço a avaliação do seu carro.</p></div>
      <a class="btn btn-wa" href="{w(f"Olá {v['primeiro']}! Quero avaliar meu carro na troca por um Land Rover 0km. Modelo/ano/km: ")}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>Avaliar meu carro</a>
    </section>
    <section class="follow" aria-label="Siga no Instagram">
      <div class="ring"><span><svg><use href="#i-ig"/></svg></span></div>
      <div><h2>Siga no Instagram</h2><p><b style="color:var(--ig)">@{v['ig']}</b><br>Novidades Land Rover, carros em estoque e condições especiais.</p></div>
      <a class="btn btn-igsolid" href="https://www.instagram.com/{v['ig']}/" target="_blank" rel="noopener"><svg><use href="#i-ig"/></svg>Seguir</a>
    </section>
  </div>
</main>
<footer class="pad">
  <div class="inner">
    <span>WhatsApp: <span class="num">{v['fonefmt']}</span></span>
    <span>Land Rover · Grand Brasil · Alphaville, Barueri – SP</span>
    <span>Preços "a partir de" conforme o site oficial da Land Rover Brasil em 21/11/2026, para a versão indicada em cada modelo. Valores, versões e disponibilidade sujeitos a alteração. Fotos ilustrativas.</span>
  </div>
</footer>
<a class="fab" href="{w(f"Olá {v['primeiro']}! Vi o catálogo Land Rover 0km e quero saber mais.")}" target="_blank" rel="noopener" aria-label="Chamar no WhatsApp"><svg><use href="#i-wa"/></svg><span class="lbl">Fale comigo</span></a>
</body>
</html>
'''
    import os; os.makedirs(f"{root}/{v['slug']}/0km",exist_ok=True)
    open(f"{root}/{v['slug']}/0km/index.html","w").write(page)
    # aba na página de seminovos
    sp=f"{root}/{v['slug']}/index.html"; s=open(sp).read()
    if 'lr-nav' not in s:
        nav='<style>.lr-nav{display:flex;gap:6px;margin:14px 0 4px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:12px;padding:5px;width:max-content;max-width:100%}.lr-nav a{padding:10px 18px;border-radius:8px;font-weight:800;text-transform:uppercase;letter-spacing:.04em;font-size:14px;color:#fff;text-decoration:none;white-space:nowrap}.lr-nav a.on{background:#ffd400;color:#111}@media(max-width:520px){.lr-nav{width:100%}.lr-nav a{flex:1;text-align:center;padding:10px 8px;font-size:13px}}</style>'
        s=s.replace('</head>',nav+'\n</head>',1)
        i=s.index('<div class="brandbar">'); j=s.index('</div>',i)+6
        s=s[:j]+'\n    <nav class="lr-nav" aria-label="Páginas"><a href="0km/">Land Rover 0km</a><a class="on" href="./">Seminovos</a></nav>'+s[j:]
        open(sp,'w').write(s)
    print('ok',v['slug'],len(page))
