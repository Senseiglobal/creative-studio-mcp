import json
import socket
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from business_tools import (
    calculate_payment,
    create_project_package,
    create_quote,
    generate_project_checklist,
    get_brand_profile,
    list_recent_projects,
    list_services,
    parse_services_text,
    save_brand_profile,
    save_project,
)


HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <title>Creative Studio MCP</title>
  <style>
    :root {
      --font-ui: Arial, Helvetica, sans-serif;
      --font-mono: Consolas, Monaco, monospace;

      --space-1: .25rem;
      --space-2: .5rem;
      --space-3: .75rem;
      --space-4: 1rem;
      --space-5: 1.25rem;
      --space-6: 1.5rem;
      --space-8: 2rem;
      --space-10: 2.5rem;

      --radius-sm: .5rem;
      --radius-md: .75rem;
      --radius-lg: 1rem;
      --radius-xl: 1.25rem;

      --shadow-sm: 0 1px 2px rgba(15, 23, 42, .08);
      --shadow-md: 0 12px 30px rgba(15, 23, 42, .12);

      --motion-fast: 140ms ease;
      --motion-med: 220ms ease;

      --bg: #f6f7f4;
      --surface: #ffffff;
      --surface-soft: #eef3ef;
      --surface-strong: #e5ece6;
      --ink: #131a15;
      --muted: #5f6b63;
      --line: #d9e1da;
      --primary: #18713a;
      --primary-strong: #10542a;
      --primary-soft: #e5f5ea;
      --danger: #b42318;
      --danger-soft: #fff1f0;
      --focus: #1769e0;
      --code-bg: #111827;
      --code-ink: #f8fafc;
    }

    [data-theme="dark"] {
      --bg: #0f1511;
      --surface: #151d18;
      --surface-soft: #1e2922;
      --surface-strong: #26342b;
      --ink: #f2f6f2;
      --muted: #b8c4ba;
      --line: #2e3b32;
      --primary: #7ddc97;
      --primary-strong: #a4efb8;
      --primary-soft: #183923;
      --danger: #ffb4ab;
      --danger-soft: #3f1714;
      --focus: #9cc4ff;
      --code-bg: #050807;
      --code-ink: #eef8f0;
      color-scheme: dark;
    }

    * {
      box-sizing: border-box;
    }

    html {
      scroll-behavior: smooth;
    }

    body {
      margin: 0;
      min-height: 100vh;
      background:
        radial-gradient(circle at top left, rgba(24, 113, 58, .10), transparent 28rem),
        var(--bg);
      color: var(--ink);
      font-family: var(--font-ui);
      line-height: 1.5;
      text-rendering: optimizeLegibility;
    }

    body.onboarding-open {
      overflow: hidden;
    }

    a {
      color: inherit;
    }

    button,
    input,
    select,
    textarea {
      font: inherit;
    }

    button {
      min-height: 48px;
      border: 0;
      cursor: pointer;
      touch-action: manipulation;
    }

    button:disabled {
      opacity: .55;
      cursor: not-allowed;
    }

    :focus-visible {
      outline: 3px solid var(--focus);
      outline-offset: 3px;
    }

    .skip-link {
      position: fixed;
      top: var(--space-3);
      left: var(--space-3);
      z-index: 30;
      transform: translateY(-140%);
      padding: var(--space-3) var(--space-4);
      border-radius: var(--radius-md);
      background: var(--ink);
      color: var(--bg);
      font-weight: 700;
      transition: transform var(--motion-fast);
    }

    .skip-link:focus {
      transform: translateY(0);
    }

    .app-shell {
      display: grid;
      grid-template-columns: 18rem minmax(0, 1fr);
      min-height: 100vh;
    }

    .sidebar {
      position: sticky;
      top: 0;
      height: 100vh;
      padding: var(--space-6);
      background: rgba(21, 29, 24, .96);
      color: #f8fafc;
      border-right: 1px solid rgba(255, 255, 255, .08);
    }

    .brand {
      display: flex;
      gap: var(--space-3);
      align-items: center;
      margin-bottom: var(--space-8);
    }

    .brand-mark {
      width: 48px;
      height: 48px;
      display: grid;
      place-items: center;
      border-radius: var(--radius-lg);
      background: linear-gradient(135deg, #6ee78b, #18713a);
      color: #07130a;
      font-weight: 900;
      box-shadow: var(--shadow-md);
    }

    .brand strong {
      display: block;
      font-size: 1rem;
    }

    .brand span {
      display: block;
      margin-top: 2px;
      color: rgba(248, 250, 252, .72);
      font-size: .875rem;
    }

    .nav {
      display: grid;
      gap: var(--space-2);
    }

    .nav button {
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: var(--space-3);
      padding: 0 var(--space-4);
      border-radius: var(--radius-md);
      background: transparent;
      color: rgba(248, 250, 252, .86);
      text-align: left;
      transition: background var(--motion-fast), color var(--motion-fast), transform var(--motion-fast);
    }

    .nav button:hover,
    .nav button.active {
      background: rgba(255, 255, 255, .11);
      color: #fff;
    }

    .nav button:active {
      transform: scale(.99);
    }

    .main {
      min-width: 0;
      padding: clamp(1rem, 2.5vw, 2rem);
    }

    .topbar {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: var(--space-4);
      margin-bottom: var(--space-6);
    }

    .title-block {
      max-width: 48rem;
    }

    .eyebrow {
      display: inline-flex;
      align-items: center;
      gap: var(--space-2);
      margin-bottom: var(--space-2);
      color: var(--primary-strong);
      font-size: .84rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: .08em;
    }

    h1,
    h2,
    h3 {
      margin: 0;
      letter-spacing: 0;
      line-height: 1.12;
    }

    h1 {
      font-size: clamp(2rem, 4vw, 3.6rem);
      font-weight: 850;
    }

    h2 {
      font-size: clamp(1.35rem, 2vw, 1.85rem);
    }

    h3 {
      font-size: 1.05rem;
    }

    p {
      margin: var(--space-2) 0 0;
      color: var(--muted);
    }

    .toolbar {
      display: flex;
      flex-wrap: wrap;
      gap: var(--space-2);
      align-items: center;
      justify-content: flex-end;
    }

    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: var(--space-2);
      min-height: 48px;
      padding: 0 var(--space-5);
      border-radius: 999px;
      font-weight: 800;
      transition: transform var(--motion-fast), box-shadow var(--motion-fast), background var(--motion-fast), color var(--motion-fast), border-color var(--motion-fast);
    }

    .btn:active {
      transform: scale(.98);
    }

    .btn-primary {
      background: var(--primary);
      color: #fff;
      box-shadow: 0 10px 20px rgba(24, 113, 58, .20);
    }

    .btn-primary:hover {
      background: var(--primary-strong);
      box-shadow: var(--shadow-md);
    }

    [data-theme="dark"] .btn-primary {
      color: #07130a;
    }

    .btn-secondary {
      background: var(--surface);
      color: var(--ink);
      border: 1px solid var(--line);
    }

    .btn-secondary:hover {
      border-color: var(--primary);
      color: var(--primary-strong);
    }

    .btn-ghost {
      background: transparent;
      color: var(--ink);
      border: 1px solid transparent;
    }

    .btn-ghost:hover {
      background: var(--surface-soft);
    }

    .btn-danger {
      background: var(--danger-soft);
      color: var(--danger);
      border: 1px solid color-mix(in srgb, var(--danger), transparent 70%);
    }

    .section {
      display: none;
      animation: sectionIn var(--motion-med);
    }

    .section.active {
      display: block;
    }

    .hero,
    .panel,
    .card,
    .output,
    .onboarding-card {
      background: color-mix(in srgb, var(--surface), transparent 2%);
      border: 1px solid var(--line);
      border-radius: var(--radius-xl);
      box-shadow: var(--shadow-sm);
    }

    .hero {
      padding: clamp(1.35rem, 3vw, 2rem);
      margin-bottom: var(--space-6);
    }

    .card-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: var(--space-4);
    }

    .card {
      min-height: 10rem;
      padding: var(--space-5);
      text-align: left;
      color: var(--ink);
      transition: transform var(--motion-fast), box-shadow var(--motion-fast), border-color var(--motion-fast), background var(--motion-fast);
    }

    .card:hover {
      transform: translateY(-3px);
      border-color: color-mix(in srgb, var(--primary), var(--line) 45%);
      box-shadow: var(--shadow-md);
    }

    .card .icon {
      width: 2.5rem;
      height: 2.5rem;
      display: grid;
      place-items: center;
      margin-bottom: var(--space-4);
      border-radius: var(--radius-md);
      background: var(--primary-soft);
      color: var(--primary-strong);
      font-weight: 900;
    }

    .panel {
      padding: clamp(1rem, 2vw, 1.5rem);
      margin-top: var(--space-5);
    }

    .panel-head {
      display: flex;
      justify-content: space-between;
      gap: var(--space-4);
      align-items: flex-start;
      margin-bottom: var(--space-4);
    }

    .onboarding-card {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: var(--space-4);
      align-items: center;
      padding: var(--space-5);
      margin-bottom: var(--space-5);
      background: linear-gradient(135deg, var(--primary-soft), var(--surface));
    }

    .recent-list {
      display: grid;
      gap: var(--space-3);
    }

    .recent-item {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: var(--space-3);
      align-items: center;
      padding: var(--space-4);
      border: 1px solid var(--line);
      border-radius: var(--radius-lg);
      background: var(--surface);
    }

    .empty {
      padding: var(--space-5);
      border-radius: var(--radius-lg);
      background: var(--surface-soft);
      color: var(--muted);
    }

    form {
      display: grid;
      gap: var(--space-5);
    }

    .form-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: var(--space-5);
    }

    label {
      display: grid;
      gap: var(--space-2);
      color: var(--ink);
      font-weight: 800;
    }

    .helper {
      color: var(--muted);
      font-size: .9rem;
      font-weight: 400;
    }

    input,
    select,
    textarea {
      width: 100%;
      min-height: 48px;
      padding: 0 var(--space-4);
      border: 1px solid var(--line);
      border-radius: var(--radius-md);
      background: var(--surface);
      color: var(--ink);
      transition: border-color var(--motion-fast), box-shadow var(--motion-fast), background var(--motion-fast);
    }

    textarea {
      min-height: 8rem;
      padding-top: var(--space-3);
      resize: vertical;
    }

    input:hover,
    select:hover,
    textarea:hover {
      border-color: color-mix(in srgb, var(--primary), var(--line) 55%);
    }

    .output-grid {
      display: grid;
      gap: var(--space-4);
      margin-top: var(--space-5);
    }

    .output {
      padding: var(--space-5);
    }

    .output-head {
      display: flex;
      justify-content: space-between;
      gap: var(--space-3);
      align-items: center;
    }

    pre {
      margin: var(--space-4) 0 0;
      padding: var(--space-4);
      border-radius: var(--radius-md);
      background: var(--code-bg);
      color: var(--code-ink);
      white-space: pre-wrap;
      word-break: break-word;
      font-family: var(--font-mono);
      font-size: .92rem;
      line-height: 1.55;
    }

    .message {
      display: none;
      padding: var(--space-3) var(--space-4);
      border-radius: var(--radius-md);
      background: var(--surface-soft);
      color: var(--ink);
    }

    .message.error {
      background: var(--danger-soft);
      color: var(--danger);
      border: 1px solid color-mix(in srgb, var(--danger), transparent 70%);
    }

    .toast {
      position: fixed;
      right: var(--space-5);
      bottom: var(--space-5);
      z-index: 40;
      max-width: min(24rem, calc(100vw - 2rem));
      padding: var(--space-4) var(--space-5);
      border-radius: var(--radius-lg);
      background: var(--ink);
      color: var(--bg);
      box-shadow: var(--shadow-md);
      opacity: 0;
      transform: translateY(1rem);
      pointer-events: none;
      transition: opacity var(--motion-med), transform var(--motion-med);
    }

    .toast.show {
      opacity: 1;
      transform: translateY(0);
    }

    .tooltip-wrap {
      position: relative;
      display: inline-flex;
      align-items: center;
      gap: var(--space-2);
    }

    .tip-btn {
      width: 32px;
      height: 32px;
      min-height: 32px;
      border-radius: 999px;
      background: var(--surface-soft);
      color: var(--ink);
      font-weight: 900;
    }

    .tooltip {
      position: absolute;
      top: calc(100% + .5rem);
      right: 0;
      width: min(18rem, calc(100vw - 2rem));
      z-index: 20;
      display: none;
      padding: var(--space-4);
      border: 1px solid var(--line);
      border-radius: var(--radius-md);
      background: var(--surface);
      color: var(--ink);
      box-shadow: var(--shadow-md);
      font-weight: 400;
    }

    .tooltip-wrap:focus-within .tooltip,
    .tooltip-wrap:hover .tooltip {
      display: block;
    }

    .modal {
      position: fixed;
      inset: 0;
      z-index: 50;
      display: none;
      place-items: center;
      padding: var(--space-4);
      background: rgba(0, 0, 0, .42);
    }

    .modal.show {
      display: grid;
    }

    .modal-card {
      width: min(42rem, 100%);
      max-height: min(42rem, calc(100vh - 2rem));
      overflow: auto;
      padding: var(--space-6);
      border-radius: var(--radius-xl);
      background: var(--surface);
      color: var(--ink);
      box-shadow: var(--shadow-md);
    }

    .modal-actions {
      display: flex;
      flex-wrap: wrap;
      justify-content: flex-end;
      gap: var(--space-3);
      margin-top: var(--space-5);
    }

    @keyframes sectionIn {
      from {
        opacity: 0;
        transform: translateY(.5rem);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    @media (max-width: 1100px) {
      .card-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }

    @media (max-width: 760px) {
      .app-shell {
        grid-template-columns: 1fr;
      }

      .sidebar {
        position: static;
        height: auto;
        padding: var(--space-4);
      }

      .nav {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }

      .main {
        padding: var(--space-4);
      }

      .topbar,
      .panel-head,
      .onboarding-card,
      .recent-item,
      .output-head {
        align-items: stretch;
        grid-template-columns: 1fr;
        flex-direction: column;
      }

      .card-grid,
      .form-grid {
        grid-template-columns: 1fr;
      }
    }

    @media (prefers-reduced-motion: reduce) {
      *,
      *::before,
      *::after {
        animation-duration: .001ms !important;
        animation-iteration-count: 1 !important;
        scroll-behavior: auto !important;
        transition-duration: .001ms !important;
      }
    }
  </style>
</head>
<body>
  <a href="#main" class="skip-link">Skip to content</a>
  <div class="app-shell">
    <aside class="sidebar" aria-label="Main navigation">
      <div class="brand">
        <div class="brand-mark" aria-hidden="true">CS</div>
        <div>
          <strong>Creative Studio MCP</strong>
          <span>Creative workspace</span>
        </div>
      </div>
      <nav class="nav">
        <button class="active" type="button" data-view="home" aria-current="page">Home</button>
        <button type="button" data-view="new-project">New Project</button>
        <button type="button" data-view="settings">Settings</button>
        <button type="button" data-view="quote">Quote</button>
        <button type="button" data-view="payment">Payment</button>
        <button type="button" data-view="checklist">Checklist</button>
        <button type="button" data-view="services">Services</button>
      </nav>
    </aside>

    <main id="main" class="main" tabindex="-1">
      <section id="home" class="section active" aria-labelledby="home-title">
        <div class="hero">
          <div class="topbar">
            <div class="title-block">
              <span class="eyebrow">Local-first creative dashboard</span>
              <h1 id="home-title">Creative Studio MCP</h1>
              <p>Create project packages using your services, pricing, payment terms, and brand voice.</p>
            </div>
            <div class="toolbar">
              <div class="tooltip-wrap">
                <button class="btn btn-secondary" id="theme-toggle" type="button" aria-label="Switch theme">Theme</button>
                <div class="tooltip" role="tooltip">Switch between light and dark mode. Your choice is saved on this device.</div>
              </div>
              <button class="btn btn-primary" type="button" data-view="new-project">New Project</button>
            </div>
          </div>
        </div>

        <div id="onboarding-card" class="onboarding-card">
          <div>
            <h2>Start with your first project</h2>
            <p>Set your business details, create a project package, then copy the quote or email draft.</p>
          </div>
          <div class="toolbar">
            <button class="btn btn-secondary" type="button" data-view="settings">Set Business</button>
            <button class="btn btn-primary" type="button" data-view="new-project">Create Project</button>
            <button class="btn btn-ghost" type="button" id="dismiss-onboarding">Dismiss</button>
          </div>
        </div>

        <div class="card-grid" aria-label="Quick actions">
          <button class="card" type="button" data-view="new-project">
            <span class="icon" aria-hidden="true">01</span>
            <h3>New Project</h3>
            <p>Quote, payment, checklist, deliverables, and email in one flow.</p>
          </button>
          <button class="card" type="button" data-view="settings">
            <span class="icon" aria-hidden="true">02</span>
            <h3>Business Settings</h3>
            <p>Edit your brand profile, terms, and service database.</p>
          </button>
          <button class="card" type="button" data-view="quote">
            <span class="icon" aria-hidden="true">03</span>
            <h3>Quote</h3>
            <p>Create a quick client-ready quote.</p>
          </button>
          <button class="card" type="button" data-view="services">
            <span class="icon" aria-hidden="true">04</span>
            <h3>Services</h3>
            <p>Review the saved service list and price ranges.</p>
          </button>
        </div>

        <div class="panel">
          <div class="panel-head">
            <div>
              <h2>Recent Projects</h2>
              <p>Saved locally in <strong>projects.json</strong>.</p>
            </div>
            <button class="btn btn-secondary" type="button" id="refresh-recent">Refresh</button>
          </div>
          <div id="recent" class="recent-list" aria-live="polite"></div>
        </div>
      </section>

      <section id="settings" class="section" aria-labelledby="settings-title">
        <div class="topbar">
          <div>
            <span class="eyebrow">Preferences</span>
            <h1 id="settings-title">Business Settings</h1>
            <p>Edit your local brand database. These preferences are saved in <strong>brand_profile.json</strong>.</p>
          </div>
        </div>
        <div class="panel">
          <form id="settings-form">
            <div class="form-grid">
              <label>Business name
                <input name="business_name" autocomplete="organization">
                <span class="helper">Used in quotes and emails.</span>
              </label>
              <label>Owner name
                <input name="owner_name" autocomplete="name">
                <span class="helper">Used as the sign-off name.</span>
              </label>
              <label>Email
                <input name="email" autocomplete="email">
                <span class="helper">Optional contact detail.</span>
              </label>
              <label>Phone
                <input name="phone" autocomplete="tel">
                <span class="helper">Optional contact detail.</span>
              </label>
              <label>Website
                <input name="website" autocomplete="url">
                <span class="helper">Optional website or portfolio link.</span>
              </label>
              <label>Location
                <input name="location" autocomplete="address-level2">
                <span class="helper">Optional city or service area.</span>
              </label>
              <label>Currency
                <input name="currency" value="USD">
                <span class="helper">Use USD for dollar formatting.</span>
              </label>
            </div>
            <label>Brand voice
              <textarea name="brand_voice"></textarea>
              <span class="helper">Example: professional, warm, clear, and confident.</span>
            </label>
            <label>Payment terms
              <textarea name="payment_terms"></textarea>
              <span class="helper">This appears in quotes and emails.</span>
            </label>
            <label>Services and price ranges
              <textarea name="services_text"></textarea>
              <span class="helper">One per line. Example: Brand Identity Design | $500 to $2,500+</span>
            </label>
            <div class="toolbar">
              <button class="btn btn-primary" type="submit">Save</button>
              <button class="btn btn-secondary" type="button" data-view="new-project">New Project</button>
            </div>
            <div id="settings-message" class="message" role="status" aria-live="polite"></div>
          </form>
        </div>
      </section>

      <section id="new-project" class="section" aria-labelledby="project-title">
        <div class="topbar">
          <div>
            <span class="eyebrow">Project package</span>
            <h1 id="project-title">New Project</h1>
            <p>Generate a quote, payment breakdown, checklist, deliverables, and email draft.</p>
          </div>
        </div>
        <div class="panel">
          <form id="project-form">
            <div class="form-grid">
              <label>Client name
                <input name="client_name" value="John Smith" required>
                <span class="helper">Who is this project for?</span>
              </label>
              <label>Service
                <select name="service" id="project-service" required></select>
                <span class="helper">Choose from Business Settings.</span>
              </label>
              <label>Design fee
                <input name="design_fee" type="number" min="1" value="3000" required>
                <span class="helper">Use numbers only.</span>
              </label>
              <label>Upfront percent
                <input name="upfront_percent" type="number" min="0" max="100" value="70" required>
                <span class="helper">Example: 70 means 70% upfront.</span>
              </label>
              <label>Project type
                <input name="project_type" value="Brand identity project" required>
                <span class="helper">Example: branding, packaging, profile design.</span>
              </label>
            </div>
            <button class="btn btn-primary" type="submit">Generate</button>
            <div id="project-error" class="message error" role="alert"></div>
          </form>
          <div id="project-output" class="output-grid" aria-live="polite"></div>
        </div>
      </section>

      <section id="quote" class="section" aria-labelledby="quote-title">
        <h1 id="quote-title">Quote</h1>
        <div class="panel">
          <form id="quote-form">
            <div class="form-grid">
              <label>Client name <input name="client_name" value="John Smith" required></label>
              <label>Service <select name="service" id="quote-service" required></select></label>
              <label>Design fee <input name="design_fee" type="number" min="1" value="3000" required></label>
            </div>
            <button class="btn btn-primary" type="submit">Generate</button>
          </form>
          <div id="quote-output" aria-live="polite"></div>
        </div>
      </section>

      <section id="payment" class="section" aria-labelledby="payment-title">
        <h1 id="payment-title">Payment</h1>
        <div class="panel">
          <form id="payment-form">
            <div class="form-grid">
              <label>Total fee <input name="total_fee" type="number" min="1" value="5000" required></label>
              <label>Upfront percent <input name="upfront_percent" type="number" min="0" max="100" value="70" required></label>
            </div>
            <button class="btn btn-primary" type="submit">Generate</button>
          </form>
          <div id="payment-output" aria-live="polite"></div>
        </div>
      </section>

      <section id="checklist" class="section" aria-labelledby="checklist-title">
        <h1 id="checklist-title">Checklist</h1>
        <div class="panel">
          <form id="checklist-form">
            <label>Project type <input name="project_type" value="Product packaging design" required></label>
            <button class="btn btn-primary" type="submit">Generate</button>
          </form>
          <div id="checklist-output" aria-live="polite"></div>
        </div>
      </section>

      <section id="services" class="section" aria-labelledby="services-title">
        <h1 id="services-title">Services</h1>
        <div class="panel">
          <div class="toolbar">
            <button class="btn btn-primary" type="button" id="load-services">Generate</button>
            <button class="btn btn-secondary" type="button" data-view="settings">Edit Services</button>
          </div>
          <div id="services-output" aria-live="polite"></div>
        </div>
      </section>
    </main>
  </div>

  <div id="toast" class="toast" role="status" aria-live="polite"></div>

  <div id="onboarding-modal" class="modal" role="dialog" aria-modal="true" aria-labelledby="onboarding-title">
    <div class="modal-card">
      <h2 id="onboarding-title">Welcome to your creative workspace</h2>
      <p>Start by saving your business settings, then create your first project package. You can skip this and use the app anytime.</p>
      <div class="modal-actions">
        <button class="btn btn-secondary" type="button" id="skip-onboarding">Skip</button>
        <button class="btn btn-primary" type="button" id="start-onboarding">Set Business</button>
      </div>
    </div>
  </div>

  <script>
    const state = { services: {}, profile: {} };
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)");
    const savedTheme = localStorage.getItem("creativeStudioTheme");
    const initialTheme = savedTheme || (prefersDark.matches ? "dark" : "light");
    document.documentElement.dataset.theme = initialTheme;

    function toast(message) {
      const node = document.getElementById("toast");
      node.textContent = message;
      node.classList.add("show");
      clearTimeout(window.toastTimer);
      window.toastTimer = setTimeout(() => node.classList.remove("show"), 2200);
    }

    function showView(id) {
      document.querySelectorAll(".section").forEach((item) => item.classList.remove("active"));
      document.querySelectorAll(".nav button").forEach((item) => {
        item.classList.remove("active");
        item.removeAttribute("aria-current");
      });
      document.getElementById(id).classList.add("active");
      document.querySelectorAll(`[data-view="${id}"]`).forEach((item) => {
        if (item.tagName === "BUTTON" && item.closest(".nav")) {
          item.classList.add("active");
          item.setAttribute("aria-current", "page");
        }
      });
      document.getElementById("main").focus({ preventScroll: true });
      if (id === "home") loadRecent();
      if (id === "settings") loadProfileIntoForm();
    }

    document.querySelectorAll("[data-view]").forEach((item) => {
      item.addEventListener("click", () => showView(item.dataset.view));
    });

    document.getElementById("theme-toggle").addEventListener("click", () => {
      const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
      document.documentElement.dataset.theme = next;
      localStorage.setItem("creativeStudioTheme", next);
      toast(`${next === "dark" ? "Dark" : "Light"} mode on`);
    });

    async function api(path, payload = {}) {
      const response = await fetch(path, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Something went wrong.");
      return data.result;
    }

    function asText(value) {
      if (typeof value === "string") return value;
      if (Array.isArray(value)) return value.map((item, index) => `${index + 1}. ${item}`).join("\n");
      return Object.entries(value).map(([key, item]) => `${key}: ${item}`).join("\n");
    }

    function escapeHtml(text) {
      return String(text)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;");
    }

    function outputBlock(title, value) {
      const text = asText(value);
      return `<article class="output">
        <div class="output-head">
          <h3>${title}</h3>
          <button class="btn btn-secondary" type="button" data-copy="${encodeURIComponent(text)}">Copy</button>
        </div>
        <pre>${escapeHtml(text)}</pre>
      </article>`;
    }

    document.addEventListener("click", async (event) => {
      const button = event.target.closest("[data-copy]");
      if (!button) return;
      await navigator.clipboard.writeText(decodeURIComponent(button.dataset.copy));
      toast("Copied");
    });

    function formData(form) {
      return Object.fromEntries(new FormData(form).entries());
    }

    async function loadServices() {
      state.services = await api("/api/services");
      ["project-service", "quote-service"].forEach((id) => {
        const select = document.getElementById(id);
        select.innerHTML = "";
        Object.keys(state.services).forEach((name) => {
          const option = document.createElement("option");
          option.value = name;
          option.textContent = name;
          select.appendChild(option);
        });
      });
    }

    async function loadProfile() {
      state.profile = await api("/api/profile");
      await loadServices();
    }

    async function loadProfileIntoForm() {
      await loadProfile();
      const form = document.getElementById("settings-form");
      Object.entries(state.profile).forEach(([key, value]) => {
        if (form.elements[key] && key !== "services") form.elements[key].value = value || "";
      });
      form.elements.services_text.value = Object.entries(state.profile.services || {})
        .map(([name, price]) => `${name} | ${price}`)
        .join("\n");
    }

    document.getElementById("settings-form").addEventListener("submit", async (event) => {
      event.preventDefault();
      const data = formData(event.target);
      const message = document.getElementById("settings-message");
      try {
        state.profile = await api("/api/save-profile", data);
        await loadServices();
        message.textContent = "Business settings saved.";
        message.classList.remove("error");
        message.style.display = "block";
        toast("Settings saved");
      } catch (err) {
        message.textContent = err.message;
        message.classList.add("error");
        message.style.display = "block";
      }
    });

    async function loadRecent() {
      const target = document.getElementById("recent");
      const projects = await api("/api/recent", { limit: 8 });
      if (!projects.length) {
        target.innerHTML = `<div class="empty">No saved projects yet. Create one from New Project.</div>`;
        return;
      }
      target.innerHTML = projects.map((project) => `
        <article class="recent-item">
          <div>
            <h3>${escapeHtml(project.client_name)}</h3>
            <p>${escapeHtml(project.service)} at $${Number(project.design_fee).toLocaleString()}</p>
          </div>
          <button class="btn btn-secondary" type="button" data-copy="${encodeURIComponent(asText(project.generated_package.client_quote))}">Copy</button>
        </article>
      `).join("");
    }

    function renderPackage(project) {
      const pkg = project.generated_package;
      const full = [
        "CLIENT QUOTE", asText(pkg.client_quote), "",
        "PAYMENT BREAKDOWN", asText(pkg.payment_breakdown), "",
        "PROJECT CHECKLIST", asText(pkg.project_checklist), "",
        "DELIVERABLES", asText(pkg.deliverables), "",
        "CLIENT EMAIL", asText(pkg.client_email)
      ].join("\n");

      return `<article class="output">
        <div class="output-head">
          <h3>Full Project Package</h3>
          <button class="btn btn-primary" type="button" data-copy="${encodeURIComponent(full)}">Copy Full Package</button>
        </div>
      </article>
      ${outputBlock("Client Quote", pkg.client_quote)}
      ${outputBlock("Payment Breakdown", pkg.payment_breakdown)}
      ${outputBlock("Project Checklist", pkg.project_checklist)}
      ${outputBlock("Deliverables", pkg.deliverables)}
      ${outputBlock("Client Email", pkg.client_email)}`;
    }

    document.getElementById("project-form").addEventListener("submit", async (event) => {
      event.preventDefault();
      const error = document.getElementById("project-error");
      error.style.display = "none";
      try {
        const project = await api("/api/project", formData(event.target));
        document.getElementById("project-output").innerHTML = renderPackage(project);
        loadRecent();
        toast("Project package generated");
      } catch (err) {
        error.textContent = err.message;
        error.style.display = "block";
      }
    });

    document.getElementById("quote-form").addEventListener("submit", async (event) => {
      event.preventDefault();
      const result = await api("/api/quote", formData(event.target));
      document.getElementById("quote-output").innerHTML = outputBlock("Quote", result);
      toast("Quote generated");
    });

    document.getElementById("payment-form").addEventListener("submit", async (event) => {
      event.preventDefault();
      const result = await api("/api/payment", formData(event.target));
      document.getElementById("payment-output").innerHTML = outputBlock("Payment Breakdown", result);
      toast("Payment generated");
    });

    document.getElementById("checklist-form").addEventListener("submit", async (event) => {
      event.preventDefault();
      const result = await api("/api/checklist", formData(event.target));
      document.getElementById("checklist-output").innerHTML = outputBlock("Checklist", result);
      toast("Checklist generated");
    });

    document.getElementById("load-services").addEventListener("click", async () => {
      const result = await api("/api/services");
      document.getElementById("services-output").innerHTML = outputBlock("Services", result);
      toast("Services loaded");
    });

    document.getElementById("refresh-recent").addEventListener("click", loadRecent);

    function closeOnboarding() {
      document.getElementById("onboarding-modal").classList.remove("show");
      document.body.classList.remove("onboarding-open");
      localStorage.setItem("creativeStudioOnboardingDone", "true");
    }

    document.getElementById("dismiss-onboarding").addEventListener("click", () => {
      document.getElementById("onboarding-card").style.display = "none";
      localStorage.setItem("creativeStudioOnboardingDone", "true");
    });

    document.getElementById("skip-onboarding").addEventListener("click", closeOnboarding);
    document.getElementById("start-onboarding").addEventListener("click", () => {
      closeOnboarding();
      showView("settings");
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeOnboarding();
    });

    loadProfile().then(() => {
      loadRecent();
      if (!localStorage.getItem("creativeStudioOnboardingDone")) {
        document.getElementById("onboarding-modal").classList.add("show");
        document.body.classList.add("onboarding-open");
      } else {
        document.getElementById("onboarding-card").style.display = "none";
      }
    });
  </script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def _send(self, status, content, content_type="application/json"):
        body = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, HTML, "text/html")
        else:
            self._send(404, "Not found", "text/plain")

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            payload = json.loads(raw or "{}")

            if self.path == "/api/profile":
                result = get_brand_profile()
            elif self.path == "/api/save-profile":
                services = parse_services_text(payload.get("services_text", ""))
                payload["services"] = services
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
            else:
                self._send(404, json.dumps({"error": "Unknown action"}))
                return

            self._send(200, json.dumps({"result": result}))
        except Exception as exc:
            self._send(400, json.dumps({"error": str(exc)}))


def find_port(start=8765, end=8790):
    for port in range(start, end + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError("No free local port found")


def main():
    port = find_port()
    url = f"http://127.0.0.1:{port}"
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    print()
    print("Creative Studio MCP is running.")
    print(f"Open this link if the browser does not open: {url}")
    print()
    print("Keep this window open while using the app.")
    print("Press Ctrl+C to stop.")
    print()
    server.serve_forever()


if __name__ == "__main__":
    main()
