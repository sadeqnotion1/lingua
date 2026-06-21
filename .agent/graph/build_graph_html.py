"""Regenerate backend/docs/graph.html from backend/docs/graph.json.

Produces a self-contained (no-CDN) interactive force-directed view: color by
community, click a node for details, search/filter. Run after updating the graph:

    python backend/tools/build_graph_html.py
"""
import json
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"
GRAPH_JSON = DOCS / "graph.json"
GRAPH_HTML = DOCS / "graph.html"

TEMPLATE = """<!doctype html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\"/>
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"/>
<title>__REPO__ — Knowledge Graph</title>
<style>
  :root { --bg:#0f1320; --panel:#171c2e; --ink:#e8ecf4; --muted:#9aa6c0; --line:#2a3350; }
  * { box-sizing:border-box; }
  body { margin:0; font-family:-apple-system,Segoe UI,Roboto,sans-serif; background:var(--bg); color:var(--ink); overflow:hidden; }
  header { padding:10px 16px; border-bottom:1px solid var(--line); display:flex; gap:12px; align-items:center; flex-wrap:wrap; }
  header h1 { font-size:15px; margin:0; font-weight:700; }
  header .meta { color:var(--muted); font-size:12px; }
  #search { margin-left:auto; padding:7px 10px; border-radius:8px; border:1px solid var(--line); background:var(--panel); color:var(--ink); width:220px; }
  #wrap { display:flex; height:calc(100vh - 49px); }
  canvas { flex:1; display:block; cursor:grab; }
  #side { width:330px; border-left:1px solid var(--line); padding:14px; overflow:auto; background:var(--panel); }
  #side h2 { font-size:14px; margin:0 0 4px; }
  #side .type { color:var(--muted); font-size:12px; }
  #side .loc { color:var(--muted); font-size:11px; font-family:monospace; margin:6px 0 10px; word-break:break-all; }
  #side .sum { font-size:13px; line-height:1.5; }
  #side ul { padding-left:16px; font-size:12px; }
  #side li { margin:4px 0; }
  .pill { display:inline-block; font-size:10px; padding:1px 6px; border-radius:10px; border:1px solid var(--line); margin-right:4px; }
  #legend { position:absolute; left:12px; bottom:12px; background:rgba(23,28,46,.9); border:1px solid var(--line); border-radius:8px; padding:8px 10px; font-size:11px; }
  #legend div { margin:2px 0; }
  #legend i { display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:6px; vertical-align:middle; }
  .ev { color:var(--muted); font-size:11px; }
</style>
</head>
<body>
<header>
  <h1>__REPO__ — Knowledge Graph</h1>
  <span class=\"meta\">__NODES__ nodes · __EDGES__ edges · click a node · drag to pan · scroll to zoom</span>
  <input id=\"search\" placeholder=\"Search nodes…\"/>
</header>
<div id=\"wrap\">
  <canvas id=\"cv\"></canvas>
  <div id=\"side\"><h2>Select a node</h2><p class=\"sum\">Click any node to see its summary, location, and connections. Use search to highlight.</p></div>
</div>
<div id=\"legend\"></div>
<script>
const DATA = __DATA__;
const palette = ['#6ea8fe','#7ee787','#f0883e','#d2a8ff','#ff7b72','#79c0ff','#e3b341','#56d4dd'];
const commIndex = {}; DATA.communities.forEach((c,i)=>commIndex[c.id]=i);
const color = n => palette[(commIndex[n.community]??0) % palette.length];
const byId = {}; DATA.nodes.forEach(n=>byId[n.id]=n);

// legend
const lg = document.getElementById('legend');
DATA.communities.forEach((c,i)=>{ const d=document.createElement('div'); d.innerHTML='<i style=\"background:'+palette[i%palette.length]+'\"></i>'+c.name; lg.appendChild(d); });

const cv = document.getElementById('cv'), ctx = cv.getContext('2d');
let W,H; function resize(){ W=cv.width=cv.clientWidth; H=cv.height=cv.clientHeight; } window.addEventListener('resize',resize); resize();

// init positions on a circle per community
DATA.nodes.forEach((n,i)=>{ const a=2*Math.PI*i/DATA.nodes.length; n.x=W/2+Math.cos(a)*Math.min(W,H)*0.35; n.y=H/2+Math.sin(a)*Math.min(W,H)*0.35; n.vx=0; n.vy=0; });
const E = DATA.edges.filter(e=>byId[e.source]&&byId[e.target]);

let view={x:0,y:0,k:1}, sel=null, hi=new Set();

function step(){
  // repulsion
  for(let i=0;i<DATA.nodes.length;i++){ const a=DATA.nodes[i];
    for(let j=i+1;j<DATA.nodes.length;j++){ const b=DATA.nodes[j];
      let dx=a.x-b.x, dy=a.y-b.y, d2=dx*dx+dy*dy+0.01, f=2600/d2, d=Math.sqrt(d2);
      dx/=d; dy/=d; a.vx+=dx*f; a.vy+=dy*f; b.vx-=dx*f; b.vy-=dy*f; } }
  // springs
  E.forEach(e=>{ const a=byId[e.source], b=byId[e.target]; let dx=b.x-a.x, dy=b.y-a.y, d=Math.sqrt(dx*dx+dy*dy)+0.01; const f=(d-90)*0.01; dx/=d; dy/=d; a.vx+=dx*f; a.vy+=dy*f; b.vx-=dx*f; b.vy-=dy*f; });
  // center gravity + integrate
  DATA.nodes.forEach(n=>{ n.vx+=(W/2-n.x)*0.0008; n.vy+=(H/2-n.y)*0.0008; n.x+=n.vx*=0.85; n.y+=n.vy*=0.85; });
}
function draw(){
  ctx.clearRect(0,0,W,H); ctx.save(); ctx.translate(view.x,view.y); ctx.scale(view.k,view.k);
  E.forEach(e=>{ const a=byId[e.source], b=byId[e.target]; const on=hi.size===0||hi.has(e.source)&&hi.has(e.target)||(sel&&(e.source===sel.id||e.target===sel.id));
    ctx.strokeStyle = e.confidence==='EXTRACTED'?'rgba(120,140,190,'+(on?0.7:0.12)+')':e.confidence==='INFERRED'?'rgba(240,160,80,'+(on?0.8:0.13)+')':'rgba(255,110,90,'+(on?0.9:0.16)+')';
    ctx.lineWidth=(sel&&(e.source===sel.id||e.target===sel.id))?1.6:0.7; ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y); ctx.stroke(); });
  DATA.nodes.forEach(n=>{ const r=4+Math.sqrt(n.degree||1)*2.2; const on=hi.size===0||hi.has(n.id)||(sel&&sel.id===n.id);
    ctx.globalAlpha=on?1:0.25; ctx.fillStyle=color(n); ctx.beginPath(); ctx.arc(n.x,n.y,r,0,7); ctx.fill();
    if(sel&&sel.id===n.id){ ctx.lineWidth=2; ctx.strokeStyle='#fff'; ctx.stroke(); }
    if(view.k>0.9||r>8||(sel&&sel.id===n.id)){ ctx.globalAlpha=on?0.9:0.2; ctx.fillStyle='#e8ecf4'; ctx.font='10px sans-serif'; ctx.fillText(n.label, n.x+r+2, n.y+3); }
    ctx.globalAlpha=1; });
  ctx.restore();
}
function loop(){ for(let s=0;s<2;s++) step(); draw(); requestAnimationFrame(loop); } loop();

function screenToWorld(mx,my){ return { x:(mx-view.x)/view.k, y:(my-view.y)/view.k }; }
function pick(mx,my){ const p=screenToWorld(mx,my); let best=null,bd=1e9; DATA.nodes.forEach(n=>{ const r=4+Math.sqrt(n.degree||1)*2.2; const d=(n.x-p.x)**2+(n.y-p.y)**2; if(d<bd&&d<(r+4)**2){bd=d;best=n;} }); return best; }
function neighbors(id){ const s=new Set([id]); E.forEach(e=>{ if(e.source===id)s.add(e.target); if(e.target===id)s.add(e.source); }); return s; }
function showSide(n){ const nb=E.filter(e=>e.source===n.id||e.target===n.id); const com=DATA.communities[commIndex[n.community]]; 
  let html='<h2>'+n.label+'</h2><div class=\"type\"><span class=\"pill\">'+n.type+'</span><span class=\"pill\" style=\"border-color:'+color(n)+';color:'+color(n)+'\">'+(com?com.name:n.community)+'</span> degree '+n.degree+'</div>';
  html+='<div class=\"loc\">'+(n.location||'(semantic)')+'</div><div class=\"sum\">'+n.summary+'</div><h3 style=\"font-size:12px;margin:14px 0 4px;color:var(--muted)\">Connections ('+nb.length+')</h3><ul>';
  nb.forEach(e=>{ const out=e.source===n.id; const other=byId[out?e.target:e.source]; html+='<li><b>'+e.type+'</b> '+(out?'→':'←')+' '+(other?other.label:'?')+' <span class=\"pill\">'+e.confidence+'</span><br><span class=\"ev\">'+(e.evidence||'')+'</span></li>'; });
  html+='</ul>'; document.getElementById('side').innerHTML=html; }

let drag=null, moved=false;
cv.addEventListener('mousedown',e=>{ drag={x:e.clientX,y:e.clientY,vx:view.x,vy:view.y}; moved=false; cv.style.cursor='grabbing'; });
window.addEventListener('mousemove',e=>{ if(drag){ view.x=drag.vx+(e.clientX-drag.x); view.y=drag.vy+(e.clientY-drag.y); if(Math.abs(e.clientX-drag.x)+Math.abs(e.clientY-drag.y)>3)moved=true; } });
window.addEventListener('mouseup',e=>{ if(drag&&!moved){ const r=cv.getBoundingClientRect(); const n=pick(e.clientX-r.left,e.clientY-r.top); if(n){ sel=n; hi=neighbors(n.id); showSide(n); } else { sel=null; hi=new Set(); } } drag=null; cv.style.cursor='grab'; });
cv.addEventListener('wheel',e=>{ e.preventDefault(); const r=cv.getBoundingClientRect(), mx=e.clientX-r.left, my=e.clientY-r.top; const k=Math.exp(-e.deltaY*0.001); const wx=(mx-view.x)/view.k, wy=(my-view.y)/view.k; view.k*=k; view.x=mx-wx*view.k; view.y=my-wy*view.k; },{passive:false});
document.getElementById('search').addEventListener('input',e=>{ const q=e.target.value.toLowerCase().trim(); if(!q){ hi=sel?neighbors(sel.id):new Set(); return; } hi=new Set(); DATA.nodes.forEach(n=>{ if(n.label.toLowerCase().includes(q)||n.id.toLowerCase().includes(q))hi.add(n.id); }); });
</script>
</body>
</html>
"""


def build() -> None:
    data = json.loads(GRAPH_JSON.read_text(encoding="utf-8"))
    html = (
        TEMPLATE.replace("__DATA__", json.dumps(data))
        .replace("__REPO__", data["meta"]["repo"])
        .replace("__NODES__", str(data["meta"]["node_count"]))
        .replace("__EDGES__", str(data["meta"]["edge_count"]))
    )
    GRAPH_HTML.write_text(html, encoding="utf-8")
    print(f"Wrote {GRAPH_HTML} ({len(html)} bytes)")


if __name__ == "__main__":
    build()
