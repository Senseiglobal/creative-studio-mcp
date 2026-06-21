import json
import socket
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from business_tools import (
    calculate_payment,
    create_project_package,
    create_quote,
    delete_project,
    empty_project_bin,
    export_project,
    generate_project_checklist,
    get_brand_profile,
    list_deleted_projects,
    list_recent_projects,
    list_services,
    parse_services_text,
    package_to_markdown,
    package_to_text,
    save_brand_profile,
    save_project,
)

HTML = r'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <title>Creative Studio MCP</title>
  <style>
    :root{--bg:#eef2f0;--surface:#fff;--surface2:#f7faf8;--ink:#101814;--muted:#607066;--line:#d8e1da;--primary:#59d37b;--primary2:#1f883d;--danger:#ba1a1a;--radius:20px;--radius2:14px;--shadow:0 20px 50px rgba(15,23,42,.12);--fast:150ms ease;--med:240ms ease;font-family:Arial,Helvetica,sans-serif}
    [data-theme=dark]{--bg:#08100c;--surface:#111a15;--surface2:#17221c;--ink:#f5faf6;--muted:#b5c5bb;--line:#29372f;--primary:#7cf29b;--primary2:#8ff4aa;--danger:#ffb4ab;color-scheme:dark}
    *{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(circle at 80% 10%,rgba(89,211,123,.18),transparent 30rem),var(--bg);color:var(--ink);line-height:1.5}button,input,select,textarea{font:inherit}button{min-height:48px;cursor:pointer}.skip{position:fixed;top:12px;left:12px;z-index:99;transform:translateY(-150%);background:var(--ink);color:var(--bg);padding:12px 16px;border-radius:999px}.skip:focus{transform:translateY(0)}:focus-visible{outline:3px solid #4f8cff;outline-offset:3px}.app{display:grid;grid-template-columns:280px minmax(0,1fr)420px;min-height:100vh}.side{position:sticky;top:0;height:100vh;background:rgba(12,22,16,.96);color:#fff;padding:20px;border-right:1px solid rgba(255,255,255,.08)}.brand{display:flex;gap:12px;align-items:center;margin-bottom:28px}.mark{width:52px;height:52px;border-radius:16px;background:linear-gradient(135deg,#91f7a9,#1f883d);display:grid;place-items:center;color:#061108;font-weight:900}.nav{display:grid;gap:8px}.nav button{border:0;border-radius:14px;background:transparent;color:rgba(255,255,255,.8);text-align:left;padding:0 14px}.nav button.active,.nav button:hover{background:rgba(124,242,155,.16);color:#91f7a9}.main{padding:24px;min-width:0}.top{display:flex;justify-content:space-between;gap:16px;align-items:center;margin-bottom:24px}.search{min-height:54px;width:min(620px,100%);border:1px solid var(--line);border-radius:18px;background:var(--surface);color:var(--ink);padding:0 18px;box-shadow:0 10px 24px rgba(0,0,0,.05)}h1,h2,h3{margin:0;line-height:1.12}h1{font-size:clamp(2rem,4vw,3.2rem)}p{color:var(--muted);margin:6px 0 0}.toolbar{display:flex;gap:10px;flex-wrap:wrap;align-items:center}.btn{border:1px solid var(--line);border-radius:14px;padding:0 16px;background:var(--surface);color:var(--ink);font-weight:800;transition:transform var(--fast),box-shadow var(--fast),background var(--fast)}.btn:hover{box-shadow:var(--shadow);transform:translateY(-1px)}.btn:active{transform:scale(.98)}.primary{background:var(--primary);border-color:transparent;color:#061108}.danger{background:rgba(186,26,26,.12);color:var(--danger)}.ghost{background:transparent}.cards{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:16px;margin:24px 0}.card,.panel,.preview{background:rgba(255,255,255,.72);background:color-mix(in srgb,var(--surface),transparent 4%);border:1px solid var(--line);border-radius:var(--radius);box-shadow:0 12px 30px rgba(0,0,0,.06);backdrop-filter:blur(16px)}.card{min-height:150px;padding:18px;text-align:left;color:var(--ink);transition:transform var(--med),border-color var(--fast),box-shadow var(--fast)}.card:hover{transform:translateY(-4px);border-color:var(--primary);box-shadow:var(--shadow)}.icon{width:44px;height:44px;border-radius:14px;background:rgba(89,211,123,.18);display:grid;place-items:center;margin-bottom:18px;color:var(--primary2);font-weight:900}.panel{padding:20px;margin-top:18px}.section{display:none;animation:reveal var(--med)}.section.active{display:block}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}label{display:grid;gap:8px;font-weight:800}small{color:var(--muted);font-weight:400}input,select,textarea{width:100%;min-height:52px;border:1px solid var(--line);border-radius:14px;background:var(--surface);color:var(--ink);padding:0 14px}textarea{min-height:120px;padding-top:12px;resize:vertical}.output{margin-top:14px;padding:16px;border:1px solid var(--line);border-radius:16px;background:var(--surface2)}pre{white-space:pre-wrap;word-break:break-word;background:#07100b;color:#ecfff0;border-radius:14px;padding:16px;font:14px/1.55 Consolas,monospace}.recent{display:grid;gap:10px}.row{display:grid;grid-template-columns:1fr auto;gap:12px;align-items:center;padding:14px;border:1px solid var(--line);border-radius:16px;background:var(--surface2)}.preview{position:sticky;top:0;height:100vh;padding:22px;overflow:auto;border-radius:0}.toast{position:fixed;right:22px;bottom:22px;z-index:80;background:var(--ink);color:var(--bg);padding:14px 18px;border-radius:16px;box-shadow:var(--shadow);opacity:0;transform:translateY(12px);transition:opacity var(--med),transform var(--med)}.toast.show{opacity:1;transform:translateY(0)}.modal{position:fixed;inset:0;z-index:70;display:none;place-items:center;background:rgba(0,0,0,.48);padding:20px}.modal.show{display:grid}.modal-card{max-width:560px;background:var(--surface);border:1px solid var(--line);border-radius:24px;padding:24px;box-shadow:var(--shadow)}.tip{position:relative}.tip span{display:none;position:absolute;z-index:20;top:calc(100% + 8px);left:0;width:260px;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:12px;box-shadow:var(--shadow);color:var(--ink)}.tip:hover span,.tip:focus-within span{display:block}@keyframes reveal{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}@media(max-width:1180px){.app{grid-template-columns:240px minmax(0,1fr)}.preview{position:static;height:auto;border-radius:var(--radius);margin:0 24px 24px}.cards{grid-template-columns:repeat(2,1fr)}}@media(max-width:760px){.app{display:block}.side{position:static;height:auto}.nav{grid-template-columns:repeat(2,1fr)}.main{padding:16px}.top{align-items:stretch;flex-direction:column}.cards,.grid{grid-template-columns:1fr}.row{grid-template-columns:1fr}.preview{margin:0 16px 16px}}@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.001ms!important;transition-duration:.001ms!important;scroll-behavior:auto!important}}
  </style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="app">
  <aside class="side" aria-label="Sidebar">
    <div class="brand"><div class="mark">CS</div><div><strong>Creative Studio MCP</strong><p>Creative Workspace</p></div></div>
    <nav class="nav" aria-label="Main navigation">
      <button class="active" data-view="home">Dashboard</button><button data-view="project">New Project</button><button data-view="settings">Preferences</button><button data-view="quote">Quote</button><button data-view="payment">Payment</button><button data-view="checklist">Checklist</button><button data-view="services">Services</button><button data-view="bin">Bin</button>
    </nav>
  </aside>
  <main id="main" class="main" tabindex="-1">
    <div class="top"><input class="search" aria-label="Search projects, clients, services" placeholder="Search projects, clients, services..."><div class="toolbar"><button class="btn ghost tip" id="theme">Theme<span>Switch light, dark, or system mode.</span></button><button class="btn primary" data-view="project">New Project</button></div></div>
    <section id="home" class="section active"><h1>Good day, Thomas!</h1><p>Create quotes, manage projects, and grow your creative business.</p><div id="onboard" class="panel"><h2>Start here</h2><p>Set your preferences, create your first project, then copy, export, or share the package.</p><div class="toolbar"><button class="btn primary" data-view="project">New Project</button><button class="btn" data-view="settings">Preferences</button><button class="btn ghost" id="dismiss">Dismiss</button></div></div><div class="cards"><button class="card" data-view="project"><div class="icon">+</div><h3>New Project</h3><p>Create a project package</p></button><button class="card" data-view="quote"><div class="icon">Q</div><h3>Quote</h3><p>Generate client quotes</p></button><button class="card" data-view="payment"><div class="icon">$</div><h3>Payment</h3><p>Calculate terms</p></button><button class="card" data-view="checklist"><div class="icon">OK</div><h3>Checklist</h3><p>Create checklists</p></button><button class="card" data-view="services"><div class="icon">S</div><h3>Services</h3><p>Manage services</p></button></div><div class="panel"><div class="toolbar" style="justify-content:space-between"><h2>Recent Projects</h2><button class="btn" id="refresh">Refresh</button></div><div id="recent" class="recent" aria-live="polite"></div></div></section>
    <section id="project" class="section"><h1>New Project</h1><p>Generate a complete package.</p><div class="panel"><form id="projectForm"><div class="grid"><label>Client name<input name="client_name" value="Israel Thomas" required><small>Who is this for?</small></label><label>Service<select name="service" id="projectService"></select><small>Choose from your services.</small></label><label>Design fee<input name="design_fee" type="number" min="1" value="3000" required><small>Numbers only.</small></label><label>Upfront percent<input name="upfront_percent" type="number" min="0" max="100" value="70" required><small>Example: 70.</small></label><label>Project type<input name="project_type" value="Brand Identity Design" required><small>Short project category.</small></label></div><button class="btn primary" type="submit">Generate</button></form><div id="projectOut"></div></div></section>
    <section id="settings" class="section"><h1>Preferences</h1><div class="panel"><form id="settingsForm"><div class="grid"><label>Business name<input name="business_name"></label><label>Owner name<input name="owner_name"></label><label>Email<input name="email"></label><label>Phone<input name="phone"></label><label>Website<input name="website"></label><label>Currency<input name="currency"></label></div><label>Payment terms<textarea name="payment_terms"></textarea></label><label>Services<textarea name="services_text"></textarea><small>One per line: Service | Price range</small></label><button class="btn primary" type="submit">Save</button></form></div></section>
    <section id="quote" class="section"><h1>Quote</h1><div class="panel"><form id="quoteForm"><div class="grid"><label>Client<input name="client_name" value="John Smith"></label><label>Service<select name="service" id="quoteService"></select></label><label>Fee<input name="design_fee" type="number" value="3000"></label></div><button class="btn primary">Generate</button></form><div id="quoteOut"></div></div></section>
    <section id="payment" class="section"><h1>Payment</h1><div class="panel"><form id="paymentForm"><div class="grid"><label>Total fee<input name="total_fee" type="number" value="5000"></label><label>Upfront percent<input name="upfront_percent" type="number" value="70"></label></div><button class="btn primary">Generate</button></form><div id="paymentOut"></div></div></section>
    <section id="checklist" class="section"><h1>Checklist</h1><div class="panel"><form id="checklistForm"><label>Project type<input name="project_type" value="Product packaging design"></label><button class="btn primary">Generate</button></form><div id="checklistOut"></div></div></section>
    <section id="services" class="section"><h1>Services</h1><div class="panel"><button class="btn primary" id="servicesBtn">Generate</button><div id="servicesOut"></div></div></section>
    <section id="bin" class="section"><h1>Bin</h1><div class="panel"><div class="toolbar"><button class="btn" id="binRefresh">Refresh</button><button class="btn danger" id="binEmpty">Empty Bin</button></div><div id="binList" class="recent"></div></div></section>
  </main>
  <aside class="preview" aria-label="Project package preview"><div class="toolbar" style="justify-content:space-between"><h2>Project Package Preview</h2><button class="btn ghost" id="clearPreview">Close</button></div><div id="preview"><p>Your generated package appears here.</p></div></aside>
</div>
<div id="toast" class="toast" role="status" aria-live="polite"></div>
<div id="modal" class="modal" role="dialog" aria-modal="true" aria-labelledby="welcome"><div class="modal-card"><h2 id="welcome">Welcome to Creative Studio MCP</h2><p>Create your first project package, export it, or share it. You can skip this guide.</p><div class="toolbar"><button class="btn primary" id="start">Start</button><button class="btn" id="skip">Skip</button></div></div></div>
<script>
let lastProject=null,lastPackageText="";const qs=s=>document.querySelector(s),qsa=s=>document.querySelectorAll(s);const toast=m=>{const t=qs("#toast");t.textContent=m;t.classList.add("show");clearTimeout(window.tt);window.tt=setTimeout(()=>t.classList.remove("show"),2200)};const api=async(p,d={})=>{const r=await fetch(p,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(d)});const j=await r.json();if(!r.ok)throw Error(j.error||"Something went wrong");return j.result};const fd=f=>Object.fromEntries(new FormData(f).entries());const esc=s=>String(s).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;");const txt=v=>typeof v==="string"?v:Array.isArray(v)?v.map((x,i)=>`${i+1}. ${x}`).join("\n"):Object.entries(v).map(([k,x])=>`${k}: ${x}`).join("\n");function block(title,value){const text=txt(value);return `<div class="output"><div class="toolbar" style="justify-content:space-between"><h3>${title}</h3><button class="btn" data-copy="${encodeURIComponent(text)}">Copy</button></div><pre>${esc(text)}</pre></div>`}function show(view){qsa(".section").forEach(x=>x.classList.remove("active"));qsa(".nav button").forEach(x=>x.classList.remove("active"));qs("#"+view).classList.add("active");qsa(`[data-view="${view}"]`).forEach(b=>b.classList.add("active"));if(view==="bin")loadBin();if(view==="home")loadRecent()}qsa("[data-view]").forEach(b=>b.onclick=()=>show(b.dataset.view));function setTheme(mode){if(mode==="system")localStorage.removeItem("theme");else localStorage.setItem("theme",mode);document.documentElement.dataset.theme=mode==="system"?(matchMedia("(prefers-color-scheme:dark)").matches?"dark":"light"):mode;toast(`Theme: ${mode}`)}let theme=localStorage.getItem("theme")||"system";setTheme(theme);qs("#theme").onclick=()=>{const next=theme==="system"?"dark":theme==="dark"?"light":"system";theme=next;setTheme(next)};async function loadServices(){const s=await api("/api/services");["projectService","quoteService"].forEach(id=>{qs("#"+id).innerHTML=Object.keys(s).map(x=>`<option>${esc(x)}</option>`).join("")})}async function loadProfile(){const p=await api("/api/profile");const f=qs("#settingsForm");Object.entries(p).forEach(([k,v])=>{if(f.elements[k]&&k!=="services")f.elements[k].value=v||""});f.elements.services_text.value=Object.entries(p.services||{}).map(([k,v])=>`${k} | ${v}`).join("\n")}function renderPackage(project){lastProject=project;const p=project.generated_package;lastPackageText=["CLIENT QUOTE",txt(p.client_quote),"","PAYMENT",txt(p.payment_breakdown),"","CHECKLIST",txt(p.project_checklist),"","DELIVERABLES",txt(p.deliverables),"","EMAIL",txt(p.client_email)].join("\n");const actions=`<div class="toolbar"><button class="btn primary" data-copy="${encodeURIComponent(lastPackageText)}">Copy</button><button class="btn" data-export="txt">Export TXT</button><button class="btn" data-export="md">Export MD</button><button class="btn" id="shareBtn">Share</button></div>`;qs("#preview").innerHTML=actions+block("Client Quote",p.client_quote)+block("Payment",p.payment_breakdown)+block("Checklist",p.project_checklist)+block("Deliverables",p.deliverables)+block("Email",p.client_email);qs("#projectOut").innerHTML=qs("#preview").innerHTML}async function loadRecent(){const r=await api("/api/recent",{limit:8});qs("#recent").innerHTML=r.length?r.map(p=>`<div class="row"><div><h3>${esc(p.client_name)}</h3><p>${esc(p.service)} at $${Number(p.design_fee).toLocaleString()}</p></div><div class="toolbar"><button class="btn" data-export-id="${p.id}" data-format="pdf">Export</button><button class="btn danger" data-delete="${p.id}">Delete</button></div></div>`).join(""):`<div class="output">No saved projects yet.</div>`}async function loadBin(){const r=await api("/api/bin",{limit:20});qs("#binList").innerHTML=r.length?r.map(p=>`<div class="row"><div><h3>${esc(p.client_name)}</h3><p>${esc(p.service)}</p></div><button class="btn" data-restore="${p.id}">Restore</button></div>`).join(""):`<div class="output">Bin is empty.</div>`}document.addEventListener("click",async e=>{const c=e.target.closest("[data-copy]");if(c){await navigator.clipboard.writeText(decodeURIComponent(c.dataset.copy));toast("Copied");return}const ex=e.target.closest("[data-export]");if(ex&&lastProject){const r=await api("/api/export",{project_id:lastProject.id,file_format:ex.dataset.export});toast(`Exported ${r.file_name}`);return}const exid=e.target.closest("[data-export-id]");if(exid){const r=await api("/api/export",{project_id:exid.dataset.exportId,file_format:exid.dataset.format});toast(`Exported ${r.file_name}`);return}const del=e.target.closest("[data-delete]");if(del){await api("/api/delete",{project_id:del.dataset.delete});toast("Moved to bin");loadRecent();return}const res=e.target.closest("[data-restore]");if(res){await api("/api/restore",{project_id:res.dataset.restore});toast("Restored");loadBin();loadRecent();return}});qs("#projectForm").onsubmit=async e=>{e.preventDefault();renderPackage(await api("/api/project",fd(e.target)));toast("Project generated");loadRecent()};qs("#quoteForm").onsubmit=async e=>{e.preventDefault();qs("#quoteOut").innerHTML=block("Quote",await api("/api/quote",fd(e.target)))};qs("#paymentForm").onsubmit=async e=>{e.preventDefault();qs("#paymentOut").innerHTML=block("Payment",await api("/api/payment",fd(e.target)))};qs("#checklistForm").onsubmit=async e=>{e.preventDefault();qs("#checklistOut").innerHTML=block("Checklist",await api("/api/checklist",fd(e.target)))};qs("#settingsForm").onsubmit=async e=>{e.preventDefault();await api("/api/save-profile",fd(e.target));toast("Preferences saved");loadServices()};qs("#servicesBtn").onclick=async()=>qs("#servicesOut").innerHTML=block("Services",await api("/api/services"));qs("#refresh").onclick=loadRecent;qs("#binRefresh").onclick=loadBin;qs("#binEmpty").onclick=async()=>{await api("/api/empty-bin");toast("Bin emptied");loadBin()};qs("#clearPreview").onclick=()=>qs("#preview").innerHTML="<p>Your generated package appears here.</p>";document.addEventListener("click",async e=>{if(e.target.id==="shareBtn"){if(navigator.share)await navigator.share({title:"Project Package",text:lastPackageText});else{await navigator.clipboard.writeText(lastPackageText);toast("Share text copied")}}});if(!localStorage.getItem("seenOnboarding"))qs("#modal").classList.add("show");qs("#skip").onclick=()=>{localStorage.setItem("seenOnboarding","1");qs("#modal").classList.remove("show")};qs("#start").onclick=()=>{localStorage.setItem("seenOnboarding","1");qs("#modal").classList.remove("show");show("project")};loadServices();loadProfile();loadRecent();
</script>
</body></html>'''

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return
    def send_text(self, status, content, content_type="application/json"):
        body = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.send_text(200, HTML, "text/html")
        else:
            self.send_text(404, "Not found", "text/plain")
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8") if length else "{}")
            if self.path == "/api/profile":
                result = get_brand_profile()
            elif self.path == "/api/save-profile":
                payload["services"] = parse_services_text(payload.get("services_text", ""))
                result = save_brand_profile(payload)
            elif self.path == "/api/services":
                result = list_services()
            elif self.path == "/api/payment":
                result = calculate_payment(payload.get("total_fee", 0), payload.get("upfront_percent", 70))
            elif self.path == "/api/quote":
                result = create_quote(payload.get("client_name", ""), payload.get("service", ""), payload.get("design_fee", 0))
            elif self.path == "/api/checklist":
                result = generate_project_checklist(payload.get("project_type", ""))
            elif self.path == "/api/project":
                package = create_project_package(payload.get("client_name", ""), payload.get("service", ""), payload.get("design_fee", 0), payload.get("upfront_percent", 70), payload.get("project_type", ""))
                result = save_project(payload.get("client_name", ""), payload.get("service", ""), payload.get("design_fee", 0), payload.get("upfront_percent", 70), payload.get("project_type", ""), package)
            elif self.path == "/api/recent":
                result = list_recent_projects(payload.get("limit", 8))
            elif self.path == "/api/bin":
                result = list_deleted_projects(payload.get("limit", 20))
            elif self.path == "/api/delete":
                result = delete_project(payload.get("project_id", ""))
            elif self.path == "/api/restore":
                result = restore_project(payload.get("project_id", ""))
            elif self.path == "/api/empty-bin":
                result = empty_project_bin()
            elif self.path == "/api/export":
                result = export_project(payload.get("project_id", ""), payload.get("file_format", "txt"))
            else:
                self.send_text(404, json.dumps({"error": "Unknown action"}))
                return
            self.send_text(200, json.dumps({"result": result}))
        except Exception as exc:
            self.send_text(400, json.dumps({"error": str(exc)}))

def find_port(start=8765, end=8790):
    for port in range(start, end + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("127.0.0.1", port))
                return port
            except OSError:
                pass
    raise RuntimeError("No free local port found")

def main():
    port = find_port()
    url = f"http://127.0.0.1:{port}"
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    print()
    print("Creative Studio MCP is running.")
    print(f"Open this link if the browser does not open: {url}")
    print("Keep this window open while using the app.")
    print()
    server.serve_forever()

if __name__ == "__main__":
    main()
