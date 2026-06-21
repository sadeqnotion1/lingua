#!/usr/bin/env python3
"""Render .agents/graph/graph.json into a self-contained graph.html.

Usage:
    python .agents/graph/render_graph.py            # reads graph.json next to this file
    python .agents/graph/render_graph.py path.json  # explicit input

The output graph.html is fully offline (no CDN): data is embedded and a tiny
vanilla-JS canvas force layout draws the nodes/edges. Re-run after editing
graph.json. Idempotent: same input -> same output.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "graph.json"
    out = HERE / "graph.html"
    if not src.exists():
        print(f"[render_graph] input not found: {src}", file=sys.stderr)
        return 1
    data = json.loads(src.read_text(encoding="utf-8"))
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])
    project = data.get("project", "project")
    payload = json.dumps({"nodes": nodes, "edges": edges}, ensure_ascii=False)
    html = _TEMPLATE.replace("__PROJECT__", str(project)).replace(
        "__DATA__", payload
    ).replace("__NODE_COUNT__", str(len(nodes))).replace(
        "__EDGE_COUNT__", str(len(edges))
    )
    out.write_text(html, encoding="utf-8")
    print(f"[render_graph] wrote {out} ({len(nodes)} nodes, {len(edges)} edges)")
    return 0


_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__PROJECT__ — knowledge graph</title>
<style>
  :root { color-scheme: light dark; }
  body { margin: 0; font: 14px/1.4 system-ui, sans-serif; background: #0f1115; color: #e6e6e6; }
  header { padding: 10px 16px; border-bottom: 1px solid #2a2f3a; display: flex; gap: 16px; align-items: baseline; }
  header h1 { font-size: 15px; margin: 0; }
  header .meta { color: #8b93a7; font-size: 12px; }
  #wrap { display: flex; height: calc(100vh - 44px); }
  canvas { flex: 1; display: block; cursor: grab; }
  aside { width: 280px; border-left: 1px solid #2a2f3a; overflow: auto; padding: 12px; }
  aside h2 { font-size: 12px; text-transform: uppercase; letter-spacing: .05em; color: #8b93a7; margin: 12px 0 6px; }
  .node-item { padding: 4px 6px; border-radius: 6px; cursor: pointer; }
  .node-item:hover { background: #1b2030; }
  .pill { display:inline-block; font-size: 10px; padding: 1px 6px; border-radius: 999px; background:#1b2030; color:#9fb0d0; margin-right:6px; }
  code { color:#9fb0d0; }
</style>
</head>
<body>
<header>
  <h1>__PROJECT__ — knowledge graph</h1>
  <span class="meta">__NODE_COUNT__ nodes · __EDGE_COUNT__ edges · drag to pan, scroll to zoom</span>
</header>
<div id="wrap">
  <canvas id="c"></canvas>
  <aside>
    <h2>Nodes</h2>
    <div id="list"></div>
    <h2>Selected</h2>
    <div id="detail" class="meta">Click a node.</div>
  </aside>
</div>
<script>
const GRAPH = __DATA__;
const colors = {module:'#6ea8fe',file:'#7ee787',function:'#f0b86e',class:'#d2a8ff',route:'#ff7b9c',asset:'#56d4dd',doc:'#c9d1d9',external:'#8b949e'};
const canvas = document.getElementById('c'), ctx = canvas.getContext('2d');
let W,H,scale=1,ox=0,oy=0;
function resize(){ const r=canvas.getBoundingClientRect(); W=canvas.width=r.width*devicePixelRatio; H=canvas.height=r.height*devicePixelRatio; }
window.addEventListener('resize',resize);
const idx={}; GRAPH.nodes.forEach((n,i)=>{ idx[n.id]=i; n.x=Math.cos(i)*180+ (Math.random()*40); n.y=Math.sin(i)*180+(Math.random()*40); n.vx=0; n.vy=0; });
const E = GRAPH.edges.filter(e=>idx[e.from]!=null && idx[e.to]!=null);
function step(){
  for(const n of GRAPH.nodes){ n.fx=0; n.fy=0; }
  for(let i=0;i<GRAPH.nodes.length;i++) for(let j=i+1;j<GRAPH.nodes.length;j++){
    const a=GRAPH.nodes[i],b=GRAPH.nodes[j]; let dx=a.x-b.x,dy=a.y-b.y; let d2=dx*dx+dy*dy+0.01; let f=2200/d2; let d=Math.sqrt(d2);
    a.fx+=f*dx/d; a.fy+=f*dy/d; b.fx-=f*dx/d; b.fy-=f*dy/d;
  }
  for(const e of E){ const a=GRAPH.nodes[idx[e.from]],b=GRAPH.nodes[idx[e.to]]; let dx=b.x-a.x,dy=b.y-a.y; let d=Math.sqrt(dx*dx+dy*dy)||1; let f=(d-120)*0.02; a.fx+=f*dx/d; a.fy+=f*dy/d; b.fx-=f*dx/d; b.fy-=f*dy/d; }
  for(const n of GRAPH.nodes){ n.fx-=n.x*0.002; n.fy-=n.y*0.002; n.vx=(n.vx+n.fx)*0.85; n.vy=(n.vy+n.fy)*0.85; n.x+=n.vx; n.y+=n.vy; }
}
let sel=null;
function draw(){
  ctx.setTransform(1,0,0,1,0,0); ctx.clearRect(0,0,W,H);
  ctx.setTransform(scale*devicePixelRatio,0,0,scale*devicePixelRatio, W/2+ox, H/2+oy);
  ctx.lineWidth=1/scale; ctx.strokeStyle='rgba(140,150,170,.35)';
  for(const e of E){ const a=GRAPH.nodes[idx[e.from]],b=GRAPH.nodes[idx[e.to]]; ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y); ctx.stroke(); }
  for(const n of GRAPH.nodes){ ctx.beginPath(); ctx.fillStyle=colors[n.type]||'#ccc'; const r=n===sel?9:6; ctx.arc(n.x,n.y,r,0,7); ctx.fill(); ctx.fillStyle='#cfd6e4'; ctx.font=(11/scale)+'px system-ui'; ctx.fillText(n.id, n.x+8, n.y+3); }
}
function loop(){ for(let k=0;k<2;k++) step(); draw(); requestAnimationFrame(loop); }
resize(); loop();
let drag=false,lx,ly; canvas.addEventListener('mousedown',e=>{drag=true;lx=e.clientX;ly=e.clientY;});
window.addEventListener('mouseup',()=>drag=false);
window.addEventListener('mousemove',e=>{ if(drag){ ox+=(e.clientX-lx)*devicePixelRatio; oy+=(e.clientY-ly)*devicePixelRatio; lx=e.clientX; ly=e.clientY; }});
canvas.addEventListener('wheel',e=>{ e.preventDefault(); scale*=e.deltaY<0?1.1:0.9; scale=Math.max(0.2,Math.min(4,scale)); },{passive:false});
const list=document.getElementById('list'), detail=document.getElementById('detail');
GRAPH.nodes.forEach(n=>{ const d=document.createElement('div'); d.className='node-item'; d.innerHTML='<span class="pill">'+n.type+'</span>'+n.id; d.onclick=()=>{ sel=n; detail.innerHTML='<b>'+n.id+'</b><br><span class="pill">'+n.type+'</span> <code>'+(n.path||'')+'</code><br>'+(n.summary||'')+(n.symbols?'<br>symbols: '+n.symbols.join(', '):''); }; list.appendChild(d); });
</script>
</body>
</html>
"""


if __name__ == "__main__":
    raise SystemExit(main())
