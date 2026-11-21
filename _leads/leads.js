/* Leads das páginas da Grand Brasil (pedido do Maycom em 21/11/2026).
   Ao clicar em "Quero esse", pede nome e WhatsApp antes de abrir a conversa e grava na planilha
   "Leads do site – Seminovos e 0km". Também conta acessos e cliques (aba Acessos). */
(function(){
  var URL_LEADS = "https://script.google.com/macros/s/AKfycbx6OdkygIjYsNgYK2AWgo6wuD80W4P6h9KdAv55JOXOzbBIjTZI2lPd_ayFkNGJQ5ig_w/exec";
  try{ if(new URLSearchParams(location.search).get("disparo")) return; }catch(_){}
  if(!/^https:/.test(URL_LEADS)) return;
  function txt(el){ return el ? el.textContent.replace(/\s+/g," ").trim() : ""; }
  var vend = txt(document.getElementById("v-nome")) || document.title;
  var on = document.querySelector(".lr-nav a.on,.dz-nav a.on");
  var tipo = (/\/0km\//.test(location.pathname) || (on && /0km/i.test(on.textContent))) ? "0km" : "Seminovo";
  var pagina = location.origin + location.pathname;
  function envia(d){
    d.vend = vend; d.tipo = tipo; d.url = pagina;
    var body = new URLSearchParams(d).toString();
    try{
      if(navigator.sendBeacon && navigator.sendBeacon(URL_LEADS, new Blob([body],{type:"application/x-www-form-urlencoded"}))) return;
    }catch(_){}
    try{ fetch(URL_LEADS,{method:"POST",mode:"no-cors",keepalive:true,headers:{"Content-Type":"application/x-www-form-urlencoded"},body:body}); }catch(_){}
  }
  function salvo(){ try{ return JSON.parse(localStorage.getItem("gb_lead")||"null"); }catch(_){ return null; } }
  function guarda(o){ try{ localStorage.setItem("gb_lead", JSON.stringify(o)); }catch(_){} }
  try{ if(!sessionStorage.getItem("gb_ac:"+pagina)){ sessionStorage.setItem("gb_ac:"+pagina,"1"); envia({t:"ev",ev:"acesso"}); } }catch(_){ envia({t:"ev",ev:"acesso"}); }

  var css = document.createElement("style");
  css.textContent = ".gbl-bg{position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:1000;display:flex;align-items:flex-end;justify-content:center;padding:16px}@media(min-width:600px){.gbl-bg{align-items:center}}"
   +".gbl{background:#161618;color:#f4f4f5;border:1px solid #2b2b30;border-radius:18px;padding:22px 20px 18px;width:100%;max-width:420px;font-family:Montserrat,system-ui,sans-serif;box-shadow:0 20px 50px rgba(0,0,0,.5)}"
   +".gbl h3{margin:0 0 4px;font-size:21px;font-weight:800;line-height:1.15}.gbl p{margin:0 0 14px;color:#a6a6ad;font-size:14px}.gbl .car{color:#ffd400;font-weight:700}"
   +".gbl label{display:block;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#a6a6ad;margin:10px 0 4px}"
   +".gbl input{width:100%;box-sizing:border-box;background:#0b0b0c;border:1px solid #2b2b30;border-radius:10px;color:#fff;font:500 16px Montserrat,system-ui,sans-serif;padding:13px 12px;outline:none}.gbl input:focus{border-color:#ffd400}"
   +".gbl .ok{margin-top:16px;width:100%;border:0;border-radius:8px;background:#ffd400;color:#111;font:800 15px Montserrat,system-ui,sans-serif;text-transform:uppercase;letter-spacing:.03em;padding:15px;cursor:pointer}"
   +".gbl .pula{display:block;margin:12px auto 0;background:none;border:0;color:#a6a6ad;font:500 13px Montserrat,system-ui,sans-serif;text-decoration:underline;cursor:pointer}"
   +".gbl .lgpd{margin:10px 0 0;font-size:11px;color:#7d7d85}.gbl .err{color:#ff8a8a;font-size:13px;margin-top:6px;display:none}";
  document.head.appendChild(css);

  function abrir(href){ var w = window.open(href,"_blank","noopener"); if(!w) location.href = href; }
  function carroDe(a){
    var c = a.closest("article,.card"); if(!c) return {carro:"",preco:""};
    var p = c.querySelector(".price"); var pr = p ? txt(p).replace(/^(A partir de|Valor|Preço)\s*/i,"") : "";
    return {carro:[txt(c.querySelector(".brand")),txt(c.querySelector(".name")),txt(c.querySelector(".meta"))].filter(Boolean).join(" · "),preco:pr};
  }
  function modal(info, href){
    var bg = document.createElement("div"); bg.className = "gbl-bg";
    var primeiro = vend.split(" ")[0];
    bg.innerHTML = '<form class="gbl" novalidate><h3>Quase lá!</h3><p>Deixe seu nome e WhatsApp para '+primeiro+' te mandar as condições do <span class="car"></span>.</p>'
      +'<label for="gbl-n">Seu nome</label><input id="gbl-n" name="nome" autocomplete="name" maxlength="80" required>'
      +'<label for="gbl-w">WhatsApp com DDD</label><input id="gbl-w" name="whats" type="tel" inputmode="tel" autocomplete="tel" placeholder="(11) 99999-9999" maxlength="20" required>'
      +'<div class="err">Confira o nome e o WhatsApp com DDD.</div>'
      +'<button class="ok" type="submit">Continuar no WhatsApp</button>'
      +'<p class="lgpd">Ao continuar, você autoriza a Grand Brasil a falar com você sobre este veículo.</p>'
      +'<button class="pula" type="button">Prefiro só abrir o WhatsApp</button></form>';
    bg.querySelector(".car").textContent = info.carro.split(" · ").slice(0,2).join(" ") || "carro";
    document.body.appendChild(bg);
    var f = bg.querySelector("form"); setTimeout(function(){ f.nome.focus(); }, 50);
    function fecha(){ bg.remove(); }
    bg.addEventListener("click", function(e){ if(e.target === bg) fecha(); });
    bg.querySelector(".pula").addEventListener("click", function(){ fecha(); abrir(href); });
    f.addEventListener("submit", function(e){
      e.preventDefault();
      var nome = f.nome.value.trim(), zap = f.whats.value.replace(/\D/g,"");
      if(nome.length < 2 || zap.length < 10){ bg.querySelector(".err").style.display = "block"; return; }
      guarda({nome:nome, whats:zap});
      envia({t:"lead", nome:nome, whats:zap, carro:info.carro, preco:info.preco});
      fecha(); abrir(href);
    });
  }
  document.addEventListener("click", function(e){
    var a = e.target.closest && e.target.closest('a[href*="wa.me/"]');
    if(!a || !a.closest("article,.card") || !/quero/i.test(a.textContent)) return;
    var info = carroDe(a);
    envia({t:"ev", ev:"clique", carro:info.carro});
    var s = salvo();
    if(s && s.nome && s.whats){ envia({t:"lead", nome:s.nome, whats:s.whats, carro:info.carro, preco:info.preco}); return; }
    e.preventDefault(); e.stopPropagation();
    modal(info, a.href);
  }, true);
})();
