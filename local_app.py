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
  

/* Creative Studio MCP UI polish: spacing, feedback, tooltips, export messages */
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-7: 32px;
  --success: #6ff08e;
  --warning: #ffd166;
}
body {
  text-rendering: optimizeLegibility;
}
.main {
  padding: clamp(18px, 2.4vw, 34px);
}
.top {
  gap: var(--space-5);
  margin-bottom: var(--space-7);
}
.search {
  min-height: 58px;
  padding: 0 20px;
}
h1 {
  letter-spacing: 0;
  margin-bottom: var(--space-3);
}
h2,
h3 {
  letter-spacing: 0;
}
.panel {
  padding: clamp(20px, 2.4vw, 30px);
  margin-top: var(--space-6);
}
#onboard {
  display: grid;
  gap: var(--space-4);
}
#onboard .toolbar {
  margin-top: var(--space-2);
}
.cards {
  gap: var(--space-5);
  margin: var(--space-7) 0 var(--space-6);
}
.card {
  display: grid;
  align-content: start;
  gap: var(--space-3);
  min-height: 166px;
  padding: 22px;
}
.card h3,
.card p {
  margin: 0;
}
.icon {
  width: 48px;
  height: 48px;
  margin-bottom: var(--space-3);
  border-radius: 16px;
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.08), 0 10px 24px rgba(0,0,0,.12);
}
.toolbar {
  gap: var(--space-3);
}
.btn {
  min-height: 48px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  line-height: 1;
  padding: 0 18px;
  white-space: nowrap;
}
.btn[data-busy="true"] {
  opacity: .72;
  pointer-events: none;
}
.btn[data-busy="true"]::after {
  content: "";
  width: 14px;
  height: 14px;
  border-radius: 999px;
  border: 2px solid currentColor;
  border-right-color: transparent;
  animation: cs-spin .8s linear infinite;
}
.recent {
  margin-top: var(--space-4);
}
.row {
  padding: 18px;
  gap: var(--space-5);
}
.row h3,
.row p {
  margin: 0;
}
.preview {
  padding: clamp(20px, 2vw, 28px);
}
.preview > .toolbar:first-child {
  margin-bottom: var(--space-5);
}
#preview {
  display: grid;
  gap: var(--space-5);
}
.output {
  padding: 18px;
  display: grid;
  gap: var(--space-4);
}
.output > .toolbar {
  align-items: center;
}
pre {
  margin: 0;
  padding: 18px;
  border: 1px solid rgba(255,255,255,.06);
  max-height: 52vh;
  overflow: auto;
}
.tip {
  position: relative;
}
.tip span,
.tooltip-card {
  display: none;
  position: absolute;
  z-index: 100;
  top: calc(100% + 12px);
  left: 0;
  min-width: 240px;
  max-width: min(320px, 80vw);
  padding: 14px 16px;
  border: 1px solid var(--line);
  border-radius: 16px;
  background: var(--surface);
  color: var(--ink);
  box-shadow: var(--shadow);
  line-height: 1.45;
  font-weight: 600;
}
.tip:hover span,
.tip:focus-within span,
.tip.is-open span {
  display: block;
  animation: cs-pop 180ms ease both;
}
.toast {
  right: 24px;
  bottom: 24px;
  max-width: min(460px, calc(100vw - 32px));
  display: grid;
  gap: 6px;
  padding: 16px 18px;
  border-radius: 18px;
  border: 1px solid color-mix(in srgb, var(--success), transparent 65%);
  background: color-mix(in srgb, var(--ink), #0d2817 18%);
  color: var(--bg);
}
.toast strong {
  display: block;
  color: var(--success);
  font-size: 14px;
}
.toast small {
  color: color-mix(in srgb, var(--bg), transparent 20%);
  word-break: break-word;
}
.action-confirm {
  position: fixed;
  right: 24px;
  bottom: 92px;
  z-index: 82;
  max-width: min(460px, calc(100vw - 32px));
  border: 1px solid var(--line);
  border-radius: 18px;
  background: var(--surface);
  color: var(--ink);
  box-shadow: var(--shadow);
  padding: 14px 16px;
  opacity: 0;
  transform: translateY(10px) scale(.98);
  transition: opacity 220ms ease, transform 220ms ease;
}
.action-confirm.show {
  opacity: 1;
  transform: translateY(0) scale(1);
}
.action-confirm b {
  display: block;
  margin-bottom: 4px;
}
.action-confirm code {
  display: block;
  margin-top: 6px;
  color: var(--muted);
  white-space: normal;
  word-break: break-word;
  font-size: 12px;
}
form {
  display: grid;
  gap: var(--space-5);
}
label {
  gap: var(--space-2);
}
input,
select,
textarea {
  transition: border-color var(--fast), box-shadow var(--fast), background var(--fast);
}
input:focus,
select:focus,
textarea:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 4px color-mix(in srgb, var(--primary), transparent 78%);
}
.help-text,
.field-error {
  display: block;
  margin-top: 6px;
  font-size: 13px;
}
.field-error {
  color: var(--danger);
  font-weight: 700;
}
@keyframes cs-spin {
  to { transform: rotate(360deg); }
}
@keyframes cs-pop {
  from { opacity: 0; transform: translateY(6px) scale(.98); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
@media (max-width: 1180px) {
  .preview {
    margin: 0 clamp(16px, 3vw, 24px) 24px;
  }
}
@media (max-width: 760px) {
  .toolbar {
    width: 100%;
  }
  .btn {
    flex: 1 1 auto;
  }
  .card {
    min-height: 130px;
  }
  .output > .toolbar,
  .row {
    align-items: stretch;
  }
  .output > .toolbar .btn,
  .row .btn {
    width: 100%;
  }
  .toast,
  .action-confirm {
    left: 16px;
    right: 16px;
  }
}
@media (prefers-reduced-motion: reduce) {
  .btn[data-busy="true"]::after {
    animation: none;
  }
}

  

/* Dashboard connection cards and footer info */
.meta-strip {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-4, 16px);
  margin-top: var(--space-5, 20px);
}
.meta-card {
  min-height: 96px;
  padding: 18px;
  border: 1px solid var(--line);
  border-radius: var(--radius2, 14px);
  background: color-mix(in srgb, var(--surface), transparent 5%);
}
.meta-card strong {
  display: block;
  margin-bottom: 6px;
}
.connection-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-4, 16px);
  margin-top: var(--space-5, 20px);
}
.connection-card {
  display: grid;
  gap: 12px;
  padding: 20px;
  border: 1px solid var(--line);
  border-radius: var(--radius, 20px);
  background: linear-gradient(145deg, color-mix(in srgb, var(--surface), transparent 2%), color-mix(in srgb, var(--surface2), transparent 4%));
  min-height: 190px;
  transition: transform var(--med, 240ms ease), border-color var(--fast, 150ms ease), box-shadow var(--fast, 150ms ease);
}
.connection-card:hover {
  transform: translateY(-3px);
  border-color: var(--primary);
  box-shadow: var(--shadow);
}
.connection-card .status {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  width: fit-content;
  border-radius: 999px;
  padding: 0 10px;
  font-size: 12px;
  font-weight: 800;
  color: #061108;
  background: var(--primary);
}
.connection-card .status.soft {
  color: var(--ink);
  background: color-mix(in srgb, var(--surface2), var(--primary) 18%);
  border: 1px solid var(--line);
}
.developer-footer {
  margin-top: var(--space-6, 24px);
  padding: 18px;
  border: 1px solid var(--line);
  border-radius: var(--radius2, 14px);
  color: var(--muted);
  background: color-mix(in srgb, var(--surface), transparent 12%);
}
.developer-footer a {
  color: var(--primary2);
  font-weight: 800;
}
@media (max-width: 980px) {
  .meta-strip,
  .connection-grid {
    grid-template-columns: 1fr;
  }
}

  

/* Generate results repair */
.generated-results {
  margin-top: 22px;
  display: grid;
  gap: 18px;
}
.result-banner {
  display: grid;
  gap: 6px;
  padding: 16px 18px;
  border-radius: 18px;
  border: 1px solid color-mix(in srgb, var(--primary), transparent 55%);
  background: color-mix(in srgb, var(--primary), transparent 88%);
}
.result-banner strong {
  color: var(--ink);
}
.result-banner p {
  margin: 0;
}
.generated-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

  </style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="app">
  <aside class="side" aria-label="Sidebar">
    <div class="brand"><div class="mark">CS</div><div><strong>Creative Studio MCP</strong><p>Creative Workspace</p></div></div>
    <nav class="nav" aria-label="Main navigation">
      <button class="active" data-view="home">Dashboard</button><button data-view="project">New Project</button><button data-view="settings">Preferences</button><button data-view="quote">Quote</button><button data-view="payment">Payment</button><button data-view="checklist">Checklist</button><button data-view="services">Services</button><button data-view="bin">Bin</button><button data-view="claude">Connect Claude</button><button data-view="storage">Storage</button>
    </nav>
  </aside>
  <main id="main" class="main" tabindex="-1">
    <div class="top"><input class="search" aria-label="Search projects, clients, services" placeholder="Search projects, clients, services..."><div class="toolbar"><button class="btn ghost tip" id="theme">Theme<span>Switch light, dark, or system mode.</span></button><button class="btn primary" data-view="project">New Project</button></div></div>
    <section id="home" class="section active"><h1 id="dashboardGreeting">Welcome</h1><p>Create quotes, manage projects, and grow your creative business.</p>
<div class="meta-strip" aria-label="App information">
  <div class="meta-card" id="appVersionCard"><strong>App version</strong><p>Creative Studio MCP v1.0.0</p></div>
  <div class="meta-card"><strong>Developer team</strong><p>Thomas Ogun under Senseiglobal.</p></div>
  <div class="meta-card"><strong>Contact</strong><p><a href="https://github.com/Senseiglobal/creative-studio-mcp" target="_blank" rel="noreferrer">GitHub repo</a> and <a href="https://github.com/sponsors/Senseiglobal" target="_blank" rel="noreferrer">Support Us</a></p></div>
</div>
<div id="onboard" class="panel"><h2>Start here</h2><p>Set your preferences, create your first project, then copy, export, or share the package.</p><div class="toolbar"><button class="btn primary" data-view="project">New Project</button><button class="btn" data-view="settings">Preferences</button><button class="btn ghost" id="dismiss">Dismiss</button></div></div><div class="cards"><button class="card" data-view="project"><div class="icon">+</div><h3>New Project</h3><p>Create a project package</p></button><button class="card" data-view="quote"><div class="icon">Q</div><h3>Quote</h3><p>Generate client quotes</p></button><button class="card" data-view="payment"><div class="icon">$</div><h3>Payment</h3><p>Calculate terms</p></button><button class="card" data-view="checklist"><div class="icon">OK</div><h3>Checklist</h3><p>Create checklists</p></button><button class="card" data-view="services"><div class="icon">S</div><h3>Services</h3><p>Manage services</p></button></div>
<div class="panel" id="connectionsPanel">
  <div class="toolbar" style="justify-content:space-between">
    <div>
      <h2>Connect tools</h2>
      <p>Use the app by itself, or connect it to Claude when you are ready.</p>
    </div>
  </div>
  <div class="connection-grid">
    <article class="connection-card" id="connectClaudeCard">
      <span class="status">Recommended</span>
      <h3>Connect Claude</h3>
      <p>Use Creative Studio MCP inside Claude as an MCP tool. Best for people who want the assistant to call the business tools directly.</p>
      <button class="btn primary" data-view="claude">Connect Claude</button>
    </article>
    <article class="connection-card">
      <span class="status soft">Optional</span>
      <h3>Enable more tools</h3>
      <p>Add more creative business tools later, such as invoices, client records, templates, and analytics.</p>
      <button class="btn" data-view="services">View Tools</button>
    </article>
    <article class="connection-card">
      <span class="status soft">Coming soon</span>
      <h3>Connect Google Drive</h3>
      <p>Store project exports in Google Drive when cloud storage support is added. For now, exports are saved locally.</p>
      <button class="btn" data-view="storage">Storage Options</button>
    </article>
  </div>
</div>
<div class="panel"><div class="toolbar" style="justify-content:space-between"><h2>Recent Projects</h2><button class="btn" id="refresh">Refresh</button></div><div id="recent" class="recent" aria-live="polite"></div></div>
<div class="developer-footer" id="developerFooter">
  <strong>Creative Studio MCP v1.0.0</strong><br>
  Built by Thomas Ogun under Senseiglobal. For support, updates, and contributions, use the GitHub repository or the Support Us button.
</div>
</section>
    <section id="project" class="section"><h1>New Project</h1><p>Generate a complete package.</p><div class="panel"><form id="projectForm"><div class="grid"><label>Client name<input name="client_name" value="Israel Thomas" required><small>Who is this for?</small></label><label>Service<select name="service" id="projectService"></select><small>Choose from your services.</small></label><label>Design fee<input name="design_fee" type="number" min="1" value="3000" required><small>Numbers only.</small></label><label>Upfront percent<input name="upfront_percent" type="number" min="0" max="100" value="70" required><small>Example: 70.</small></label><label>Project type<input name="project_type" value="Brand Identity Design" required><small>Short project category.</small></label></div><button class="btn primary" type="submit">Generate</button></form><div id="projectOut"></div></div></section>
    <section id="settings" class="section"><h1>Preferences</h1><div class="panel"><form id="settingsForm"><div class="grid"><label>Business name<input name="business_name"></label><label>Your name<input name="owner_name" autocomplete="name" placeholder="Your name"><small>This name is used for your greeting and client signature.</small></label><label>Email<input name="email"></label><label>Phone<input name="phone"></label><label>Website<input name="website"></label><label>Currency<input name="currency"></label></div><label>Payment terms<textarea name="payment_terms"></textarea></label><label>Services<textarea name="services_text"></textarea><small>One per line: Service | Price range</small></label><button class="btn primary" type="submit">Save</button></form></div></section>
    <section id="quote" class="section"><h1>Quote</h1><div class="panel"><form id="quoteForm"><div class="grid"><label>Client<input name="client_name" value="John Smith"></label><label>Service<select name="service" id="quoteService"></select></label><label>Fee<input name="design_fee" type="number" value="3000"></label></div><button class="btn primary">Generate</button></form><div id="quoteOut"></div></div></section>
    <section id="payment" class="section"><h1>Payment</h1><div class="panel"><form id="paymentForm"><div class="grid"><label>Total fee<input name="total_fee" type="number" value="5000"></label><label>Upfront percent<input name="upfront_percent" type="number" value="70"></label></div><button class="btn primary">Generate</button></form><div id="paymentOut"></div></div></section>
    <section id="checklist" class="section"><h1>Checklist</h1><div class="panel"><form id="checklistForm"><label>Project type<input name="project_type" value="Product packaging design"></label><button class="btn primary">Generate</button></form><div id="checklistOut"></div></div></section>
    <section id="services" class="section"><h1>Services</h1><div class="panel"><button class="btn primary" id="servicesBtn">Generate</button><div id="servicesOut"></div></div></section>

    <section id="claude" class="section"><h1>Connect Claude</h1><p>This is optional. The local dashboard works without Claude.</p><div class="panel"><h2>Beginner steps</h2><div class="recent"><div class="row"><div><h3>Step 1</h3><p>Install and start Creative Studio MCP first.</p></div></div><div class="row"><div><h3>Step 2</h3><p>Use the Claude setup button or guide from this repo to add the MCP server to Claude.</p></div></div><div class="row"><div><h3>Step 3</h3><p>Restart Claude, then ask: Use Creative Studio MCP to list my services.</p></div></div></div><div class="toolbar"><button class="btn primary" data-view="project">Use Local App</button><button class="btn" data-view="settings">Check Preferences</button></div></div></section>


    <section id="storage" class="section"><h1>Storage Options</h1><p>Exports are saved safely on this computer today. Cloud storage can be added later.</p><div class="panel"><div class="connection-grid"><article class="connection-card"><span class="status">Available</span><h3>Local exports</h3><p>TXT and MD files are saved in the exports folder inside the app folder.</p><button class="btn primary" data-view="project">Create Export</button></article><article class="connection-card"><span class="status soft">Coming soon</span><h3>Google Drive</h3><p>Future option for saving exports to your Drive account.</p><button class="btn" disabled aria-disabled="true">Coming Soon</button></article><article class="connection-card"><span class="status soft">Coming soon</span><h3>Dropbox or OneDrive</h3><p>Future options for teams that want shared project folders.</p><button class="btn" disabled aria-disabled="true">Coming Soon</button></article></div></div></section>

    <section id="bin" class="section"><h1>Bin</h1><div class="panel"><div class="toolbar"><button class="btn" id="binRefresh">Refresh</button><button class="btn danger" id="binEmpty">Empty Bin</button></div><div id="binList" class="recent"></div></div></section>
  </main>
  <aside class="preview" aria-label="Project package preview"><div class="toolbar" style="justify-content:space-between"><h2>Project Package Preview</h2><button class="btn ghost" id="clearPreview">Close</button></div><div id="preview"><p>Your generated package appears here.</p></div></aside>
</div>
<div id="toast" class="toast" role="status" aria-live="polite"></div>
<div id="modal" class="modal" role="dialog" aria-modal="true" aria-labelledby="welcome"><div class="modal-card"><h2 id="welcome">Welcome to Creative Studio MCP</h2><p>Create your first project package, export it, or share it. You can skip this guide.</p><div class="toolbar"><button class="btn primary" id="start">Start</button><button class="btn" id="skip">Skip</button></div></div></div>
<script>


// Greeting uses only the saved user name and the device time zone.
function greetingWord(){
  const hour = new Date().getHours();
  if(hour >= 5 && hour < 12) return "Good morning";
  if(hour >= 12 && hour < 17) return "Good afternoon";
  if(hour >= 17 && hour < 21) return "Good evening";
  return "Good night";
}
function firstNameFromProfile(profile){
  const fullName = String((profile && profile.owner_name) || "").trim();
  if(!fullName) return "";
  return fullName.split(/\s+/)[0];
}
function updateGreetingFromProfile(profile){
  const heading = document.querySelector("#dashboardGreeting");
  if(!heading) return;
  const firstName = firstNameFromProfile(profile);
  heading.textContent = firstName ? `${greetingWord()}, ${firstName}!` : `${greetingWord()}!`;
  heading.setAttribute("aria-label", heading.textContent);
}

let lastProject=null,lastPackageText="";const qs=s=>document.querySelector(s),qsa=s=>document.querySelectorAll(s);const toast=m=>{const t=qs("#toast");t.textContent=m;t.classList.add("show");clearTimeout(window.tt);window.tt=setTimeout(()=>t.classList.remove("show"),2200)};const api=async(p,d={})=>{const r=await fetch(p,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(d)});const j=await r.json();if(!r.ok)throw Error(j.error||"Something went wrong");return j.result};const fd=f=>Object.fromEntries(new FormData(f).entries());const esc=s=>String(s).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;");const txt=v=>typeof v==="string"?v:Array.isArray(v)?v.map((x,i)=>`${i+1}. ${x}`).join("\n"):Object.entries(v).map(([k,x])=>`${k}: ${x}`).join("\n");function block(title,value){const text=txt(value);return `<div class="output"><div class="toolbar" style="justify-content:space-between"><h3>${title}</h3><button class="btn" data-copy="${encodeURIComponent(text)}">Copy</button></div><pre>${esc(text)}</pre></div>`}function show(view){qsa(".section").forEach(x=>x.classList.remove("active"));qsa(".nav button").forEach(x=>x.classList.remove("active"));qs("#"+view).classList.add("active");qsa(`[data-view="${view}"]`).forEach(b=>b.classList.add("active"));if(view==="bin")loadBin();if(view==="home")loadRecent()}qsa("[data-view]").forEach(b=>b.onclick=()=>show(b.dataset.view));function setTheme(mode){if(mode==="system")localStorage.removeItem("theme");else localStorage.setItem("theme",mode);document.documentElement.dataset.theme=mode==="system"?(matchMedia("(prefers-color-scheme:dark)").matches?"dark":"light"):mode;toast(`Theme: ${mode}`)}let theme=localStorage.getItem("theme")||"system";setTheme(theme);qs("#theme").onclick=()=>{const next=theme==="system"?"dark":theme==="dark"?"light":"system";theme=next;setTheme(next)};async function loadServices(){const s=await api("/api/services");["projectService","quoteService"].forEach(id=>{qs("#"+id).innerHTML=Object.keys(s).map(x=>`<option>${esc(x)}</option>`).join("")})}async function loadProfile(){const p=await api("/api/profile");const f=qs("#settingsForm");Object.entries(p).forEach(([k,v])=>{if(f.elements[k]&&k!=="services")f.elements[k].value=v||""});f.elements.services_text.value=Object.entries(p.services||{}).map(([k,v])=>`${k} | ${v}`).join("\n");updateGreetingFromProfile(p)}function renderPackage(project){lastProject=project;const p=project.generated_package;lastPackageText=["CLIENT QUOTE",txt(p.client_quote),"","PAYMENT",txt(p.payment_breakdown),"","CHECKLIST",txt(p.project_checklist),"","DELIVERABLES",txt(p.deliverables),"","EMAIL",txt(p.client_email)].join("\n");const actions=`<div class="toolbar"><button class="btn primary" data-copy="${encodeURIComponent(lastPackageText)}">Copy</button><button class="btn" data-export="txt">Export TXT</button><button class="btn" data-export="md">Export MD</button><button class="btn" id="shareBtn">Share</button></div>`;qs("#preview").innerHTML=actions+block("Client Quote",p.client_quote)+block("Payment",p.payment_breakdown)+block("Checklist",p.project_checklist)+block("Deliverables",p.deliverables)+block("Email",p.client_email);qs("#projectOut").innerHTML=qs("#preview").innerHTML}async function loadRecent(){const r=await api("/api/recent",{limit:8});qs("#recent").innerHTML=r.length?r.map(p=>`<div class="row"><div><h3>${esc(p.client_name)}</h3><p>${esc(p.service)} at $${Number(p.design_fee).toLocaleString()}</p></div><div class="toolbar"><button class="btn" data-export-id="${p.id}" data-format="pdf">Export</button><button class="btn danger" data-delete="${p.id}">Delete</button></div></div>`).join(""):`<div class="output">No saved projects yet.</div>`}async function loadBin(){const r=await api("/api/bin",{limit:20});qs("#binList").innerHTML=r.length?r.map(p=>`<div class="row"><div><h3>${esc(p.client_name)}</h3><p>${esc(p.service)}</p></div><button class="btn" data-restore="${p.id}">Restore</button></div>`).join(""):`<div class="output">Bin is empty.</div>`}document.addEventListener("click",async e=>{const c=e.target.closest("[data-copy]");if(c){await navigator.clipboard.writeText(decodeURIComponent(c.dataset.copy));toast("Copied");return}const ex=e.target.closest("[data-export]");if(ex&&lastProject){const r=await api("/api/export",{project_id:lastProject.id,file_format:ex.dataset.export});toast(`Exported ${r.file_name}`);return}const exid=e.target.closest("[data-export-id]");if(exid){const r=await api("/api/export",{project_id:exid.dataset.exportId,file_format:exid.dataset.format});toast(`Exported ${r.file_name}`);return}const del=e.target.closest("[data-delete]");if(del){await api("/api/delete",{project_id:del.dataset.delete});toast("Moved to bin");loadRecent();return}const res=e.target.closest("[data-restore]");if(res){await api("/api/restore",{project_id:res.dataset.restore});toast("Restored");loadBin();loadRecent();return}});qs("#projectForm").onsubmit=async e=>{e.preventDefault();renderPackage(await api("/api/project",fd(e.target)));toast("Project generated");loadRecent()};qs("#quoteForm").onsubmit=async e=>{e.preventDefault();qs("#quoteOut").innerHTML=block("Quote",await api("/api/quote",fd(e.target)))};qs("#paymentForm").onsubmit=async e=>{e.preventDefault();qs("#paymentOut").innerHTML=block("Payment",await api("/api/payment",fd(e.target)))};qs("#checklistForm").onsubmit=async e=>{e.preventDefault();qs("#checklistOut").innerHTML=block("Checklist",await api("/api/checklist",fd(e.target)))};qs("#settingsForm").onsubmit=async e=>{e.preventDefault();const data=fd(e.target);await api("/api/save-profile",data);updateGreetingFromProfile(data);toast("Preferences saved");loadServices()};qs("#servicesBtn").onclick=async()=>qs("#servicesOut").innerHTML=block("Services",await api("/api/services"));qs("#refresh").onclick=loadRecent;qs("#binRefresh").onclick=loadBin;qs("#binEmpty").onclick=async()=>{await api("/api/empty-bin");toast("Bin emptied");loadBin()};qs("#clearPreview").onclick=()=>qs("#preview").innerHTML="<p>Your generated package appears here.</p>";document.addEventListener("click",async e=>{if(e.target.id==="shareBtn"){if(navigator.share)await navigator.share({title:"Project Package",text:lastPackageText});else{await navigator.clipboard.writeText(lastPackageText);toast("Share text copied")}}});if(!localStorage.getItem("seenOnboarding"))qs("#modal").classList.add("show");qs("#skip").onclick=()=>{localStorage.setItem("seenOnboarding","1");qs("#modal").classList.remove("show")};qs("#start").onclick=()=>{localStorage.setItem("seenOnboarding","1");qs("#modal").classList.remove("show");show("project")};loadServices();loadProfile();loadRecent();


// Creative Studio MCP UI polish: better feedback, export path notice, friendlier actions
(function () {
  const $ = (selector) => document.querySelector(selector);
  const $$ = (selector) => Array.from(document.querySelectorAll(selector));

  function ensureConfirmBox() {
    let box = $("#actionConfirm");
    if (!box) {
      box = document.createElement("div");
      box.id = "actionConfirm";
      box.className = "action-confirm";
      box.setAttribute("role", "status");
      box.setAttribute("aria-live", "polite");
      document.body.appendChild(box);
    }
    return box;
  }

  window.showActionConfirm = function (title, detail, path) {
    const box = ensureConfirmBox();
    box.innerHTML = `<b>${title}</b><span>${detail || "Done."}</span>${path ? `<code>${path}</code>` : ""}`;
    box.classList.add("show");
    clearTimeout(window.__csConfirmTimer);
    window.__csConfirmTimer = setTimeout(() => box.classList.remove("show"), 4600);
  };

  window.showSoftToast = function (title, detail) {
    const toastBox = $("#toast");
    if (!toastBox) return;
    toastBox.innerHTML = `<strong>${title}</strong>${detail ? `<small>${detail}</small>` : ""}`;
    toastBox.classList.add("show");
    clearTimeout(window.__csToastTimer);
    window.__csToastTimer = setTimeout(() => toastBox.classList.remove("show"), 2600);
  };

  const originalFetch = window.fetch.bind(window);
  window.fetch = async function (resource, options) {
    const activeButton = document.activeElement && document.activeElement.tagName === "BUTTON" ? document.activeElement : null;
    if (activeButton) activeButton.dataset.busy = "true";
    try {
      const response = await originalFetch(resource, options);
      return response;
    } finally {
      if (activeButton) setTimeout(() => { delete activeButton.dataset.busy; }, 180);
    }
  };

  document.addEventListener("click", function (event) {
    const button = event.target.closest("button");
    if (!button || !button.animate) return;
    button.animate(
      [{ transform: "scale(1)" }, { transform: "scale(.97)" }, { transform: "scale(1)" }],
      { duration: 170, easing: "ease-out" }
    );
  });

  document.addEventListener("click", function (event) {
    const tipButton = event.target.closest(".tip");
    $$(".tip.is-open").forEach((tip) => {
      if (tip !== tipButton) tip.classList.remove("is-open");
    });
    if (tipButton) tipButton.classList.toggle("is-open");
  });

  const previousToast = window.toast;
  window.toast = function (message) {
    window.showSoftToast("Done", message);
    if (typeof previousToast === "function") {
      try { previousToast(message); } catch (error) {}
    }
  };

  const previousApi = window.api;
  if (typeof previousApi === "function") {
    window.api = async function (path, data) {
      const result = await previousApi(path, data);
      if (path === "/api/export" && result) {
        const format = (result.format || (data && data.file_format) || "file").toUpperCase();
        const fileName = result.file_name || "your export file";
        const savedPath = result.path || result.file_path || fileName;
        window.showSoftToast(`Exported ${format}`, `Saved as ${fileName}`);
        window.showActionConfirm("Export saved", "Your file is ready in the exports folder.", savedPath);
      }
      if (path === "/api/delete") {
        window.showActionConfirm("Moved to bin", "You can restore it from the Bin section.");
      }
      if (path === "/api/restore") {
        window.showActionConfirm("Restored", "The project is back in Recent Projects.");
      }
      if (path === "/api/save-profile") {
        window.showActionConfirm("Preferences saved", "Your business details will be used in new packages.");
      }
      return result;
    };
  }

  function improvePreviewLabels() {
    const preview = $("#preview");
    if (!preview || !window.MutationObserver) return;
    const observer = new MutationObserver(() => {
      $$("#preview .btn[data-export='txt']").forEach((button) => button.textContent = "Export TXT");
      $$("#preview .btn[data-export='md']").forEach((button) => button.textContent = "Export MD");
      $$("#preview #shareBtn").forEach((button) => button.textContent = "Share");
      $$("#preview .output h3").forEach((heading) => heading.setAttribute("tabindex", "0"));
    });
    observer.observe(preview, { childList: true, subtree: true });
  }

  improvePreviewLabels();
})();



// Generate results repair: capture the New Project form and always show the package.
(function () {
  const $ = (selector) => document.querySelector(selector);

  function htmlEscape(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;");
  }

  function asText(value) {
    if (typeof value === "string") return value;
    if (Array.isArray(value)) return value.map((item, index) => `${index + 1}. ${item}`).join("\n");
    if (value && typeof value === "object") {
      return Object.entries(value).map(([key, item]) => `${key}: ${item}`).join("\n");
    }
    return String(value ?? "");
  }

  function notifyUser(title, detail) {
    if (window.showSoftToast) {
      window.showSoftToast(title, detail);
      return;
    }
    const toast = $("#toast");
    if (!toast) return;
    toast.textContent = detail ? `${title}: ${detail}` : title;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 2600);
  }

  async function apiPost(path, payload) {
    const response = await fetch(path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload || {})
    });
    let data = {};
    try {
      data = await response.json();
    } catch (error) {
      throw new Error("The app did not return a readable response.");
    }
    if (!response.ok || data.error) {
      throw new Error(data.error || "The project could not be generated.");
    }
    return data.result;
  }

  function section(title, value) {
    const text = asText(value);
    return `<section class="output" aria-label="${htmlEscape(title)}">
      <div class="toolbar" style="justify-content:space-between">
        <h3>${htmlEscape(title)}</h3>
        <button class="btn" type="button" data-copy="${encodeURIComponent(text)}">Copy</button>
      </div>
      <pre>${htmlEscape(text)}</pre>
    </section>`;
  }

  function renderGeneratedProject(project) {
    const pkg = project.generated_package || {};
    const packageText = [
      "CLIENT QUOTE", asText(pkg.client_quote), "",
      "PAYMENT", asText(pkg.payment_breakdown), "",
      "CHECKLIST", asText(pkg.project_checklist), "",
      "DELIVERABLES", asText(pkg.deliverables), "",
      "EMAIL", asText(pkg.client_email)
    ].join("\n");

    window.lastProject = project;
    window.lastPackageText = packageText;

    const actions = `<div class="generated-actions">
      <button class="btn primary" type="button" data-copy="${encodeURIComponent(packageText)}">Copy Full Package</button>
      <button class="btn" type="button" data-export="txt">Export TXT</button>
      <button class="btn" type="button" data-export="md">Export MD</button>
      <button class="btn" type="button" id="shareBtn">Share</button>
    </div>`;

    const html = `<div class="generated-results">
      <div class="result-banner" role="status" aria-live="polite">
        <strong>Project package generated</strong>
        <p>Review the sections below, then copy, export, or share.</p>
      </div>
      ${actions}
      ${section("Client Quote", pkg.client_quote)}
      ${section("Payment Breakdown", pkg.payment_breakdown)}
      ${section("Project Checklist", pkg.project_checklist)}
      ${section("Deliverables", pkg.deliverables)}
      ${section("Client Email", pkg.client_email)}
    </div>`;

    const projectOut = $("#projectOut");
    const preview = $("#preview");
    if (projectOut) {
      projectOut.innerHTML = html;
      projectOut.scrollIntoView({ behavior: "smooth", block: "start" });
    }
    if (preview) preview.innerHTML = html;

    const app = $(".app");
    const expand = $("#previewExpand");
    if (app) app.classList.remove("preview-collapsed");
    if (expand) expand.classList.remove("show");
  }

  function validate(payload) {
    const fee = Number(payload.design_fee);
    const upfront = Number(payload.upfront_percent);
    if (!String(payload.client_name || "").trim()) return "Please enter the client name.";
    if (!String(payload.service || "").trim()) return "Please choose a service.";
    if (!Number.isFinite(fee) || fee <= 0) return "Please enter a design fee above 0.";
    if (!Number.isFinite(upfront) || upfront < 0 || upfront > 100) return "Upfront percent must be from 0 to 100.";
    if (!String(payload.project_type || "").trim()) return "Please enter the project type.";
    return "";
  }

  const form = $("#projectForm");
  if (!form || form.dataset.resultsRepairInstalled === "true") return;
  form.dataset.resultsRepairInstalled = "true";

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    event.stopPropagation();
    if (event.stopImmediatePropagation) event.stopImmediatePropagation();

    const submit = form.querySelector("button[type='submit']");
    const output = $("#projectOut");
    const payload = Object.fromEntries(new FormData(form).entries());
    const error = validate(payload);

    if (error) {
      if (output) output.innerHTML = `<div class="form-message error">${htmlEscape(error)}</div>`;
      notifyUser("Please check the form", error);
      return false;
    }

    try {
      if (submit) {
        submit.dataset.busy = "true";
        submit.disabled = true;
      }
      if (output) {
        output.innerHTML = `<div class="result-banner" role="status"><strong>Generating package...</strong><p>Please wait a moment.</p></div>`;
      }
      const project = await apiPost("/api/project", payload);
      renderGeneratedProject(project);
      notifyUser("Project generated", "Your results are now shown below and in the preview.");
      if (window.showActionConfirm) {
        window.showActionConfirm("Results ready", "Your project package is visible on the screen.");
      }
      if (typeof window.loadRecent === "function") window.loadRecent();
      return false;
    } catch (err) {
      const message = err && err.message ? err.message : "The project could not be generated.";
      if (output) output.innerHTML = `<div class="form-message error">${htmlEscape(message)}</div>`;
      notifyUser("Generate failed", message);
      return false;
    } finally {
      if (submit) {
        delete submit.dataset.busy;
        submit.disabled = false;
      }
    }
  }, true);
})();

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
