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
    list_recent_projects,
    list_services,
    save_project,
)


HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Creative Studio MCP</title>
  <style>
    :root {
      --bg: #f5f6f2;
      --ink: #172018;
      --muted: #647067;
      --line: #d8dfd7;
      --panel: #ffffff;
      --soft: #eef4ef;
      --green: #1f883d;
      --green-dark: #155f2b;
      --gold: #d99a22;
      --dark: #111827;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Arial, Helvetica, sans-serif;
      line-height: 1.45;
    }

    .shell {
      min-height: 100vh;
      display: grid;
      grid-template-columns: 260px 1fr;
    }

    aside {
      background: #162117;
      color: #fff;
      padding: 22px;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 24px;
    }

    .logo {
      width: 42px;
      height: 42px;
      display: grid;
      place-items: center;
      border-radius: 8px;
      background: var(--green);
      font-weight: 800;
    }

    nav button {
      width: 100%;
      min-height: 42px;
      margin-bottom: 8px;
      border: 1px solid rgba(255,255,255,.12);
      border-radius: 6px;
      background: transparent;
      color: #fff;
      font: inherit;
      text-align: left;
      padding: 0 12px;
      cursor: pointer;
    }

    nav button.active,
    nav button:hover {
      background: rgba(255,255,255,.12);
    }

    main {
      padding: 28px;
      overflow: auto;
    }

    h1, h2, h3 {
      margin: 0;
      letter-spacing: 0;
    }

    h1 { font-size: 34px; }
    h2 { font-size: 23px; }
    h3 { font-size: 18px; }

    p {
      margin: 7px 0 0;
      color: var(--muted);
    }

    .topbar {
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: center;
      margin-bottom: 18px;
    }

    .primary {
      min-height: 44px;
      padding: 0 16px;
      border-radius: 6px;
      border: 1px solid var(--green);
      background: var(--green);
      color: #fff;
      font: inherit;
      font-weight: 700;
      cursor: pointer;
    }

    .primary:hover { background: var(--green-dark); }

    .secondary {
      min-height: 38px;
      padding: 0 12px;
      border-radius: 6px;
      border: 1px solid var(--line);
      background: #fff;
      color: var(--green-dark);
      font: inherit;
      font-weight: 700;
      cursor: pointer;
    }

    .grid,
    .actions {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
    }

    .panel,
    .card,
    .output {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }

    .panel {
      padding: 20px;
      margin-bottom: 16px;
    }

    .card {
      padding: 18px;
      cursor: pointer;
      min-height: 132px;
    }

    .card:hover {
      border-color: var(--green);
      box-shadow: 0 8px 24px rgba(21, 95, 43, .08);
    }

    .section {
      display: none;
    }

    .section.active {
      display: block;
    }

    form {
      display: grid;
      gap: 12px;
      margin-top: 14px;
    }

    .form-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
    }

    label {
      display: block;
      font-weight: 700;
    }

    small {
      display: block;
      margin-top: 4px;
      color: var(--muted);
      font-weight: 400;
    }

    input,
    select {
      width: 100%;
      min-height: 42px;
      margin-top: 6px;
      padding: 9px 10px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fff;
      color: var(--ink);
      font: inherit;
    }

    .output {
      margin-top: 14px;
      padding: 16px;
    }

    .output-head {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
    }

    pre {
      margin: 12px 0 0;
      padding: 14px;
      border-radius: 6px;
      background: var(--dark);
      color: #f9fafb;
      white-space: pre-wrap;
      word-break: break-word;
      font-family: Consolas, Monaco, monospace;
      font-size: 14px;
    }

    .package {
      display: grid;
      gap: 14px;
      margin-top: 16px;
    }

    .recent {
      display: grid;
      gap: 10px;
      margin-top: 12px;
    }

    .recent-item {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 12px;
      align-items: center;
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
    }

    .empty {
      padding: 18px;
      border-radius: 8px;
      background: var(--soft);
      color: var(--muted);
    }

    .error {
      margin-top: 12px;
      padding: 12px;
      border-radius: 6px;
      background: #fff1f1;
      color: #9f1d1d;
      border: 1px solid #f2c4c4;
      display: none;
    }

    @media (max-width: 980px) {
      .shell { grid-template-columns: 1fr; }
      aside { position: static; }
      .grid,
      .actions,
      .form-grid { grid-template-columns: 1fr; }
      .topbar { align-items: flex-start; flex-direction: column; }
    }
  </style>
</head>
<body>
  <div class="shell">
    <aside>
      <div class="brand">
        <div class="logo">CS</div>
        <div>
          <strong>Creative Studio MCP</strong>
          <p>Daily business workspace</p>
        </div>
      </div>
      <nav>
        <button class="active" type="button" data-view="home">Home</button>
        <button type="button" data-view="new-project">New Project</button>
        <button type="button" data-view="quote">Quote</button>
        <button type="button" data-view="payment">Payment Breakdown</button>
        <button type="button" data-view="checklist">Project Checklist</button>
        <button type="button" data-view="services">Service List</button>
      </nav>
    </aside>

    <main>
      <section id="home" class="section active">
        <div class="topbar">
          <div>
            <h1>Creative Studio MCP</h1>
            <p>Create quotes, payment breakdowns, checklists, and complete project packages.</p>
          </div>
          <button class="primary" type="button" data-view="new-project">New Project</button>
        </div>

        <div class="actions">
          <article class="card" data-view="quote">
            <h3>Quote</h3>
            <p>Create a client-ready quote.</p>
          </article>
          <article class="card" data-view="payment">
            <h3>Payment Breakdown</h3>
            <p>Calculate upfront and balance payments.</p>
          </article>
          <article class="card" data-view="checklist">
            <h3>Project Checklist</h3>
            <p>Build a simple project task list.</p>
          </article>
          <article class="card" data-view="services">
            <h3>Service List</h3>
            <p>View services and price ranges.</p>
          </article>
        </div>

        <div class="panel" style="margin-top:16px">
          <div class="topbar">
            <div>
              <h2>Recent Projects</h2>
              <p>Saved locally in projects.json.</p>
            </div>
            <button class="secondary" type="button" id="refresh-recent">Refresh</button>
          </div>
          <div id="recent" class="recent"></div>
        </div>
      </section>

      <section id="new-project" class="section">
        <div class="topbar">
          <div>
            <h1>New Project</h1>
            <p>Fill this once and generate a full project package.</p>
          </div>
        </div>
        <div class="panel">
          <form id="project-form">
            <div class="form-grid">
              <label>Client name
                <input name="client_name" value="John Smith" required>
                <small>Who is this project for?</small>
              </label>
              <label>Service
                <select name="service" id="project-service"></select>
                <small>Pick the main service.</small>
              </label>
              <label>Design fee
                <input name="design_fee" type="number" min="1" value="3000" required>
                <small>Use numbers only.</small>
              </label>
              <label>Upfront percent
                <input name="upfront_percent" type="number" min="0" max="100" value="70" required>
                <small>Example: 70 means 70% upfront.</small>
              </label>
              <label>Project type
                <input name="project_type" value="Brand identity project" required>
                <small>Example: packaging, branding, profile design.</small>
              </label>
            </div>
            <button class="primary" type="submit">Generate Project Package</button>
            <div id="project-error" class="error"></div>
          </form>
          <div id="project-output" class="package"></div>
        </div>
      </section>

      <section id="quote" class="section">
        <h1>Quote</h1>
        <div class="panel">
          <form id="quote-form">
            <div class="form-grid">
              <label>Client name <input name="client_name" value="John Smith" required></label>
              <label>Service <select name="service" id="quote-service"></select></label>
              <label>Design fee <input name="design_fee" type="number" min="1" value="3000" required></label>
            </div>
            <button class="primary" type="submit">Create Quote</button>
          </form>
          <div id="quote-output"></div>
        </div>
      </section>

      <section id="payment" class="section">
        <h1>Payment Breakdown</h1>
        <div class="panel">
          <form id="payment-form">
            <div class="form-grid">
              <label>Total fee <input name="total_fee" type="number" min="1" value="5000" required></label>
              <label>Upfront percent <input name="upfront_percent" type="number" min="0" max="100" value="70" required></label>
            </div>
            <button class="primary" type="submit">Calculate</button>
          </form>
          <div id="payment-output"></div>
        </div>
      </section>

      <section id="checklist" class="section">
        <h1>Project Checklist</h1>
        <div class="panel">
          <form id="checklist-form">
            <label>Project type <input name="project_type" value="Product packaging design" required></label>
            <button class="primary" type="submit">Create Checklist</button>
          </form>
          <div id="checklist-output"></div>
        </div>
      </section>

      <section id="services" class="section">
        <h1>Service List</h1>
        <div class="panel">
          <button class="primary" type="button" id="load-services">Show Services</button>
          <div id="services-output"></div>
        </div>
      </section>
    </main>
  </div>

  <script>
    const state = { services: {} };

    function showView(id) {
      document.querySelectorAll(".section").forEach((item) => item.classList.remove("active"));
      document.querySelectorAll("nav button").forEach((item) => item.classList.remove("active"));
      document.getElementById(id).classList.add("active");
      document.querySelectorAll(`[data-view="${id}"]`).forEach((item) => {
        if (item.tagName === "BUTTON") item.classList.add("active");
      });
      if (id === "home") loadRecent();
    }

    document.querySelectorAll("[data-view]").forEach((item) => {
      item.addEventListener("click", () => showView(item.dataset.view));
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

    function outputBlock(title, value) {
      const text = asText(value);
      return `<div class="output">
        <div class="output-head">
          <h3>${title}</h3>
          <button class="secondary" type="button" data-copy="${encodeURIComponent(text)}">Copy</button>
        </div>
        <pre>${escapeHtml(text)}</pre>
      </div>`;
    }

    function escapeHtml(text) {
      return String(text)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;");
    }

    document.addEventListener("click", async (event) => {
      const button = event.target.closest("[data-copy]");
      if (!button) return;
      await navigator.clipboard.writeText(decodeURIComponent(button.dataset.copy));
      button.textContent = "Copied";
      setTimeout(() => button.textContent = "Copy", 1200);
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

    async function loadRecent() {
      const target = document.getElementById("recent");
      const projects = await api("/api/recent", { limit: 8 });
      if (!projects.length) {
        target.innerHTML = `<div class="empty">No saved projects yet. Create one from New Project.</div>`;
        return;
      }
      target.innerHTML = projects.map((project) => `
        <div class="recent-item">
          <div>
            <strong>${escapeHtml(project.client_name)}</strong>
            <p>${escapeHtml(project.service)} at $${Number(project.design_fee).toLocaleString()}</p>
          </div>
          <button class="secondary" type="button" data-copy="${encodeURIComponent(asText(project.generated_package.client_quote))}">Copy Quote</button>
        </div>
      `).join("");
    }

    function renderPackage(project) {
      const pkg = project.generated_package;
      const full = [
        "CLIENT QUOTE",
        asText(pkg.client_quote),
        "",
        "PAYMENT BREAKDOWN",
        asText(pkg.payment_breakdown),
        "",
        "PROJECT CHECKLIST",
        asText(pkg.project_checklist),
        "",
        "DELIVERABLES",
        asText(pkg.deliverables),
        "",
        "CLIENT EMAIL",
        asText(pkg.client_email),
      ].join("\n");

      return `<div class="output">
        <div class="output-head">
          <h3>Full Project Package</h3>
          <button class="primary" type="button" data-copy="${encodeURIComponent(full)}">Copy Full Package</button>
        </div>
      </div>
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
      } catch (err) {
        error.textContent = err.message;
        error.style.display = "block";
      }
    });

    document.getElementById("quote-form").addEventListener("submit", async (event) => {
      event.preventDefault();
      const result = await api("/api/quote", formData(event.target));
      document.getElementById("quote-output").innerHTML = outputBlock("Quote", result);
    });

    document.getElementById("payment-form").addEventListener("submit", async (event) => {
      event.preventDefault();
      const result = await api("/api/payment", formData(event.target));
      document.getElementById("payment-output").innerHTML = outputBlock("Payment Breakdown", result);
    });

    document.getElementById("checklist-form").addEventListener("submit", async (event) => {
      event.preventDefault();
      const result = await api("/api/checklist", formData(event.target));
      document.getElementById("checklist-output").innerHTML = outputBlock("Checklist", result);
    });

    document.getElementById("load-services").addEventListener("click", async () => {
      const result = await api("/api/services");
      document.getElementById("services-output").innerHTML = outputBlock("Services", result);
    });

    document.getElementById("refresh-recent").addEventListener("click", loadRecent);

    loadServices().then(loadRecent);
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

            if self.path == "/api/services":
                result = list_services()
            elif self.path == "/api/payment":
                result = calculate_payment(
                    payload.get("total_fee", 0),
                    payload.get("upfront_percent", 70),
                )
            elif self.path == "/api/quote":
                result = create_quote(
                    payload.get("client_name", ""),
                    payload.get("service", ""),
                    payload.get("design_fee", 0),
                )
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
