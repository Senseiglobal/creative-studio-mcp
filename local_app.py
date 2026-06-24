import json
import mimetypes
import os
import socket
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse

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
    save_brand_profile,
    save_project,
)

HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark light">
  <title>Creative Studio MCP</title>
  <link rel="icon" href="/assets/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon-16.png">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png">
  <link rel="manifest" href="/assets/site.webmanifest">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,400..700,0..1,0&display=swap" rel="stylesheet">
  <style>
    :root {
      --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px; --space-5: 20px; --space-6: 24px; --space-7: 32px; --space-8: 40px;
      --radius-1: 10px; --radius-2: 14px; --radius-3: 18px; --radius-4: 24px;
      --display: 56px; --h1: 40px; --h2: 32px; --h3: 24px; --section: 20px; --body: 16px; --caption: 13px;
      --bg: #0b0d12; --surface: #11151d; --surface-2: #161b25; --surface-3: #1e2531;
      --text: #f8fafc; --muted: #a7b0bf; --soft: #778195; --line: #2b3342;
      --accent: #8b5cf6; --accent-2: #7c3aed; --success: #22c55e; --warning: #f59e0b; --danger: #ef4444;
      --shadow-1: 0 1px 2px rgba(0,0,0,.16); --shadow-2: 0 10px 28px rgba(0,0,0,.20); --focus: 0 0 0 4px rgba(139,92,246,.22);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
    }
    [data-theme="light"] {
      --bg: #f7f7fb; --surface: #ffffff; --surface-2: #f8fafc; --surface-3: #f1f5f9;
      --text: #111827; --muted: #667085; --soft: #98a2b3; --line: #e5e7eb;
      --shadow-1: 0 1px 2px rgba(16,24,40,.06); --shadow-2: 0 16px 40px rgba(16,24,40,.1);
    }
    [data-accent="red"] { --accent: #ef4444; --accent-2: #dc2626; --focus: 0 0 0 4px rgba(239,68,68,.26); }
    [data-accent="green"] { --accent: #22c55e; --accent-2: #16a34a; --focus: 0 0 0 4px rgba(34,197,94,.24); }
    [data-accent="blue"] { --accent: #3b82f6; --accent-2: #2563eb; --focus: 0 0 0 4px rgba(59,130,246,.24); }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body { margin: 0; background: var(--bg); color: var(--text); font-size: var(--body); line-height: 1.5; letter-spacing: 0; }
    button, input, select, textarea { font: inherit; }
    button { cursor: pointer; }
    a { color: inherit; }
    .mi { font-family: "Material Symbols Rounded"; font-size: 21px; line-height: 1; display: inline-flex; font-variation-settings: "FILL" 0, "wght" 500, "GRAD" 0, "opsz" 24; }
    .skip { position: fixed; left: 16px; top: 16px; transform: translateY(-150%); z-index: 99; background: var(--text); color: var(--bg); padding: 10px 14px; border-radius: 999px; }
    .skip:focus { transform: translateY(0); }
    :focus-visible { outline: 0; box-shadow: var(--focus); }
    .shell { min-height: 100vh; display: grid; grid-template-columns: 240px minmax(0, 1fr) minmax(380px, 420px); transition: grid-template-columns 180ms ease; }
    .shell.inspector-wide { grid-template-columns: 240px minmax(360px, .8fr) minmax(560px, 680px); }
    .shell.inspector-collapsed { grid-template-columns: 240px minmax(0, 1fr) 72px; }
    .shell.inspector-closed { grid-template-columns: 240px minmax(0, 1fr); }
    .sidebar { position: sticky; top: 0; height: 100vh; padding: var(--space-6) var(--space-4); border-right: 1px solid var(--line); background: color-mix(in srgb, var(--surface), transparent 4%); overflow: auto; display: flex; flex-direction: column; }
    .brand { display: flex; gap: var(--space-3); align-items: center; padding: 0 var(--space-2) var(--space-6); }
    .logo { width: 46px; height: 46px; border-radius: var(--radius-2); display: grid; place-items: center; overflow: hidden; background: var(--surface-2); border: 1px solid color-mix(in srgb, var(--accent), var(--line) 42%); box-shadow: 0 8px 22px color-mix(in srgb, var(--accent), transparent 84%); }
    .logo img { width: 100%; height: 100%; object-fit: cover; display: block; }
    .brand strong { display: block; font-size: 15px; line-height: 1.15; }
    .brand span { color: var(--muted); font-size: var(--caption); }
    .nav-group { margin-top: var(--space-5); }
    .nav-label { padding: 0 var(--space-3) var(--space-2); color: var(--soft); font-size: 11px; font-weight: 850; text-transform: uppercase; letter-spacing: .12em; }
    .nav { display: grid; gap: var(--space-1); }
    .nav button, .nav a { min-height: 44px; border: 0; border-radius: var(--radius-2); background: transparent; color: var(--muted); text-align: left; display: flex; align-items: center; gap: var(--space-3); padding: 0 var(--space-3); font-weight: 740; text-decoration: none; transition: background 160ms ease, color 160ms ease, transform 160ms ease; }
    .nav button:hover, .nav a:hover, .nav button.active { background: color-mix(in srgb, var(--accent), transparent 86%); color: var(--text); }
    .nav button.active { box-shadow: inset 3px 0 0 var(--accent); }
    .theme-dots { display: flex; gap: var(--space-2); padding: var(--space-3); }
    .dot { width: 34px; height: 34px; border-radius: 999px; border: 2px solid transparent; display: grid; place-items: center; background: var(--surface-2); }
    .dot span { width: 18px; height: 18px; border-radius: 999px; display: block; }
    .dot.active { border-color: var(--accent); box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent), transparent 78%); }
    .dot.red span { background: #ef4444; } .dot.green span { background: #22c55e; } .dot.blue span { background: #3b82f6; }
    .sidebar-footer { margin-top: auto; padding: var(--space-8) var(--space-3) 0; color: var(--soft); font-size: 12px; }
    .version-pill { display: inline-flex; align-items: center; justify-content: center; min-height: 32px; border: 1px solid var(--line); border-radius: 999px; padding: 0 12px; color: var(--muted); background: var(--surface-2); font-weight: 800; line-height: 1; }
    .workspace-wrap { min-width: 0; padding: var(--space-7); }
    .workspace { max-width: 1200px; margin: 0 auto; }
    .view { display: none; animation: enter 160ms ease both; }
    .view.active { display: block; }
    .page-head { display: flex; justify-content: space-between; align-items: flex-start; gap: var(--space-6); margin-bottom: var(--space-7); }
    .eyebrow { margin: 0 0 var(--space-2); color: var(--accent); font-size: var(--caption); font-weight: 850; text-transform: uppercase; letter-spacing: .1em; }
    h1, h2, h3, p { margin-top: 0; }
    h1 { margin-bottom: var(--space-3); font-size: var(--h1); line-height: 1.05; letter-spacing: -.035em; }
    h2 { margin-bottom: var(--space-2); font-size: var(--h2); line-height: 1.12; letter-spacing: -.025em; }
    h3 { margin-bottom: var(--space-2); font-size: var(--section); line-height: 1.2; letter-spacing: -.015em; }
    p { color: var(--muted); }
    .display { font-size: clamp(40px, 5vw, var(--display)); line-height: .98; letter-spacing: -.05em; }
    .btn { min-height: 44px; border-radius: var(--radius-2); display: inline-flex; align-items: center; justify-content: center; gap: var(--space-2); padding: 0 var(--space-4); border: 1px solid var(--line); background: var(--surface); color: var(--text); font-weight: 780; line-height: 1; white-space: nowrap; text-align: center; flex-shrink: 0; text-decoration: none; transition: transform 160ms ease, box-shadow 160ms ease, background 160ms ease, border-color 160ms ease, opacity 160ms ease; }
    .btn:hover { transform: translateY(-1px); box-shadow: var(--shadow-1); }
    .btn:active { transform: scale(.98); }
    .btn.primary { background: var(--accent); border-color: var(--accent); color: #fff; box-shadow: 0 8px 24px color-mix(in srgb, var(--accent), transparent 86%); }
    .btn.primary:hover { background: var(--accent-2); box-shadow: 0 10px 28px color-mix(in srgb, var(--accent), transparent 82%); }
    .btn.secondary { background: var(--surface-2); }
    .btn.ghost { background: transparent; border-color: transparent; }
    .btn.danger { color: var(--danger); background: color-mix(in srgb, var(--danger), transparent 92%); border-color: color-mix(in srgb, var(--danger), transparent 78%); }
    .btn.icon { width: 44px; min-width: 44px; height: 44px; padding: 0; }
    .btn[disabled] { opacity: .5; pointer-events: none; }
    .btn.loading { min-width: 132px; opacity: 1; }
    .btn-loader { display: inline-flex; align-items: center; gap: 10px; }
    .loader-logo { position: relative; width: 28px; height: 28px; display: inline-grid; place-items: center; }
    .loader-logo img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain; opacity: .42; }
    .loader-letter { position: relative; z-index: 1; font-weight: 950; font-size: 16px; letter-spacing: 0; color: var(--text); text-shadow: 0 1px 0 rgba(0,0,0,.18); }
    .loader-letter.c { animation: logoCFade 1.05s ease-in-out infinite; }
    .loader-letter.s { margin-left: -4px; animation: logoSFade 1.05s ease-in-out infinite; }
    .loader-heartline { width: 34px; height: 5px; border-radius: 999px; background: repeating-linear-gradient(90deg, #7aa262 0 5px, transparent 5px 8px); transform-origin: left center; animation: logoHeartbeat 1.05s ease-in-out infinite; }
    .hero, .panel, .learning-card, .feedback-card { border: 1px solid var(--line); border-radius: var(--radius-4); background: var(--surface); box-shadow: var(--shadow-1); }
    .hero { padding: var(--space-8); margin-bottom: var(--space-7); background: linear-gradient(180deg, color-mix(in srgb, var(--surface), transparent 0%), color-mix(in srgb, var(--surface-2), transparent 0%)); }
    .hero-actions, .actions { display: flex; flex-wrap: wrap; gap: var(--space-3); align-items: center; }
    .hero-actions { margin-top: var(--space-5); }
    .section { margin-top: var(--space-7); }
    .section-head { display: flex; justify-content: space-between; align-items: end; gap: var(--space-5); margin-bottom: var(--space-5); }
    .card-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--space-4); }
    .quick-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); }
    .card { min-height: 150px; border: 1px solid var(--line); border-radius: var(--radius-3); background: var(--surface); color: var(--text); box-shadow: var(--shadow-1); padding: var(--space-5); text-align: left; transition: transform 160ms ease, box-shadow 160ms ease, border-color 160ms ease; }
    .card:hover { transform: translateY(-2px); box-shadow: 0 10px 28px rgba(0,0,0,.16); border-color: color-mix(in srgb, var(--accent), var(--line) 70%); }
    .card-icon { width: 44px; height: 44px; display: grid; place-items: center; border-radius: var(--radius-2); background: color-mix(in srgb, var(--accent), transparent 88%); color: var(--accent); margin-bottom: var(--space-4); }
    .card-row { display: flex; align-items: center; justify-content: space-between; gap: var(--space-4); }
    .panel { max-width: 900px; padding: var(--space-7); }
    form { display: grid; gap: var(--space-7); }
    .form-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--space-6); }
    .other-field { display: none; margin-top: var(--space-2); }
    .other-field.show { display: grid; }
    .remove-selected { display: none; width: max-content; margin-top: var(--space-2); }
    .remove-selected.show { display: inline-flex; }
    label { display: grid; gap: var(--space-2); font-weight: 780; }
    small { color: var(--muted); font-size: var(--caption); font-weight: 500; }
    input, select, textarea { width: 100%; min-height: 48px; border: 1px solid var(--line); border-radius: var(--radius-2); background: var(--surface-2); color: var(--text); padding: 0 var(--space-4); transition: border-color 160ms ease, box-shadow 160ms ease; }
    textarea { min-height: 132px; padding-top: var(--space-4); resize: vertical; }
    input:focus, select:focus, textarea:focus { border-color: var(--accent); box-shadow: var(--focus); outline: 0; }
    .recent-list, .lesson-list, .faq-list, .custom-list { display: grid; gap: var(--space-3); }
    .custom-manager { margin-top: var(--space-5); display: grid; gap: var(--space-4); }
    .custom-chip { min-height: 44px; display: flex; align-items: center; justify-content: space-between; gap: var(--space-3); border: 1px solid var(--line); border-radius: var(--radius-2); background: var(--surface-2); padding: var(--space-2) var(--space-3); }
    .custom-chip span { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .recent-item, .lesson-card { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: var(--space-4); align-items: center; border: 1px solid var(--line); border-radius: var(--radius-3); background: var(--surface); padding: var(--space-4); }
    .lesson-card.complete { border-color: color-mix(in srgb, var(--success), var(--line) 45%); }
    .lesson-card p { margin-bottom: 0; }
    .progress-wrap { height: 10px; border-radius: 999px; overflow: hidden; background: var(--surface-3); }
    .progress-bar { height: 100%; width: 0%; background: var(--accent); transition: width 180ms ease; }
    .empty { min-height: 160px; display: grid; place-items: center; text-align: center; border: 1px dashed var(--line); border-radius: var(--radius-3); background: var(--surface-2); color: var(--muted); padding: var(--space-7); }
    .empty .mi { color: var(--accent); font-size: 38px; margin-bottom: var(--space-3); }
    .notice { margin-top: var(--space-5); border: 1px solid var(--line); border-radius: var(--radius-2); background: var(--surface-2); padding: var(--space-4); }
    .notice.success { color: var(--success); border-color: color-mix(in srgb, var(--success), transparent 70%); }
    .notice.error { color: var(--danger); border-color: color-mix(in srgb, var(--danger), transparent 70%); }
    .inspector { position: sticky; top: 0; height: 100vh; overflow: auto; resize: horizontal; min-width: 380px; max-width: 760px; border-left: 1px solid var(--line); background: color-mix(in srgb, var(--surface), transparent 2%); padding: var(--space-5); }
    .inspector-inner { display: grid; grid-template-columns: 14px minmax(0, 1fr); gap: var(--space-4); min-height: 100%; }
    .inspector-handle { width: 14px; border: 0; border-radius: 999px; background: color-mix(in srgb, var(--line), transparent 12%); color: var(--soft); min-height: 240px; align-self: stretch; display: grid; place-items: center; padding: 0; }
    .inspector-handle:hover { background: color-mix(in srgb, var(--accent), transparent 78%); color: var(--accent); }
    .inspector-head { display: flex; justify-content: space-between; align-items: start; gap: var(--space-4); margin-bottom: var(--space-5); }
    .inspector-title p { margin: 4px 0 0; font-size: var(--caption); }
    .inspector-actions, .inspector-toolbar { display: flex; flex-wrap: wrap; gap: var(--space-2); }
    .inspector-toolbar { margin-bottom: var(--space-5); }
    .inspector-body { display: grid; gap: var(--space-4); }
    .preview-section { border: 1px solid var(--line); border-radius: var(--radius-3); background: var(--surface-2); overflow: hidden; }
    .preview-section summary { min-height: 52px; display: flex; align-items: center; justify-content: space-between; gap: var(--space-3); padding: 0 var(--space-4); list-style: none; cursor: pointer; font-weight: 820; }
    .preview-section summary::-webkit-details-marker { display: none; }
    .preview-doc { padding: var(--space-4); border-top: 1px solid var(--line); }
    .doc-text { white-space: pre-wrap; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 14px; line-height: 1.72; color: var(--text); }
    .check-list, .bullet-list { display: grid; gap: var(--space-3); margin: 0; padding: 0; list-style: none; }
    .check-row { display: grid; grid-template-columns: 24px minmax(0, 1fr) auto auto; align-items: start; gap: var(--space-3); padding: var(--space-3); border: 1px solid var(--line); border-radius: var(--radius-2); background: color-mix(in srgb, var(--surface-3) 72%, transparent); font-size: 16px; line-height: 1.6; }
    .check-row input { width: 18px; height: 18px; margin-top: 2px; accent-color: var(--accent); }
    .check-row.checked span { color: var(--muted); text-decoration: line-through; }
    .check-actions { display: flex; flex-wrap: wrap; gap: var(--space-2); padding: var(--space-3) var(--space-4); border-top: 1px solid var(--line); background: color-mix(in srgb, var(--surface-3) 58%, transparent); }
    .check-row .mini-action { min-height: 36px; padding: 0 10px; font-size: var(--caption); }
    .bullet-row { padding: var(--space-3); border: 1px solid var(--line); border-radius: var(--radius-2); background: color-mix(in srgb, var(--surface-3) 72%, transparent); font-size: 15px; line-height: 1.55; }
    .kv { display: grid; gap: var(--space-2); }
    .kv-row { display: flex; justify-content: space-between; gap: var(--space-3); border-bottom: 1px solid var(--line); padding-bottom: var(--space-2); }
    .kv-row:last-child { border-bottom: 0; padding-bottom: 0; }
    .token { color: var(--accent); }
    .inspector-rail { display: none; height: 100vh; border-left: 1px solid var(--line); background: var(--surface); padding: var(--space-4) var(--space-2); }
    .shell.inspector-collapsed .inspector { display: none; }
    .shell.inspector-collapsed .inspector-rail { display: grid; align-content: start; gap: var(--space-3); }
    .shell.inspector-closed .inspector, .shell.inspector-closed .inspector-rail { display: none; }
    .tooltip { position: fixed; z-index: 120; max-width: 280px; padding: 10px 12px; border: 1px solid var(--line); border-radius: var(--radius-2); background: var(--text); color: var(--bg); font-size: var(--caption); box-shadow: var(--shadow-2); opacity: 0; transform: translateY(6px); pointer-events: auto; transition: opacity 150ms ease, transform 150ms ease; display: flex; align-items: start; gap: var(--space-2); }
    .tooltip.show { opacity: 1; transform: translateY(0); }
    .tooltip button { border: 0; background: transparent; color: inherit; min-width: 24px; min-height: 24px; border-radius: 999px; display: inline-flex; align-items: center; justify-content: center; }
    .toast { position: fixed; right: 18px; bottom: 18px; z-index: 90; max-width: min(420px, calc(100vw - 32px)); background: var(--text); color: var(--bg); padding: 14px 16px; border-radius: var(--radius-2); box-shadow: var(--shadow-2); opacity: 0; transform: translateY(10px); transition: opacity 160ms ease, transform 160ms ease; }
    .toast.show { opacity: 1; transform: translateY(0); }
    .help-fab { position: fixed; right: 18px; bottom: 84px; z-index: 88; min-height: 52px; padding: 0 18px; border-radius: 999px; box-shadow: var(--shadow-2); }
    .walkthrough-list { display: grid; gap: var(--space-3); margin-top: var(--space-4); }
    .walkthrough-step { border: 1px solid var(--line); border-radius: var(--radius-3); background: var(--surface-2); padding: var(--space-4); display: grid; gap: var(--space-2); }
    .walkthrough-step strong { display: inline-flex; align-items: center; gap: var(--space-2); }
    .step-number { width: 28px; height: 28px; border-radius: 999px; display: inline-flex; align-items: center; justify-content: center; background: color-mix(in srgb, var(--accent), transparent 78%); color: var(--accent); font-weight: 900; flex: 0 0 auto; }
    .walkthrough-step p { margin-bottom: 0; }
    .modal-backdrop { position: fixed; inset: 0; z-index: 130; display: none; place-items: center; background: rgba(0,0,0,.48); padding: var(--space-5); }
    .modal-backdrop.show { display: grid; }
    .modal { width: min(520px, 100%); border: 1px solid var(--line); border-radius: var(--radius-4); background: var(--surface); box-shadow: var(--shadow-2); padding: var(--space-6); }
    .feedback-card { padding: var(--space-5); margin-top: var(--space-6); }
    .faq details { border: 1px solid var(--line); border-radius: var(--radius-2); background: var(--surface); padding: var(--space-4); }
    .faq summary { cursor: pointer; font-weight: 820; }
    .mobile-accent-dots { display: none; }
    .bottom-nav { display: none; }
    @keyframes enter { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
    @keyframes spin { to { transform: rotate(360deg); } }
    @media (max-width: 1360px) {
      .shell, .shell.inspector-wide, .shell.inspector-collapsed, .shell.inspector-closed { grid-template-columns: minmax(0, 1fr); }
      .sidebar { display: none; }
      .workspace-wrap { padding: var(--space-5); padding-bottom: 116px; }
      .inspector { position: fixed; inset: auto 0 0 0; z-index: 70; height: min(72vh, 720px); min-width: 0; max-width: none; resize: none; border-left: 0; border-top: 1px solid var(--line); border-radius: 24px 24px 0 0; box-shadow: var(--shadow-2); }
      .inspector-inner { grid-template-columns: 1fr; }
      .inspector-handle { display: none; }
      .shell.inspector-collapsed .inspector-rail { position: fixed; right: 16px; bottom: 86px; width: 56px; height: 56px; border-radius: 999px; padding: 0; place-items: center; box-shadow: var(--shadow-2); z-index: 75; }
      .mobile-accent-dots { position: fixed; left: 12px; right: 12px; bottom: 80px; z-index: 80; display: flex; align-items: center; justify-content: center; gap: var(--space-2); padding: 8px 10px; border: 1px solid var(--line); border-radius: 999px; background: color-mix(in srgb, var(--surface), transparent 5%); box-shadow: var(--shadow-1); width: max-content; max-width: calc(100vw - 24px); margin: 0 auto; }
      .mobile-accent-dots .dot { width: 30px; height: 30px; }
      .mobile-accent-dots .dot span { width: 16px; height: 16px; }
      .bottom-nav { position: fixed; left: 12px; right: 12px; bottom: 12px; z-index: 80; display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; padding: 8px; border: 1px solid var(--line); border-radius: 22px; background: color-mix(in srgb, var(--surface), transparent 5%); box-shadow: var(--shadow-2); }
      .bottom-nav button { min-height: 48px; border: 0; border-radius: 16px; background: transparent; color: var(--muted); display: grid; place-items: center; }
      .bottom-nav button.active { background: color-mix(in srgb, var(--accent), transparent 84%); color: var(--text); }
      .help-fab { right: 16px; bottom: 138px; width: 56px; min-width: 56px; padding: 0; }
      .help-fab .help-text { display: none; }
    }
    @media (max-width: 760px) {
      .page-head, .section-head { align-items: start; flex-direction: column; }
      .hero { padding: var(--space-6); }
      .card-grid, .quick-grid, .form-grid { grid-template-columns: 1fr; }
      .panel { padding: var(--space-5); }
      .recent-item, .lesson-card { grid-template-columns: 1fr; }
      .display { font-size: 40px; }
    }
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after { animation-duration: .001ms !important; transition-duration: .001ms !important; scroll-behavior: auto !important; }
    }
  </style>
</head>
<body>
  <a class="skip" href="#workspace">Skip to content</a>
  <div class="shell" id="shell">
    <aside class="sidebar" aria-label="Sidebar navigation">
      <div class="brand"><div class="logo"><img src="/assets/logo-64.png" alt="Creative Studio logo"></div><div><strong>Creative Studio</strong></div></div>
      <div class="nav-group"><div class="nav-label">Workspace</div><nav class="nav">
        <button class="active" data-view="dashboard" data-tip="Your home desk. Start, continue, or check recent work."><span class="mi">dashboard</span>Dashboard</button>
        <button data-view="project" data-tip="Start a new client job from scratch."><span class="mi">folder_open</span>Projects</button>
        <button data-view="clients" data-tip="Client history is planned. Recent project names help for now."><span class="mi">groups</span>Clients</button>
        <button data-view="learn" data-tip="Simple lessons that explain the app in plain English."><span class="mi">school</span>Learn</button>
      </nav></div>
      <div class="nav-group"><div class="nav-label">Tools</div><nav class="nav">
        <button data-view="quote" data-tip="A Quote is like a price note you send before work begins."><span class="mi">request_quote</span>Quote</button>
        <button data-view="payment" data-tip="Payment Breakdown shows what the client pays now and later."><span class="mi">payments</span>Payment</button>
        <button data-view="checklist" data-tip="Checklist is your project recipe."><span class="mi">checklist</span>Checklist</button>
        <button data-view="services" data-tip="Save your common offers so quotes are faster."><span class="mi">design_services</span>Services</button>
      </nav></div>
      <div class="nav-group"><div class="nav-label">Business</div><nav class="nav">
        <button data-view="settings" data-tip="Set your name, business, services, theme, and memory."><span class="mi">settings</span>Settings</button>
        <button id="themeBtn" type="button" data-tip="Switch day or night mode."><span class="mi">dark_mode</span>Theme</button>
        <a href="https://github.com/sponsors/Senseiglobal" target="_blank" rel="noreferrer" data-tip="Support open development with any contribution."><span class="mi">favorite</span>Support</a>
      </nav></div>
      <div class="nav-group"><div class="nav-label">Accent theme</div><div class="theme-dots" id="themeDots"></div></div>
      <div class="sidebar-footer" aria-label="App version">
        <span class="version-pill">Version 1.0 Beta</span>
      </div>
    </aside>

    <main class="workspace-wrap" id="workspace">
      <div class="workspace">
        <section id="dashboard" class="view active">
          <div class="hero">
            <p class="eyebrow">Studio HQ</p>
            <div class="page-head"><div>
              <h1 class="display" id="greeting">Welcome to Creative Studio</h1>
              <p>Pick up where you left off or start a new client package.</p>
              <div class="hero-actions">
                <button class="btn primary" data-view="project" type="button" data-tip="Create a complete client package in one step."><span class="mi">add</span>New Project</button>
                <button class="btn secondary" id="continueRecent" type="button" data-tip="Go back to the last project you worked on."><span class="mi">play_arrow</span>Continue Recent</button>
                <button class="btn ghost" data-view="learn" type="button" data-tip="Learn what each tool does in simple language."><span class="mi">school</span>Learn</button>
              </div>
            </div></div>
          </div>

          <section class="section">
            <div class="section-head"><div><h2>Recent Projects</h2><p>Saved locally on this computer.</p></div><button class="btn secondary" id="refreshRecent" type="button"><span class="mi">refresh</span>Refresh</button></div>
            <div id="recent" class="recent-list"></div>
          </section>

          <section class="section">
            <div class="section-head"><div><h2>Quick Actions</h2><p>Use the fastest path for the job.</p></div></div>
            <div class="card-grid quick-grid">
              <button class="card" data-view="project" type="button" data-tip="A Project is like a folder for one client job."><div class="card-icon"><span class="mi">note_stack</span></div><div class="card-row"><strong>Project package</strong><span class="mi">chevron_right</span></div><p>Create quote, payment, checklist, deliverables, and email.</p></button>
              <button class="card" data-view="quote" type="button" data-tip="A Quote is the price note your client can read."><div class="card-icon"><span class="mi">request_quote</span></div><div class="card-row"><strong>Quote</strong><span class="mi">chevron_right</span></div><p>Create a clear price message.</p></button>
              <button class="card" data-view="payment" type="button" data-tip="Split payment into now and later."><div class="card-icon"><span class="mi">payments</span></div><div class="card-row"><strong>Payment</strong><span class="mi">chevron_right</span></div><p>Calculate upfront and balance.</p></button>
              <button class="card" data-view="checklist" type="button" data-tip="A checklist is your project recipe."><div class="card-icon"><span class="mi">checklist</span></div><div class="card-row"><strong>Checklist</strong><span class="mi">chevron_right</span></div><p>Keep the job organized.</p></button>
            </div>
          </section>

          <section class="section">
            <div class="section-head"><div><h2>Business Setup</h2><p>Small settings that make the app feel like yours.</p></div></div>
            <div class="card-grid">
              <button class="card" data-view="settings" type="button"><div class="card-icon"><span class="mi">badge</span></div><strong>Brand profile</strong><p>Add your name, business, and contact details.</p></button>
              <button class="card" data-view="services" type="button"><div class="card-icon"><span class="mi">design_services</span></div><strong>Services</strong><p>Save your regular offers for faster quotes.</p></button>
              <button class="card" id="openInspector" type="button"><div class="card-icon"><span class="mi">preview</span></div><strong>Client-ready preview</strong><p>See what your client document looks like.</p></button>
            </div>
          </section>
          <div id="feedbackHost"></div>
        </section>

        <section id="learn" class="view">
          <div class="page-head"><div><p class="eyebrow">Learn Center</p><h1>Learn Creative Studio MCP</h1><p>Short lessons in plain English. No technical language needed.</p></div><button class="btn primary" id="continueLearning" type="button"><span class="mi">play_arrow</span>Continue learning</button></div>
          <div class="learning-card panel" style="max-width:100%; margin-bottom:24px;">
            <h3>Your progress</h3>
            <p id="learnProgressText">0% complete</p>
            <div class="progress-wrap"><div class="progress-bar" id="learnProgress"></div></div>
          </div>
          <div id="lessonList" class="lesson-list"></div>
          <section class="section faq"><div class="section-head"><div><h2>FAQ</h2><p>Quick answers without leaving the app.</p></div></div><div id="faqList" class="faq-list"></div></section>
        </section>

        <section id="project" class="view">
          <div class="page-head"><div><p class="eyebrow">New Project</p><h1>Create client package</h1><p>A Project is like a folder for one client job.</p></div></div>
          <div class="panel">
            <form id="projectForm">
              <div class="form-grid">
                <label>Client name<input name="client_name" value="New Client" required data-tip="Who is this job for?"></label>
                <label>Service<select name="service" id="projectService" data-tip="Choose a saved service, or choose Other to type a quick new one."></select><input class="other-field" name="service_other" id="projectServiceOther" placeholder="Type new service, then create package"><button class="btn danger remove-selected" type="button" data-remove-selected="service"><span class="mi">delete</span>Remove selected</button><small>Choose a saved service or add one quickly.</small></label>
                <label>Design fee<input name="design_fee" type="number" min="1" value="3000" required data-tip="Use numbers only, like 3000."></label>
                <label>Upfront %<input name="upfront_percent" type="number" min="0" max="100" value="70" required data-tip="This is what the client pays before work starts."></label>
                <label>Project type<select name="project_type" id="projectTypeSelect" required data-tip="Pick the kind of job, or choose Other for a quick custom type."></select><input class="other-field" name="project_type_other" id="projectTypeOther" placeholder="Type new project type, then create package"><button class="btn danger remove-selected" type="button" data-remove-selected="project_type"><span class="mi">delete</span>Remove selected</button><small>Used for the checklist.</small></label>
                <label>Deadline<input name="deadline" disabled placeholder="Future feature"><small>Coming later.</small></label>
              </div>
              <div class="actions"><button class="btn primary" id="projectGenerate" type="submit"><span class="mi">auto_awesome</span>Create client package</button><button class="btn secondary" data-clear type="button">Clear</button></div>
            </form>
            <div id="projectStatus"></div>
          </div>
        </section>

        <section id="quote" class="view">
          <div class="page-head"><div><p class="eyebrow">Quick tool</p><h1>Quote</h1><p>A Quote is like a price note you send before work begins.</p></div></div>
          <div class="panel"><form id="quoteForm"><div class="form-grid"><label>Client name<input name="client_name" value="New Client" required></label><label>Service<select name="service" id="quoteService" data-tip="Choose a saved service, or choose Other to type a quick new one."></select><input class="other-field" name="service_other" id="quoteServiceOther" placeholder="Type new service, then create quote"><button class="btn danger remove-selected" type="button" data-remove-selected="service"><span class="mi">delete</span>Remove selected</button></label><label>Design fee<input name="design_fee" type="number" min="1" value="3000" required></label><label>Project type<select name="project_type" id="quoteProjectType" data-tip="Pick the kind of job for this quote."></select><input class="other-field" name="project_type_other" id="quoteProjectTypeOther" placeholder="Type new project type, then create quote"><button class="btn danger remove-selected" type="button" data-remove-selected="project_type"><span class="mi">delete</span>Remove selected</button></label></div><div class="actions"><button class="btn primary" id="quoteGenerate" type="submit"><span class="mi">request_quote</span>Create quote</button></div></form><div id="quoteStatus"></div></div>
        </section>

        <section id="payment" class="view">
          <div class="page-head"><div><p class="eyebrow">Quick tool</p><h1>Payment</h1><p>Payment Breakdown shows what the client pays now and what they pay later.</p></div></div>
          <div class="panel"><form id="paymentForm"><div class="form-grid"><label>Total fee<input name="total_fee" type="number" min="1" value="5000" required></label><label>Upfront %<input name="upfront_percent" type="number" min="0" max="100" value="70" required></label></div><div class="actions"><button class="btn primary" id="paymentGenerate" type="submit"><span class="mi">calculate</span>Calculate</button></div></form><div id="paymentStatus"></div></div>
        </section>

        <section id="checklist" class="view">
          <div class="page-head"><div><p class="eyebrow">Quick tool</p><h1>Checklist</h1><p>Checklist is your project recipe.</p></div></div>
          <div class="panel"><form id="checklistForm"><label>Project type<select name="project_type" id="checklistProjectType" required data-tip="Pick the kind of job, or choose Other for a quick custom type."></select><input class="other-field" name="project_type_other" id="checklistProjectTypeOther" placeholder="Type new project type, then create checklist"><button class="btn danger remove-selected" type="button" data-remove-selected="project_type"><span class="mi">delete</span>Remove selected</button></label><div class="actions"><button class="btn primary" id="checklistGenerate" type="submit"><span class="mi">checklist</span>Create checklist</button></div></form><div id="checklistStatus"></div></div>
        </section>

        <section id="services" class="view">
          <div class="page-head"><div><p class="eyebrow">Services</p><h1>Service library</h1><p>Services are your usual offers, saved so quotes are faster.</p></div></div>
          <div class="panel"><div class="actions"><button class="btn primary" id="showServices" type="button"><span class="mi">design_services</span>Show services</button><button class="btn secondary" data-view="settings" type="button"><span class="mi">edit</span>Edit in Settings</button></div><div class="custom-manager"><div><h3>Quick additions</h3><p>Items you added with Other appear here. Remove anything you no longer need.</p></div><div class="form-grid"><div><h3>Custom services</h3><div id="customServicesList" class="custom-list"></div></div><div><h3>Custom project types</h3><div id="customProjectTypesList" class="custom-list"></div></div></div></div></div>
        </section>

        <section id="clients" class="view">
          <div class="page-head"><div><p class="eyebrow">Clients</p><h1>Clients</h1><p>Client database is planned. Recent project clients appear in Recent Projects for now.</p></div></div>
          <div class="empty"><div><span class="mi">groups</span><h3>Client database coming soon</h3><p>For now, create a project to save client details locally.</p></div></div>
        </section>

        <section id="settings" class="view">
          <div class="page-head"><div><p class="eyebrow">Business</p><h1>Settings</h1><p>Personalize your business profile, theme, services, and 7-day memory.</p></div></div>
          <div class="panel">
            <form id="settingsForm">
              <div class="form-grid">
                <label>Your name<input name="owner_name" autocomplete="name" placeholder="Your name"></label>
                <label>Business name<input name="business_name" placeholder="Business name"></label>
                <label>Email<input name="email" placeholder="name@example.com"></label>
                <label>Phone<input name="phone" placeholder="Phone"></label>
                <label>Website<input name="website" placeholder="Website"></label>
                <label>Currency<input name="currency" value="USD"></label>
              </div>
              <label>Payment terms<textarea name="payment_terms"></textarea></label>
              <label>Services<textarea name="services_text"></textarea><small>One per line: Service | Price range</small></label>
              <div class="actions"><button class="btn primary" type="submit"><span class="mi">save</span>Save Settings</button></div>
            </form>
          </div>
          <section class="section">
            <div class="panel">
              <h2>Memory</h2>
              <p>Memory helps Creative Studio remember where you left off, like a desk that keeps your papers in place for a few days.</p>
              <div class="actions"><button class="btn secondary" id="toggleMemory" type="button"></button><button class="btn danger" id="clearMemory" type="button">Clear 7-day memory</button></div>
              <div class="notice"><strong>What we remember</strong><p>Last active project, last service, preferred upfront percent, last export format, learning progress, theme color, dismissed tooltips, and feedback prompts shown.</p><strong>What we avoid</strong><p>We do not save every keystroke, failed forms, empty forms, or private notes unless you save a project.</p><strong>Future Pro idea</strong><p>Longer memory, client history, templates, brand tone, analytics, and cloud sync can be tested later.</p></div>
            </div>
          </section>
          <section class="section faq"><div class="section-head"><div><h2>FAQ</h2><p>Simple answers about data, exports, and memory.</p></div></div><div id="settingsFaqList" class="faq-list"></div></section>
        </section>
      </div>
    </main>

    <aside class="inspector" id="inspector" aria-label="Contextual inspector">
      <div class="inspector-inner">
        <button class="inspector-handle" id="handleInspector" type="button" aria-label="Toggle inspector width"><span class="mi">drag_indicator</span></button>
        <div>
          <div class="inspector-head">
            <div class="inspector-title"><h2>Client-ready preview</h2><p id="inspectorHint">Latest result appears here.</p></div>
            <div class="inspector-actions">
              <button class="btn icon ghost" id="collapseInspector" type="button" aria-label="Collapse preview" data-tip="Minimize the preview panel."><span class="mi">right_panel_close</span></button>
              <button class="btn icon ghost" id="expandInspector" type="button" aria-label="Expand preview" data-tip="Make the preview wider."><span class="mi">open_in_full</span></button>
              <button class="btn icon ghost" id="closeInspector" type="button" aria-label="Close preview"><span class="mi">close</span></button>
            </div>
          </div>
          <div class="inspector-toolbar">
            <button class="btn secondary" id="copyInspector" type="button" data-tip="Copy everything in the preview."><span class="mi">content_copy</span>Copy</button>
            <button class="btn secondary" id="exportTxt" type="button" data-tip="Download a plain text version."><span class="mi">article</span>TXT</button>
            <button class="btn secondary" id="exportMd" type="button" data-tip="Download a Markdown version."><span class="mi">description</span>Markdown</button>
            <button class="btn secondary" id="exportPdf" type="button" data-tip="Download a PDF version."><span class="mi">picture_as_pdf</span>PDF</button>
          </div>
          <div id="inspectorBody" class="inspector-body"><div class="empty"><div><span class="mi">preview</span><h3>No preview yet</h3><p>Run a tool to see the latest result.</p></div></div></div>
        </div>
      </div>
    </aside>
    <aside class="inspector-rail" id="inspectorRail" aria-label="Inspector collapsed"><button class="btn icon primary" id="restoreInspector" type="button" aria-label="Open preview"><span class="mi">dock_to_right</span></button></aside>
  </div>

  <div class="mobile-accent-dots" id="mobileThemeDots" aria-label="Accent theme"></div>
  <nav class="bottom-nav" aria-label="Mobile navigation">
    <button class="active" data-view="dashboard"><span class="mi">dashboard</span></button>
    <button data-view="project"><span class="mi">folder_open</span></button>
    <button data-view="learn"><span class="mi">school</span></button>
    <button data-view="quote"><span class="mi">request_quote</span></button>
    <button data-view="settings"><span class="mi">settings</span></button>
  </nav>
  <div class="tooltip" id="tooltip" role="tooltip"></div>
  <div class="toast" id="toast" role="status" aria-live="polite"></div>
  <button class="btn primary help-fab" id="walkthroughHelp" type="button" data-tip="Open simple tips for where you are now."><span class="mi">help</span><span class="help-text">Need help?</span></button>
  <div class="modal-backdrop" id="nameOnboardingModal" aria-hidden="true"><div class="modal" role="dialog" aria-modal="true" aria-labelledby="nameOnboardingTitle"><p class="eyebrow">First setup</p><h2 id="nameOnboardingTitle">Welcome to Creative Studio</h2><p>Add your name so the dashboard can greet you properly. You can skip this and keep the greeting neutral.</p><label>Your name<input id="onboardingName" autocomplete="name" placeholder="Your name"></label><div class="actions" style="margin-top:16px;"><button class="btn primary" id="saveOnboardingName" type="button"><span class="mi">check</span>Save name</button><button class="btn secondary" id="skipOnboardingName" type="button">Skip for now</button></div></div></div>
  <div class="modal-backdrop" id="walkthroughModal" aria-hidden="true"><div class="modal" role="dialog" aria-modal="true" aria-labelledby="walkthroughTitle"><p class="eyebrow">Walkthrough</p><h2 id="walkthroughTitle">Feeling lost?</h2><p id="walkthroughIntro">Here is the easiest next move.</p><div id="walkthroughSteps" class="walkthrough-list"></div><div class="actions" style="margin-top:16px;"><button class="btn primary" id="walkthroughPrimary" type="button"><span class="mi">play_arrow</span>Guide me</button><button class="btn secondary" id="walkthroughLearn" type="button"><span class="mi">school</span>Open Learn</button><button class="btn ghost" id="closeWalkthrough" type="button">Close</button></div></div></div>
  <div class="modal-backdrop" id="feedbackModal" aria-hidden="true"><div class="modal" role="dialog" aria-modal="true" aria-labelledby="feedbackTitle"><h2 id="feedbackTitle">Share feedback</h2><p>What felt useful, confusing, or missing?</p><textarea id="feedbackText" placeholder="Optional comment"></textarea><div class="actions" style="margin-top:16px;"><button class="btn primary" id="saveFeedback" type="button">Save feedback</button><button class="btn secondary" id="closeFeedback" type="button">Close</button></div></div></div>

  <script>
    const $ = (selector) => document.querySelector(selector);
    const $$ = (selector) => Array.from(document.querySelectorAll(selector));
    const MEMORY_KEY = "creativeStudioMemory";
    const CUSTOM_SERVICES_KEY = "creativeStudioCustomServices";
    const CUSTOM_PROJECT_TYPES_KEY = "creativeStudioCustomProjectTypes";
    const MEMORY_DAYS = 7;
    let lastProject = null;
    let lastPreviewText = "";
    let lastPreviewSections = [];
    let lastRecent = [];
    let currentServiceNames = [];
    let formEditTimers = {};

    const lessons = [
      ["started", "Getting Started", "Think of Creative Studio MCP like a tidy desk for client work. It keeps your quote, payment, checklist, and email in one place.", "dashboard"],
      ["first_project", "Creating Your First Project", "A Project is like a folder for one client job. Put the client name, service, fee, and payment terms inside.", "project"],
      ["quote", "Sending a Quote", "A Quote is like a price note you send before work begins. It tells the client what the work costs.", "quote"],
      ["payment", "Understanding Payments", "Payment Breakdown shows what the client pays now and what they pay later.", "payment"],
      ["checklist", "Using Checklists", "Checklist is your project recipe. It helps you follow the same steps every time.", "checklist"],
      ["services", "Managing Services", "Services are your common offers. Save them once so future quotes are faster.", "services"],
      ["export", "Exporting TXT and MD", "Export is like putting your work into a file you can send, save, or reuse.", "project"],
      ["continue", "Saving and Continuing Work", "Continue Recent brings you back to the last project, like reopening the folder you were using.", "dashboard"],
      ["faq", "FAQ", "Quick answers for common questions, all inside the app.", "learn"],
    ];
    const defaultProjectTypes = [
      "Brand Identity Design",
      "Product Packaging Design",
      "Corporate Profile Design",
      "Proposal / Presentation Design",
      "Merchandise Design",
      "Banner & Event Visual Design",
      "Social Media Design",
      "Website Design",
      "Logo Design",
      "Other"
    ];
    const faqs = [
      ["What is Creative Studio MCP?", "It is a local workspace that helps creative businesses prepare quotes, payments, checklists, deliverables, and client emails."],
      ["What is a project?", "A project is one client job, like a folder that keeps all the important pieces together."],
      ["What is a quote?", "A quote is a clear price note for your client before work begins."],
      ["What is a service?", "A service is something you sell, such as Brand Identity Design or Product Packaging Design."],
      ["What does payment breakdown mean?", "It shows what the client pays now and what they pay later."],
      ["What is the preview panel?", "It shows what your client-ready document looks like before you copy or export it."],
      ["Where is my data saved?", "Projects and settings are saved locally on this computer."],
      ["What does 7-day memory mean?", "The app can remember helpful workflow details for 7 days, then they expire automatically."],
      ["Can I clear my memory?", "Yes. Go to Settings, then use Clear 7-day memory."],
      ["Can I export my work?", "Yes. You can export project packages as TXT or Markdown."],
      ["What is Markdown?", "Markdown is a clean text format that works well for docs, GitHub, and notes apps."],
      ["Why should I save services?", "Saved services make quotes faster and help keep pricing consistent."],
    ];
    const walkthroughTips = {
      dashboard: {
        intro: "Start here if you are unsure what to do next.",
        view: "project",
        steps: [
          ["Start a project", "Use New Project when you want the app to prepare the full client package."],
          ["Check recent work", "Recent Projects is like your desk. It shows the jobs you saved on this computer."],
          ["Use Learn", "Learn explains the app in simple words if any tool feels unclear."]
        ]
      },
      project: {
        intro: "A project is one client job. Fill the form, then generate.",
        view: "project",
        steps: [
          ["Add client details", "Type the client name, choose a service, and enter the fee."],
          ["Generate once", "Create client package builds the quote, payment, checklist, deliverables, and email together."],
          ["Use the preview", "The right panel shows the client-ready result. Copy or export from there."]
        ]
      },
      quote: {
        intro: "Use Quote when you only need the client price message.",
        view: "quote",
        steps: [
          ["Pick a service", "Choose a saved service or Other if you need a new one quickly."],
          ["Enter the fee", "Use numbers only, such as 3000."],
          ["Create quote", "The result appears in the preview panel for copying."]
        ]
      },
      payment: {
        intro: "Payment shows what the client pays now and later.",
        view: "payment",
        steps: [
          ["Add total fee", "Type the full project amount."],
          ["Set upfront percent", "70 means the client pays 70 percent before work starts."],
          ["Calculate", "The preview shows upfront payment and balance payment."]
        ]
      },
      checklist: {
        intro: "Checklist is your project recipe.",
        view: "checklist",
        steps: [
          ["Choose project type", "Pick the kind of job you are doing."],
          ["Use Other for new work", "If your job type is missing, choose Other and type it."],
          ["Create checklist", "The preview gives you tickable steps you can follow."]
        ]
      },
      services: {
        intro: "Services are the things your business sells.",
        view: "services",
        steps: [
          ["Show services", "View your saved service list."],
          ["Add with Other", "Use Other inside Quote or Project to quickly add a new service."],
          ["Remove mistakes", "User-added options can be removed without opening Settings."]
        ]
      },
      settings: {
        intro: "Settings makes the app feel like your business.",
        view: "settings",
        steps: [
          ["Add your name", "This controls the dashboard greeting and client-ready signature."],
          ["Add business details", "Business name, email, phone, and website can appear in client messages."],
          ["Save settings", "Your details stay on this computer."]
        ]
      },
      learn: {
        intro: "Learn is the simple guide inside the app.",
        view: "learn",
        steps: [
          ["Read one lesson", "Each card explains one part of the app."],
          ["Try it", "Use the Try it button to jump straight to that tool."],
          ["Mark done", "Mark lessons as done so you know what you already understand."]
        ]
      }
    };
    function activeViewId() {
      return document.querySelector(".view.active")?.id || "dashboard";
    }
    function currentWalkthrough() {
      return walkthroughTips[activeViewId()] || walkthroughTips.dashboard;
    }
    function openWalkthrough() {
      const tip = currentWalkthrough();
      const modal = $("#walkthroughModal");
      $("#walkthroughIntro").textContent = tip.intro;
      $("#walkthroughSteps").innerHTML = tip.steps.map(([title, body], index) => `<article class="walkthrough-step"><strong><span class="step-number" aria-hidden="true">${index + 1}</span>${escapeHtml(title)}</strong><p>${escapeHtml(body)}</p></article>`).join("");
      modal.classList.add("show");
      modal.setAttribute("aria-hidden", "false");
      saveMemory("walkthroughOpenedAt", now(), { source: "walkthrough" });
    }
    function closeWalkthrough() {
      const modal = $("#walkthroughModal");
      if (!modal) return;
      modal.classList.remove("show");
      modal.setAttribute("aria-hidden", "true");
    }
    function guideFromWalkthrough() {
      const tip = currentWalkthrough();
      closeWalkthrough();
      setView(tip.view || "project");
      toast("Follow the highlighted section. You can reopen Need help anytime.");
    }
    function now() { return Date.now(); }
    function expiry() { return now() + MEMORY_DAYS * 24 * 60 * 60 * 1000; }
    function readStore() {
      try { return JSON.parse(localStorage.getItem(MEMORY_KEY) || "{}"); } catch { return {}; }
    }
    function writeStore(store) { localStorage.setItem(MEMORY_KEY, JSON.stringify(store)); }
    function pruneExpiredMemory() {
      const store = readStore();
      let changed = false;
      Object.keys(store).forEach(key => {
        if (store[key]?.expiresAt && store[key].expiresAt < now()) { delete store[key]; changed = true; }
      });
      if (changed) writeStore(store);
      return store;
    }
    function memoryOn() { return getMemory("memoryStatus") !== "off"; }
    function saveMemory(key, value, options = {}) {
      if (key !== "memoryStatus" && !memoryOn()) return;
      if (options.requireMeaningful && !shouldSaveMemory(options.activity)) return;
      const store = pruneExpiredMemory();
      store[key] = { key, value, createdAt: now(), expiresAt: expiry(), source: options.source || "local-app", sensitivity: options.sensitivity || "workflow", version: 1 };
      writeStore(store);
    }
    function getMemory(key) {
      const item = pruneExpiredMemory()[key];
      return item ? item.value : null;
    }
    function clearMemory() { localStorage.removeItem(MEMORY_KEY); toast("7-day memory cleared."); renderMemorySettings(); renderLearn(); }
    function shouldSaveMemory(activity) {
      return ["project_generated", "quote_generated", "export_clicked", "form_edit_10s", "return_project"].includes(activity);
    }

    function toast(message) {
      const box = $("#toast");
      box.textContent = message;
      box.classList.add("show");
      clearTimeout(window.toastTimer);
      window.toastTimer = setTimeout(() => box.classList.remove("show"), 2200);
    }
    function escapeHtml(value) {
      return String(value ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
    }
    function toText(value) {
      if (typeof value === "string") return value;
      if (Array.isArray(value)) return value.map((item, index) => `${index + 1}. ${item}`).join("\\n");
      if (value && typeof value === "object") return Object.entries(value).map(([key, item]) => `${key}: ${item}`).join("\\n");
      return String(value ?? "");
    }
    async function api(path, payload = {}) {
      const response = await fetch(path, { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(payload) });
      const data = await response.json();
      if (!response.ok || data.error) throw new Error(data.error || "Request failed.");
      return data.result;
    }
    function setView(id) {
      $$(".view").forEach(view => view.classList.toggle("active", view.id === id));
      $$("[data-view]").forEach(button => button.classList.toggle("active", button.dataset.view === id));
      saveMemory("lastActiveView", id, { activity: "return_project", requireMeaningful: id !== "dashboard" });
      if (id === "dashboard") loadRecent();
      if (id === "learn") renderLearn();
    }
    function setLoading(button, loading) {
      if (!button) return;
      if (loading) {
        if (!button.dataset.originalHtml) button.dataset.originalHtml = button.innerHTML;
        button.disabled = true;
        button.setAttribute("aria-busy", "true");
        button.classList.add("loading");
        button.innerHTML = `<span class="btn-loader" aria-label="Working"><span class="loader-logo"><img src="/assets/logo-transparent.png" alt=""><span class="loader-letter c">C</span><span class="loader-letter s">S</span></span><span class="loader-heartline" aria-hidden="true"></span></span>`;
        return;
      }
      button.disabled = false;
      button.removeAttribute("aria-busy");
      button.classList.remove("loading");
      if (button.dataset.originalHtml) {
        button.innerHTML = button.dataset.originalHtml;
        delete button.dataset.originalHtml;
      }
    }
    function shellState(state) {
      const shell = $("#shell");
      shell.classList.remove("inspector-wide", "inspector-collapsed", "inspector-closed");
      if (state === "wide") shell.classList.add("inspector-wide");
      if (state === "collapsed") shell.classList.add("inspector-collapsed");
      if (state === "closed") shell.classList.add("inspector-closed");
      saveMemory("inspectorState", state, { activity: "return_project", requireMeaningful: true });
    }
    function openInspector() {
      $("#shell").classList.remove("inspector-collapsed", "inspector-closed");
    }
    function sectionHtml(title, value) {
      const text = toText(value);
      if (Array.isArray(value)) {
        const isChecklist = String(title || "").toLowerCase().includes("check");
        const rows = value.map((item, index) => isChecklist
          ? `<label class="check-row" data-check-index="${index}"><input type="checkbox" aria-label="Checklist item ${index + 1}"><span>${escapeHtml(item)}</span><button class="btn ghost mini-action" data-select-check-item="${index}" type="button">Select</button><button class="btn danger mini-action" data-remove-check-item="${index}" type="button"><span class="mi">delete</span>Remove</button></label>`
          : `<li class="bullet-row">${escapeHtml(item)}</li>`).join("");
        const body = isChecklist ? `<div class="check-actions"><button class="btn secondary" data-remove-checked-checklist type="button"><span class="mi">checklist_rtl</span>Remove checked</button><button class="btn secondary" data-export-selected-checklist="txt" type="button"><span class="mi">download</span>Export selected TXT</button><button class="btn secondary" data-export-selected-checklist="md" type="button"><span class="mi">description</span>Export selected Markdown</button></div><div class="check-list">${rows}</div>` : `<ul class="bullet-list">${rows}</ul>`;
        return `<details class="preview-section" open><summary><span>${escapeHtml(title)}</span><button class="btn ghost" data-copy="${encodeURIComponent(text)}" type="button"><span class="mi">content_copy</span>Copy</button></summary><div class="preview-doc">${body}</div></details>`;
      }
      if (value && typeof value === "object") {
        return `<details class="preview-section" open><summary><span>${escapeHtml(title)}</span><button class="btn ghost" data-copy="${encodeURIComponent(text)}" type="button"><span class="mi">content_copy</span>Copy</button></summary><div class="preview-doc kv">${Object.entries(value).map(([key, item]) => `<div class="kv-row"><span class="token">${escapeHtml(key)}</span><strong>${escapeHtml(item)}</strong></div>`).join("")}</div></details>`;
      }
      return `<details class="preview-section" open><summary><span>${escapeHtml(title)}</span><button class="btn ghost" data-copy="${encodeURIComponent(text)}" type="button"><span class="mi">content_copy</span>Copy</button></summary><div class="preview-doc"><div class="doc-text">${escapeHtml(text)}</div></div></details>`;
    }
    function preview(title, sections, project = null) {
      openInspector();
      lastProject = project;
      const list = Array.isArray(sections) ? sections : [{ title, value: sections }];
      lastPreviewSections = list.map(item => ({ title: item.title, value: Array.isArray(item.value) ? [...item.value] : item.value }));
      lastPreviewText = lastPreviewSections.map(item => `${item.title.toUpperCase()}\n${toText(item.value)}`).join("\n\n");
      $("#inspectorHint").textContent = title;
      $("#inspectorBody").innerHTML = lastPreviewSections.map(item => sectionHtml(item.title, item.value)).join("");
      saveMemory("lastPreview", { title, sections: lastPreviewSections, projectId: project?.id || null }, { activity: "return_project", requireMeaningful: true });
    }
    function checklistSection() {
      return lastPreviewSections.find(item => String(item.title || "").toLowerCase().includes("check") && Array.isArray(item.value));
    }
    function selectedChecklistIndexes() {
      return $$("#inspectorBody .check-row input[type='checkbox']:checked").map(input => Number(input.closest(".check-row")?.dataset.checkIndex)).filter(Number.isInteger);
    }
    function refreshPreviewFromState(message) {
      const title = $("#inspectorHint")?.textContent || "Updated preview";
      const project = lastProject;
      preview(title, lastPreviewSections, project);
      if (message) toast(message);
    }
    function removeChecklistIndexes(indexes) {
      const section = checklistSection();
      if (!section) { toast("Create a checklist first."); return; }
      const removeSet = new Set(indexes);
      if (!removeSet.size) { toast("Tick a checklist item first."); return; }
      section.value = section.value.filter((_, index) => !removeSet.has(index));
      if (lastProject?.generated_package?.project_checklist) lastProject.generated_package.project_checklist = section.value;
      refreshPreviewFromState(removeSet.size === 1 ? "Checklist item removed." : "Checked checklist items removed.");
    }
    function downloadTextFile(filename, text) {
      const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 800);
    }
    function exportSelectedChecklist(format = "txt") {
      const section = checklistSection();
      if (!section) { toast("Create a checklist first."); return; }
      const indexes = selectedChecklistIndexes();
      if (!indexes.length) { toast("Select at least one checklist item before exporting."); return; }
      const items = indexes.map(index => section.value[index]).filter(Boolean);
      const title = `${section.title || "Checklist"}`;
      const content = format === "md" ? [`# ${title}`, "", ...items.map(item => `- ${item}`)].join("\n") : [`${title}`, "", ...items.map(item => `- ${item}`)].join("\n");
      downloadTextFile(`selected-checklist.${format === "md" ? "md" : "txt"}`, content);
      toast(format === "md" ? "Selected checklist saved as Markdown." : "Selected checklist saved as a text file.");
    }
    function notice(target, message, type = "") {
      if (!target) return;
      target.innerHTML = `<div class="notice ${type}">${escapeHtml(message)}</div>`;
    }
    function readList(key) {
      try {
        const value = JSON.parse(localStorage.getItem(key) || "[]");
        return Array.isArray(value) ? value : [];
      } catch {
        return [];
      }
    }
    function saveListItem(key, value) {
      const cleaned = String(value || "").trim();
      if (!cleaned) return;
      const list = readList(key).filter(item => item.toLowerCase() !== cleaned.toLowerCase());
      list.unshift(cleaned);
      localStorage.setItem(key, JSON.stringify(list.slice(0, 20)));
      renderCustomAdditions();
      updateRemoveSelected();
    }
    function removeLocalListItem(key, value) {
      const cleaned = String(value || "").trim().toLowerCase();
      const before = readList(key);
      const list = before.filter(item => item.toLowerCase() !== cleaned);
      localStorage.setItem(key, JSON.stringify(list));
      return before.length !== list.length;
    }
    async function removeListItem(key, value) {
      const original = String(value || "").trim();
      const cleaned = original.toLowerCase();
      if (!cleaned) return;
      let removed = removeLocalListItem(key, original);
      if (key === CUSTOM_SERVICES_KEY) {
        try {
          const result = await api("/api/remove-service", { service: original });
          removed = removed || Boolean(result.removed);
          if (result.profile) syncSettingsProfile(result.profile);
        } catch (error) {
          toast(error.message);
        }
      }
      document.querySelectorAll("select").forEach(select => {
        Array.from(select.options).forEach(option => {
          if (String(option.value || "").trim().toLowerCase() === cleaned) option.remove();
        });
        if (!select.options.length) select.innerHTML = `<option value="__other__">Other</option>`;
      });
      resetRemovedSelections(cleaned);
      try {
        await loadServices();
      } catch (error) {
        toast(error.message);
      }
      resetRemovedSelections(cleaned);
      renderCustomAdditions();
      updateRemoveSelected();
      toast(removed ? `Removed ${original}.` : "That option was already removed.");
    }
    function renderCustomList(target, key, emptyText) {
      const host = $(target);
      if (!host) return;
      const list = readList(key);
      host.innerHTML = list.length ? list.map(item => `<div class="custom-chip"><span>${escapeHtml(item)}</span><button class="btn danger" type="button" data-remove-custom="${key}" data-custom-value="${encodeURIComponent(item)}">Remove</button></div>`).join("") : `<div class="empty" style="min-height:90px;"><div><p>${escapeHtml(emptyText)}</p></div></div>`;
    }
    function renderCustomAdditions() {
      renderCustomList("#customServicesList", CUSTOM_SERVICES_KEY, "No custom services yet.");
      renderCustomList("#customProjectTypesList", CUSTOM_PROJECT_TYPES_KEY, "No custom project types yet.");
    }
    function normalizePayload(payload) {
      const cleaned = { ...payload };
      if (cleaned.service === "__other__") {
        cleaned.service = String(cleaned.service_other || "").trim();
        if (!cleaned.service) throw new Error("Type the new service name first.");
        saveListItem(CUSTOM_SERVICES_KEY, cleaned.service);
      }
      if (cleaned.project_type === "__other__") {
        cleaned.project_type = String(cleaned.project_type_other || "").trim();
        if (!cleaned.project_type) throw new Error("Type the new project type first.");
        saveListItem(CUSTOM_PROJECT_TYPES_KEY, cleaned.project_type);
      }
      delete cleaned.service_other;
      delete cleaned.project_type_other;
      return cleaned;
    }
    function parseForm(form) {
      if (!form || !form.elements) throw new Error("This form is not ready. Please refresh the app and try again.");
      return normalizePayload(Object.fromEntries(new FormData(form).entries()));
    }
    function setSelectOrOther(select, otherInput, value) {
      if (!select || value === undefined || value === null) return;
      const found = Array.from(select.options).some(option => option.value === String(value));
      select.value = found ? String(value) : "__other__";
      if (otherInput) {
        otherInput.value = found ? "" : String(value);
        otherInput.classList.toggle("show", !found);
        otherInput.required = !found;
      }
    }
    function fillForm(form, values = {}) {
      if (!form || !form.elements) return;
      const fields = form.elements;
      Object.entries(values || {}).forEach(([key, value]) => {
        if (key === "service" && fields.service) {
          setSelectOrOther(fields.service, fields.service_other, value);
        } else if (key === "project_type" && fields.project_type) {
          setSelectOrOther(fields.project_type, fields.project_type_other, value);
        } else if (fields[key] && value !== undefined && value !== null) {
          fields[key].value = value;
        }
      });
      syncOtherFields(form);
    }
    function savedDisplayName(profile) {
      const fullName = String(profile?.owner_name || "").trim();
      const legacyDefault = ["Tho", "mas", " Og", "un"].join("");
      if (!localStorage.getItem("creativeStudioNameOnboarded") && fullName === legacyDefault) return "";
      return fullName;
    }
    function greeting(profile) {
      const hour = new Date().getHours();
      const word = hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : hour < 21 ? "Good evening" : "Good night";
      const fullName = savedDisplayName(profile);
      const name = fullName.split(/\\s+/)[0];
      $("#greeting").textContent = name ? `${word}, ${name}` : `${word}. Welcome to Creative Studio`;
    }
    function optionList(values, includeOther = true) {
      const unique = Array.from(new Set(values.filter(Boolean).map(item => String(item).trim()).filter(Boolean)));
      const options = unique.map(name => `<option value="${escapeHtml(name)}">${escapeHtml(name)}</option>`).join("");
      return includeOther ? `${options}<option value="__other__">Other</option>` : options;
    }
    function loadProjectTypes() {
      const options = optionList([...readList(CUSTOM_PROJECT_TYPES_KEY), ...defaultProjectTypes.filter(item => item !== "Other")]);
      $("#projectTypeSelect").innerHTML = options;
      $("#checklistProjectType").innerHTML = options;
    }
    function isCustomValue(key, value) {
      const text = String(value || "").trim().toLowerCase();
      if (!text) return false;
      return readList(key).some(item => item.toLowerCase() === text);
    }
    function resetRemovedSelections(removedValue) {
      document.querySelectorAll("select").forEach(select => {
        if (String(select.value || "").trim().toLowerCase() === removedValue) {
          select.selectedIndex = 0;
        }
      });
      syncOtherFields();
    }
    function updateRemoveSelected(scope = document) {
      if (!scope || !scope.querySelectorAll) return;
      scope.querySelectorAll("[data-remove-selected]").forEach(button => {
        const fieldName = button.dataset.removeSelected;
        const form = button.closest("form") || document;
        const label = button.closest("label");
        const select = label?.querySelector("select") || form.querySelector(`select[name="${fieldName}"]`);
        const key = fieldName === "service" ? CUSTOM_SERVICES_KEY : CUSTOM_PROJECT_TYPES_KEY;
        const removable = select && select.value !== "__other__" && isCustomValue(key, select.value);
        button.classList.toggle("show", Boolean(removable));
        button.disabled = !removable;
      });
    }
    function syncOtherFields(scope = document) {
      if (!scope || !scope.querySelectorAll) return;
      scope.querySelectorAll("select").forEach(select => {
        const other = select.parentElement?.querySelector(".other-field");
        if (!other) return;
        const show = select.value === "__other__";
        other.classList.toggle("show", show);
        other.required = show;
      });
      updateRemoveSelected(scope);
    }
    async function loadServices() {
      const services = await api("/api/services");
      currentServiceNames = Object.keys(services);
      const options = optionList([...readList(CUSTOM_SERVICES_KEY), ...currentServiceNames]);
      $("#projectService").innerHTML = options;
      $("#quoteService").innerHTML = options;
      loadProjectTypes();
      syncOtherFields();
      renderCustomAdditions();
    }
    function syncSettingsProfile(profile) {
      const form = $("#settingsForm");
      if (!form || !form.elements) return;
      ["owner_name","business_name","email","phone","website","currency","payment_terms"].forEach(name => {
        if (form.elements[name]) form.elements[name].value = profile[name] || "";
      });
      if (form.elements.services_text) {
        form.elements.services_text.value = Object.entries(profile.services || {}).map(([name, price]) => `${name} | ${price}`).join("\\n");
      }
    }
    let currentProfile = {};
    function shouldShowNameOnboarding(profile) {
      return !localStorage.getItem("creativeStudioNameOnboarded") && !savedDisplayName(profile);
    }
    function showNameOnboarding(profile) {
      const modal = $("#nameOnboardingModal");
      const input = $("#onboardingName");
      if (!modal || !input || !shouldShowNameOnboarding(profile)) return;
      modal.classList.add("show");
      modal.setAttribute("aria-hidden", "false");
      setTimeout(() => input.focus(), 80);
    }
    function closeNameOnboarding() {
      const modal = $("#nameOnboardingModal");
      if (!modal) return;
      modal.classList.remove("show");
      modal.setAttribute("aria-hidden", "true");
    }
    async function loadProfile() {
      const profile = await api("/api/profile");
      currentProfile = profile || {};
      greeting(currentProfile);
      syncSettingsProfile(currentProfile);
      showNameOnboarding(currentProfile);
    }
    async function loadRecent() {
      lastRecent = await api("/api/recent", { limit: 5 });
      $("#continueRecent").disabled = !lastRecent.length && !getMemory("lastActiveProjectId");
      $("#recent").innerHTML = lastRecent.length ? lastRecent.map(project => `<div class="recent-item"><div><strong>${escapeHtml(project.client_name)}</strong><p>${escapeHtml(project.service)} at ${Number(project.design_fee).toLocaleString()}</p></div><button class="btn secondary" data-open-project="${project.id}" type="button"><span class="mi">visibility</span>Preview</button></div>`).join("") : `<div class="empty"><div><span class="mi">folder_open</span><h3>No projects yet.</h3><p>Create your first client package and it will appear here.</p><div class="actions" style="justify-content:center;"><button class="btn primary" data-view="project" type="button"><span class="mi">add</span>Create your first project</button><button class="btn ghost" data-view="learn" type="button">Learn how projects work</button></div></div></div>`;
    }
    function renderProject(project, label = "Project package") {
      const pkg = project.generated_package || {};
      fillForm($("#projectForm"), project);
      saveMemory("lastActiveProjectId", project.id, { activity: "return_project", requireMeaningful: true });
      saveMemory("lastUsedService", project.service, { activity: "return_project", requireMeaningful: true });
      saveMemory("preferredUpfrontPercent", project.upfront_percent, { activity: "return_project", requireMeaningful: true });
      preview(label, [
        { title: "Quote", value: pkg.client_quote },
        { title: "Payment", value: pkg.payment_breakdown },
        { title: "Checklist", value: pkg.project_checklist },
        { title: "Deliverables", value: pkg.deliverables },
        { title: "Email", value: pkg.client_email }
      ], project);
    }

    function renderFAQ(targetId) {
      const host = $(targetId);
      host.innerHTML = faqs.map(([q, a], index) => `<details><summary aria-expanded="false">${escapeHtml(q)}</summary><p>${escapeHtml(a)}</p></details>`).join("");
    }
    function renderLearn() {
      const progress = getMemory("learnProgress") || {};
      const done = lessons.filter(([id]) => progress[id]).length;
      const percent = Math.round(done / lessons.length * 100);
      $("#learnProgress").style.width = `${percent}%`;
      $("#learnProgressText").textContent = `${percent}% complete`;
      $("#lessonList").innerHTML = lessons.map(([id, title, text, view]) => `<article class="lesson-card ${progress[id] ? "complete" : ""}"><div><strong style="display:inline-flex;align-items:center;gap:8px;">${progress[id] ? `<span class="mi" aria-hidden="true">check_circle</span>` : `<span class="mi" aria-hidden="true">radio_button_unchecked</span>`}${escapeHtml(title)}</strong><p>${escapeHtml(text)}</p></div><div class="actions"><button class="btn secondary" data-lesson="${id}" data-view="${view}" type="button">Try it</button><button class="btn ghost" data-complete-lesson="${id}" type="button">${progress[id] ? "Done" : "Mark done"}</button></div></article>`).join("");
    }
    function completeLesson(id) {
      const progress = getMemory("learnProgress") || {};
      progress[id] = true;
      saveMemory("learnProgress", progress, { source: "learn-center" });
      renderLearn();
      renderCustomAdditions();
      toast("Lesson saved.");
    }
    function safeCompleteLesson(id) {
      try {
        completeLesson(id);
      } catch (error) {
        console.warn("Lesson progress could not update", error);
      }
    }
    function continueLearning() {
      const progress = getMemory("learnProgress") || {};
      const next = lessons.find(([id]) => !progress[id]) || lessons[0];
      setView("learn");
      setTimeout(() => document.querySelector(`[data-lesson="${next[0]}"]`)?.focus(), 50);
      toast("Continue learning.");
    }
    function renderThemeDots() {
      const selected = getMemory("accentTheme") || "purple";
      const dots = [["purple", "Default"], ["red", "Warm"], ["green", "Growth"], ["blue", "Calm"]];
      const html = dots.map(([key, label]) => `<button class="dot ${key === "purple" ? "" : key} ${selected === key ? "active" : ""}" data-accent-dot="${key}" aria-label="${label} accent theme" data-tip="Accent theme: ${label}"><span style="${key === "purple" ? "background:#8b5cf6" : ""}"></span></button>`).join("");
      const sidebarDots = $("#themeDots");
      const mobileDots = $("#mobileThemeDots");
      if (sidebarDots) sidebarDots.innerHTML = html;
      if (mobileDots) mobileDots.innerHTML = html;
    }
    function setAccent(key) {
      document.documentElement.dataset.accent = key === "purple" ? "" : key;
      saveMemory("accentTheme", key, { source: "theme" });
      renderThemeDots();
      toast(`${key === "purple" ? "Default" : key} accent selected.`);
    }
    function renderMemorySettings() {
      const status = memoryOn();
      $("#toggleMemory").textContent = status ? "Turn memory off" : "Turn memory on";
      $("#toggleMemory").className = status ? "btn secondary" : "btn primary";
    }
    function shouldShowFeedback() {
      const last = getMemory("feedbackPromptShownAt");
      if (last && now() - Number(last) < 24 * 60 * 60 * 1000) return false;
      return Boolean(getMemory("lastActiveProjectId"));
    }
    function renderFeedbackPrompt() {
      if (!shouldShowFeedback()) return;
      $("#feedbackHost").innerHTML = `<div class="feedback-card"><h3>Was this useful?</h3><p>Your beta feedback helps shape the next version.</p><div class="actions"><button class="btn secondary" data-feedback="yes">Yes</button><button class="btn secondary" data-feedback="not-yet">Not yet</button><button class="btn secondary" data-feedback="confusing">Confusing</button><button class="btn primary" data-feedback="comment">I have feedback</button></div></div>`;
      saveMemory("feedbackPromptShownAt", now(), { source: "feedback" });
    }
    function setupTooltips() {
      const tip = $("#tooltip");
      function show(el) {
        const text = el.getAttribute("data-tip");
        if (!text) return;
        tip.innerHTML = `<span>${escapeHtml(text)}</span><button type="button" aria-label="Dismiss tooltip">x</button>`;
        const rect = el.getBoundingClientRect();
        tip.style.left = `${Math.min(rect.left, window.innerWidth - 300)}px`;
        tip.style.top = `${rect.bottom + 10}px`;
        tip.classList.add("show");
      }
      function hide() { tip.classList.remove("show"); }
      document.addEventListener("mouseover", event => { const el = event.target.closest("[data-tip]"); if (el) show(el); });
      document.addEventListener("focusin", event => { const el = event.target.closest("[data-tip]"); if (el) show(el); });
      document.addEventListener("mouseout", event => { if (event.target.closest("[data-tip]")) hide(); });
      document.addEventListener("focusout", event => { if (event.target.closest("[data-tip]")) hide(); });
      tip.addEventListener("click", event => {
        if (event.target.closest("button")) {
          hide();
          saveMemory("dismissedTooltips", { lastDismissedAt: now() }, { source: "tooltip" });
        }
      });
      document.addEventListener("keydown", event => { if (event.key === "Escape") hide(); });
    }
    function trackFormMemory() {
      ["projectForm", "quoteForm", "paymentForm"].forEach(id => {
        const form = $("#" + id);
        if (!form || !form.elements) return;
        form.addEventListener("input", () => {
          clearTimeout(formEditTimers[id]);
          formEditTimers[id] = setTimeout(() => {
            try { saveMemory(`draft_${id}`, parseForm(form), { activity: "form_edit_10s", requireMeaningful: true }); } catch {}
          }, 10000);
        });
      });
    }
    async function continueRecentProject() {
      const projectId = getMemory("lastActiveProjectId");
      const all = await api("/api/recent", { limit: 50 });
      const project = all.find(item => item.id === projectId) || all[0];
      if (!project) {
        toast("No recent project yet.");
        setView("project");
        return;
      }
      setView("project");
      renderProject(project, "Restored project");
      const state = getMemory("inspectorState");
      if (state) shellState(state);
      saveMemory("lastActiveProjectId", project.id, { activity: "return_project", requireMeaningful: true });
      toast("Restored your last project.");
    }

    document.addEventListener("change", (event) => {
      if (event.target.matches("select")) syncOtherFields(event.target.closest("form") || document);
      if (event.target.matches(".check-row input[type='checkbox']")) {
        const row = event.target.closest(".check-row");
        row?.classList.toggle("checked", event.target.checked);
        toast(event.target.checked ? "Checked. You can remove it if you do not need it." : "Unchecked. It will stay on the checklist.");
      }
    });

    document.addEventListener("click", async (event) => {
      const viewButton = event.target.closest("[data-view]");
      if (viewButton) setView(viewButton.dataset.view);
      const copyButton = event.target.closest("[data-copy]");
      if (copyButton) { await navigator.clipboard.writeText(decodeURIComponent(copyButton.dataset.copy)); toast("Copied. You can paste it anywhere now."); }
      const selectCheckItem = event.target.closest("[data-select-check-item]");
      if (selectCheckItem) {
        event.preventDefault();
        const row = selectCheckItem.closest(".check-row");
        const box = row?.querySelector("input[type='checkbox']");
        if (box) { box.checked = !box.checked; row.classList.toggle("checked", box.checked); toast(box.checked ? "Selected for export." : "Removed from export selection."); }
      }
      const removeCheckItem = event.target.closest("[data-remove-check-item]");
      if (removeCheckItem) { event.preventDefault(); removeChecklistIndexes([Number(removeCheckItem.dataset.removeCheckItem)]); }
      const removeCheckedChecklist = event.target.closest("[data-remove-checked-checklist]");
      if (removeCheckedChecklist) { event.preventDefault(); removeChecklistIndexes(selectedChecklistIndexes()); }
      const exportSelectedChecklistButton = event.target.closest("[data-export-selected-checklist]");
      if (exportSelectedChecklistButton) { event.preventDefault(); exportSelectedChecklist(exportSelectedChecklistButton.dataset.exportSelectedChecklist); }
      const openProject = event.target.closest("[data-open-project]");
      if (openProject) {
        const project = lastRecent.find(item => item.id === openProject.dataset.openProject) || (await api("/api/recent", { limit: 50 })).find(item => item.id === openProject.dataset.openProject);
        if (project) { setView("project"); renderProject(project, "Recent project"); toast("Project opened."); }
      }
      const lessonDone = event.target.closest("[data-complete-lesson]");
      if (lessonDone) completeLesson(lessonDone.dataset.completeLesson);
      const accent = event.target.closest("[data-accent-dot]");
      if (accent) setAccent(accent.dataset.accentDot);
      const removeCustom = event.target.closest("[data-remove-custom]");
      if (removeCustom) {
        event.preventDefault();
        await removeListItem(removeCustom.dataset.removeCustom, decodeURIComponent(removeCustom.dataset.customValue || ""));
      }
      const removeSelected = event.target.closest("[data-remove-selected]");
      if (removeSelected) {
        event.preventDefault();
        const fieldName = removeSelected.dataset.removeSelected;
        const form = removeSelected.closest("form") || document;
        const label = removeSelected.closest("label");
        const select = label?.querySelector("select") || form.querySelector(`select[name="${fieldName}"]`);
        if (select) {
          const key = fieldName === "service" ? CUSTOM_SERVICES_KEY : CUSTOM_PROJECT_TYPES_KEY;
          await removeListItem(key, select.value);
        }
      }
      const feedback = event.target.closest("[data-feedback]");
      if (feedback) {
        saveMemory("lastFeedbackChoice", feedback.dataset.feedback, { source: "feedback" });
        if (feedback.dataset.feedback === "comment") $("#feedbackModal").classList.add("show");
        else toast("Thanks for the feedback.");
      }
    });

    $("#projectForm").addEventListener("submit", async (event) => {
      event.preventDefault();
      const button = $("#projectGenerate");
      setLoading(button, true);
      notice($("#projectStatus"), "Creating client package...");
      try {
        const payload = parseForm(event.currentTarget);
        const project = await api("/api/project", payload);
        renderProject(project);
        loadServices().catch(error => toast(error.message));
        saveMemory("lastActiveProjectId", project.id, { activity: "project_generated", requireMeaningful: true });
        saveMemory("lastUsedService", payload.service, { activity: "project_generated", requireMeaningful: true });
        saveMemory("preferredUpfrontPercent", payload.upfront_percent, { activity: "project_generated", requireMeaningful: true });
        safeCompleteLesson("first_project");
        notice($("#projectStatus"), "Created. Review it in the client-ready preview.", "success");
        toast("Client package created.");
        loadRecent().then(renderFeedbackPrompt);
      } catch (error) {
        notice($("#projectStatus"), error.message, "error");
        toast("Create failed.");
      } finally { setLoading(button, false); }
    });
    $("#quoteForm").addEventListener("submit", async (event) => {
      event.preventDefault();
      const button = event.submitter || $("#quoteGenerate");
      setLoading(button, true);
      notice($("#quoteStatus"), "Creating quote...");
      try {
        const payload = parseForm(event.currentTarget);
        const quote = await api("/api/quote", payload);
        preview("Quote", [{ title: "Quote", value: quote }]);
        notice($("#quoteStatus"), "Quote ready. Project type is included in the preview.", "success");
        loadServices().catch(error => toast(error.message));
        saveMemory("lastQuoteForm", payload, { activity: "quote_generated", requireMeaningful: true });
        safeCompleteLesson("quote");
        toast("Quote ready. Check the preview panel.");
      } catch (error) {
        notice($("#quoteStatus"), error.message, "error");
        toast(error.message);
      } finally { setLoading(button, false); }
    });
    $("#paymentForm").addEventListener("submit", async (event) => {
      event.preventDefault();
      const button = event.submitter || $("#paymentGenerate");
      setLoading(button, true);
      notice($("#paymentStatus"), "Calculating payment...");
      try {
        const form = event.currentTarget;
        const payload = parseForm(form);
        const payment = await api("/api/payment", payload);
        preview("Payment", [{ title: "Payment", value: payment }]);
        notice($("#paymentStatus"), "Payment breakdown ready. Check the preview panel.", "success");
        saveMemory("preferredUpfrontPercent", payload.upfront_percent, { activity: "payment_generated", requireMeaningful: true });
        safeCompleteLesson("payment");
        toast("Payment ready.");
      } catch (error) {
        notice($("#paymentStatus"), error.message, "error");
        toast(error.message);
      } finally { setLoading(button, false); }
    });
    $("#checklistForm").addEventListener("submit", async (event) => {
      event.preventDefault();
      const button = event.submitter || $("#checklistGenerate");
      setLoading(button, true);
      notice($("#checklistStatus"), "Creating checklist...");
      try {
        const payload = parseForm(event.currentTarget);
        const checklist = await api("/api/checklist", payload);
        preview("Checklist", [{ title: "Checklist", value: checklist }]);
        notice($("#checklistStatus"), "Checklist created. You can tick items as you finish them.", "success");
        loadProjectTypes();
        syncOtherFields();
        safeCompleteLesson("checklist");
        toast("Checklist created. You can remove or export selected items.");
      } catch (error) {
        notice($("#checklistStatus"), error.message, "error");
        toast(error.message);
      } finally { setLoading(button, false); }
    });
    $("#settingsForm").addEventListener("submit", async (event) => {
      event.preventDefault();
      const payload = parseForm(event.currentTarget);
      const services = {};
      String(payload.services_text || "").split("\\n").forEach(line => {
        const parts = line.includes("|") ? line.split("|") : line.split(":");
        if (parts.length >= 2 && parts[0].trim() && parts.slice(1).join(":").trim()) services[parts[0].trim()] = parts.slice(1).join(":").trim();
      });
      payload.services = services;
      try {
        const saved = await api("/api/save-profile", payload);
        greeting(saved);
        await loadServices();
        preview("Settings saved", [{ title: "Settings", value: "Your business profile has been updated." }]);
        toast("Settings saved.");
      } catch (error) { toast(error.message); }
    });
    $("#showServices").addEventListener("click", async () => {
      const services = await api("/api/services");
      preview("Services", [{ title: "Services", value: services }]);
      safeCompleteLesson("services");
      toast("Services shown.");
    });
    $("#continueRecent").addEventListener("click", continueRecentProject);
    $("#continueLearning").addEventListener("click", continueLearning);
    $("#walkthroughHelp").addEventListener("click", openWalkthrough);
    $("#closeWalkthrough").addEventListener("click", closeWalkthrough);
    $("#walkthroughPrimary").addEventListener("click", guideFromWalkthrough);
    $("#walkthroughLearn").addEventListener("click", () => { closeWalkthrough(); setView("learn"); toast("Learn is open."); });
    $("#refreshRecent").addEventListener("click", loadRecent);
    $("#copyInspector").addEventListener("click", async () => {
      if (!lastPreviewText) return toast("Nothing to copy yet.");
      await navigator.clipboard.writeText(lastPreviewText);
      toast("Preview copied.");
    });
    $("#exportTxt").addEventListener("click", async () => {
      if (!lastProject) return toast("Create a project first.");
      const result = await api("/api/export", { project_id: lastProject.id, file_format: "txt" });
      saveMemory("lastExportFormat", "txt", { activity: "export_clicked", requireMeaningful: true });
      safeCompleteLesson("export");
      toast(`Saved: ${result.file_name || "TXT file"}`);
    });
    $("#exportMd").addEventListener("click", async () => {
      if (!lastProject) return toast("Create a project first.");
      const result = await api("/api/export", { project_id: lastProject.id, file_format: "md" });
      saveMemory("lastExportFormat", "md", { activity: "export_clicked", requireMeaningful: true });
      safeCompleteLesson("export");
      toast(`Saved: ${result.file_name || "Markdown file"}`);
    });
    $("#exportPdf").addEventListener("click", async () => {
      if (!lastProject) return toast("Create a project first.");
      const result = await api("/api/export", { project_id: lastProject.id, file_format: "pdf" });
      saveMemory("lastExportFormat", "pdf", { activity: "export_clicked", requireMeaningful: true });
      safeCompleteLesson("export");
      toast(`Saved: ${result.file_name || "PDF file"}`);
    });
    $("#themeBtn").addEventListener("click", () => {
      const next = document.documentElement.dataset.theme === "light" ? "dark" : "light";
      document.documentElement.dataset.theme = next;
      localStorage.setItem("theme", next);
      toast(`${next === "dark" ? "Dark" : "Light"} mode`);
    });
    $("#toggleMemory").addEventListener("click", () => {
      saveMemory("memoryStatus", memoryOn() ? "off" : "on", { source: "settings" });
      renderMemorySettings();
      toast(memoryOn() ? "Creative Studio can remember where you left off for 7 days." : "Memory is off.");
    });
    $("#clearMemory").addEventListener("click", clearMemory);
    $("#saveOnboardingName").addEventListener("click", async () => {
      const name = String($("#onboardingName")?.value || "").trim();
      if (!name) return toast("Type your name or choose Skip for now.");
      try {
        const saved = await api("/api/save-profile", { ...currentProfile, owner_name: name });
        currentProfile = saved || { ...currentProfile, owner_name: name };
        localStorage.setItem("creativeStudioNameOnboarded", "yes");
        syncSettingsProfile(currentProfile);
        greeting(currentProfile);
        closeNameOnboarding();
        toast("Name saved.");
      } catch (error) { toast(error.message); }
    });
    $("#skipOnboardingName").addEventListener("click", () => {
      localStorage.setItem("creativeStudioNameOnboarded", "skipped");
      closeNameOnboarding();
      greeting(currentProfile || {});
      toast("No problem. You can add your name in Settings later.");
    });
    $("#saveFeedback").addEventListener("click", () => {
      const feedback = JSON.parse(localStorage.getItem("creativeStudioFeedback") || "[]");
      feedback.unshift({ createdAt: new Date().toISOString(), comment: $("#feedbackText").value.trim(), choice: getMemory("lastFeedbackChoice") });
      localStorage.setItem("creativeStudioFeedback", JSON.stringify(feedback.slice(0, 20)));
      $("#feedbackModal").classList.remove("show");
      $("#feedbackText").value = "";
      toast("Feedback saved locally.");
    });
    $("#closeFeedback").addEventListener("click", () => $("#feedbackModal").classList.remove("show"));
    $("#collapseInspector").addEventListener("click", () => shellState("collapsed"));
    $("#expandInspector").addEventListener("click", () => shellState($("#shell").classList.contains("inspector-wide") ? "open" : "wide"));
    $("#handleInspector").addEventListener("click", () => shellState($("#shell").classList.contains("inspector-wide") ? "open" : "wide"));
    $("#closeInspector").addEventListener("click", () => shellState("closed"));
    $("#restoreInspector").addEventListener("click", () => shellState("open"));
    $("#openInspector").addEventListener("click", () => shellState("open"));
    document.querySelector("[data-clear]").addEventListener("click", () => {
      $("#projectStatus").innerHTML = "";
      preview("Ready", [{ title: "Ready", value: "Run a tool to see the latest result here." }]);
    });
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) document.documentElement.dataset.theme = savedTheme;
    const savedAccent = getMemory("accentTheme") || "purple";
    if (savedAccent !== "purple") document.documentElement.dataset.accent = savedAccent;
    renderThemeDots();
    renderMemorySettings();
    renderFAQ("#faqList");
    renderFAQ("#settingsFaqList");
    renderLearn();
    renderCustomAdditions();
    setupTooltips();
    trackFormMemory();
    loadServices().then(loadProfile).then(loadRecent).then(() => {
      fillForm($("#projectForm"), getMemory("draft_projectForm") || {});
      const up = getMemory("preferredUpfrontPercent");
      const projectForm = $("#projectForm");
      if (up && projectForm?.elements?.upfront_percent) projectForm.elements.upfront_percent.value = up;
      const lastPreview = getMemory("lastPreview");
      if (lastPreview) preview(lastPreview.title || "Restored preview", lastPreview.sections || []);
    }).catch(error => toast(error.message));
  </script>
</body>
</html>"""

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

    def send_bytes(self, status, body, content_type):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "public, max-age=86400")
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        if not length:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def do_GET(self):
        parsed_path = unquote(urlparse(self.path).path)
        if parsed_path in ("/", "/index.html"):
            self.send_text(200, HTML, "text/html")
            return
        if parsed_path.startswith("/assets/"):
            asset_name = os.path.basename(parsed_path)
            asset_path = os.path.join(os.path.dirname(__file__), "assets", asset_name)
            if os.path.isfile(asset_path):
                content_type = mimetypes.guess_type(asset_path)[0] or "application/octet-stream"
                with open(asset_path, "rb") as file:
                    self.send_bytes(200, file.read(), content_type)
                return
        self.send_text(404, "Not found", "text/plain")

    def do_POST(self):
        try:
            payload = self.read_json()
            if self.path == "/api/profile":
                result = get_brand_profile()
            elif self.path == "/api/save-profile":
                if "services" not in payload:
                    payload["services"] = parse_services_text(payload.get("services_text", ""))
                result = save_brand_profile(payload)
            elif self.path == "/api/services":
                result = list_services()
            elif self.path == "/api/remove-service":
                service_name = str(payload.get("service", "")).strip()
                profile = get_brand_profile()
                services = dict(profile.get("services", {}))
                before = len(services)
                services = {
                    name: value
                    for name, value in services.items()
                    if name.strip().lower() != service_name.lower()
                }
                profile["services"] = services
                saved = save_brand_profile(profile)
                result = {"removed": len(services) != before, "profile": saved}
            elif self.path == "/api/payment":
                result = calculate_payment(payload.get("total_fee", 0), payload.get("upfront_percent", 70))
            elif self.path == "/api/quote":
                result = create_quote(payload.get("client_name", ""), payload.get("service", ""), payload.get("design_fee", 0), payload.get("project_type", ""))
            elif self.path == "/api/checklist":
                result = generate_project_checklist(payload.get("project_type", ""))
            elif self.path == "/api/project":
                package = create_project_package(
                    payload.get("client_name", ""),
                    payload.get("service", ""),
                    payload.get("design_fee", 0),
                    payload.get("upfront_percent", 70),
                    payload.get("project_type", ""),
                )
                result = save_project(
                    payload.get("client_name", ""),
                    payload.get("service", ""),
                    payload.get("design_fee", 0),
                    payload.get("upfront_percent", 70),
                    payload.get("project_type", ""),
                    package,
                )
            elif self.path == "/api/recent":
                result = list_recent_projects(payload.get("limit", 8))
            elif self.path == "/api/bin":
                result = list_deleted_projects(payload.get("limit", 20))
            elif self.path == "/api/delete":
                result = delete_project(payload.get("project_id", ""))
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

def find_port(start=8765, end=8795):
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











