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
    save_brand_profile,
    save_project,
)

HTML = '<!doctype html>\n<html lang="en">\n<head>\n  <meta charset="utf-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1">\n  <title>Creative Studio MCP</title>\n  <style>\n    :root {\n      --bg: #f7f8f5;\n      --surface: #ffffff;\n      --text: #111827;\n      --muted: #6b7280;\n      --line: #e5e7eb;\n      --accent: #1f883d;\n      --accent-soft: #e9f8ee;\n      --danger: #b42318;\n      --shadow: 0 12px 30px rgba(17, 24, 39, .08);\n      font-family: Arial, Helvetica, sans-serif;\n    }\n    * { box-sizing: border-box; }\n    body { margin: 0; background: var(--bg); color: var(--text); line-height: 1.5; }\n    button, input, select { font: inherit; }\n    button { cursor: pointer; }\n    .app { max-width: 1100px; margin: 0 auto; padding: 24px; }\n    header { display: flex; align-items: center; justify-content: space-between; gap: 16px; margin-bottom: 22px; }\n    .brand { display: flex; align-items: center; gap: 12px; }\n    .logo { width: 42px; height: 42px; border-radius: 12px; background: var(--accent); color: white; display: grid; place-items: center; font-weight: 900; }\n    h1, h2, h3 { margin: 0; line-height: 1.15; }\n    h1 { font-size: clamp(30px, 5vw, 48px); letter-spacing: -0.02em; }\n    p { margin: 6px 0 0; color: var(--muted); }\n    .grid { display: grid; grid-template-columns: minmax(0, 1fr) 360px; gap: 18px; align-items: start; }\n    .card { background: var(--surface); border: 1px solid var(--line); border-radius: 18px; box-shadow: 0 1px 2px rgba(17,24,39,.04); padding: 20px; }\n    .hero { margin-bottom: 18px; }\n    form { display: grid; gap: 16px; margin-top: 18px; }\n    .fields { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }\n    label { display: grid; gap: 7px; font-weight: 800; }\n    small { color: var(--muted); font-weight: 400; }\n    input, select { min-height: 48px; border: 1px solid var(--line); border-radius: 12px; padding: 0 13px; background: white; color: var(--text); }\n    input:focus, select:focus, button:focus-visible { outline: 3px solid rgba(31,136,61,.22); outline-offset: 2px; border-color: var(--accent); }\n    .actions { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }\n    .btn { min-height: 48px; border-radius: 12px; border: 1px solid var(--line); background: white; color: var(--text); padding: 0 16px; font-weight: 800; transition: transform .18s ease, box-shadow .18s ease, background .18s ease; }\n    .btn:hover { transform: translateY(-1px); box-shadow: var(--shadow); }\n    .btn:active { transform: scale(.98); }\n    .btn.primary { background: var(--accent); color: white; border-color: var(--accent); }\n    .btn.danger { color: var(--danger); background: #fff7f7; }\n    .btn[disabled] { opacity: .65; pointer-events: none; }\n    .loader { display: flex; gap: 12px; align-items: center; padding: 16px; border: 1px solid var(--line); border-radius: 14px; background: var(--accent-soft); margin-top: 16px; }\n    .spinner { width: 20px; height: 20px; border-radius: 999px; border: 3px solid rgba(31,136,61,.22); border-top-color: var(--accent); animation: spin .8s linear infinite; flex: 0 0 auto; }\n    .message { padding: 14px 16px; border-radius: 14px; border: 1px solid var(--line); background: #fbfcfb; margin-top: 16px; }\n    .message.error { color: var(--danger); background: #fff7f7; border-color: #ffd1d1; }\n    .results { display: grid; gap: 14px; margin-top: 18px; }\n    .section { border: 1px solid var(--line); border-radius: 16px; padding: 16px; background: #fbfcfb; }\n    .section-head { display: flex; justify-content: space-between; gap: 10px; align-items: center; margin-bottom: 10px; }\n    pre { margin: 0; white-space: pre-wrap; word-break: break-word; font: 13px/1.6 Consolas, monospace; background: #0b120d; color: #ecfff0; padding: 14px; border-radius: 12px; }\n    .preview { position: sticky; top: 18px; }\n    .status { display: inline-flex; align-items: center; gap: 8px; padding: 8px 10px; background: var(--accent-soft); color: var(--accent); border-radius: 999px; font-weight: 800; font-size: 13px; }\n    .toast { position: fixed; right: 20px; bottom: 20px; max-width: 380px; background: #111827; color: white; padding: 14px 16px; border-radius: 14px; box-shadow: var(--shadow); opacity: 0; transform: translateY(8px); transition: opacity .2s ease, transform .2s ease; z-index: 50; }\n    .toast.show { opacity: 1; transform: translateY(0); }\n    .muted-box { border: 1px dashed #d1d5db; border-radius: 16px; padding: 18px; color: var(--muted); background: #fbfcfb; }\n    footer { margin-top: 18px; color: var(--muted); font-size: 14px; }\n    @keyframes spin { to { transform: rotate(360deg); } }\n    @media (max-width: 850px) {\n      .grid, .fields { grid-template-columns: 1fr; }\n      .preview { position: static; }\n      header { align-items: flex-start; flex-direction: column; }\n    }\n    @media (prefers-reduced-motion: reduce) {\n      *, *::before, *::after { animation-duration: .001ms !important; transition-duration: .001ms !important; scroll-behavior: auto !important; }\n    }\n  </style>\n</head>\n<body>\n  <main class="app">\n    <header>\n      <div class="brand">\n        <div class="logo">CS</div>\n        <div>\n          <strong>Creative Studio MCP</strong>\n          <p>Minimal local project tool</p>\n        </div>\n      </div>\n      <span class="status">Local app ready</span>\n    </header>\n\n    <section class="hero">\n      <h1>Create a project package.</h1>\n      <p>Generate a quote, payment breakdown, checklist, deliverables, and client email.</p>\n    </section>\n\n    <div class="grid">\n      <section class="card">\n        <h2>New Project</h2>\n        <p>Fill the basics and click Generate.</p>\n        <form id="projectForm">\n          <div class="fields">\n            <label>Client name\n              <input name="client_name" value="Israel Thomas" required>\n              <small>Who is this for?</small>\n            </label>\n            <label>Service\n              <select name="service" id="service"></select>\n              <small>Your saved services appear here.</small>\n            </label>\n            <label>Design fee\n              <input name="design_fee" type="number" min="1" value="3000" required>\n              <small>Numbers only.</small>\n            </label>\n            <label>Upfront percent\n              <input name="upfront_percent" type="number" min="0" max="100" value="70" required>\n              <small>Example: 70.</small>\n            </label>\n            <label>Project type\n              <input name="project_type" value="Brand Identity Design" required>\n              <small>Used for the checklist.</small>\n            </label>\n          </div>\n          <div class="actions">\n            <button class="btn primary" id="generateBtn" type="submit">Generate</button>\n            <button class="btn" id="clearBtn" type="button">Clear</button>\n          </div>\n        </form>\n        <div id="output" aria-live="polite"></div>\n      </section>\n\n      <aside class="card preview">\n        <div class="section-head">\n          <div>\n            <h2>Preview</h2>\n            <p>Your result appears here.</p>\n          </div>\n          <button class="btn" id="copyAllBtn" type="button">Copy</button>\n        </div>\n        <div id="preview" class="muted-box">Nothing generated yet.</div>\n      </aside>\n    </div>\n\n    <footer>\n      Creative Studio MCP v1.0.0. Built by Thomas Ogun under Senseiglobal.\n    </footer>\n  </main>\n  <div id="toast" class="toast" role="status" aria-live="polite"></div>\n\n  <script>\n    const $ = (selector) => document.querySelector(selector);\n    let lastProject = null;\n    let lastText = "";\n\n    function toast(message) {\n      const box = $("#toast");\n      box.textContent = message;\n      box.classList.add("show");\n      clearTimeout(window.toastTimer);\n      window.toastTimer = setTimeout(() => box.classList.remove("show"), 2400);\n    }\n\n    function escapeHtml(value) {\n      return String(value ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");\n    }\n\n    function textOf(value) {\n      if (typeof value === "string") return value;\n      if (Array.isArray(value)) return value.map((item, index) => `${index + 1}. ${item}`).join("\\\\n");\n      if (value && typeof value === "object") return Object.entries(value).map(([key, item]) => `${key}: ${item}`).join("\\\\n");\n      return String(value ?? "");\n    }\n\n    async function api(path, payload = {}) {\n      const response = await fetch(path, {\n        method: "POST",\n        headers: { "Content-Type": "application/json" },\n        body: JSON.stringify(payload)\n      });\n      let data = {};\n      try {\n        data = await response.json();\n      } catch (error) {\n        throw new Error("The app returned an unreadable response.");\n      }\n      if (!response.ok || data.error) throw new Error(data.error || "Request failed.");\n      return data.result;\n    }\n\n    function validate(payload) {\n      const fee = Number(payload.design_fee);\n      const upfront = Number(payload.upfront_percent);\n      if (!String(payload.client_name || "").trim()) return "Please enter the client name.";\n      if (!String(payload.service || "").trim()) return "Please choose a service.";\n      if (!String(payload.project_type || "").trim()) return "Please enter the project type.";\n      if (!Number.isFinite(fee) || fee <= 0) return "Design fee must be above 0.";\n      if (!Number.isFinite(upfront) || upfront < 0 || upfront > 100) return "Upfront percent must be between 0 and 100.";\n      return "";\n    }\n\n    function block(title, value) {\n      const text = textOf(value);\n      return `<section class="section">\n        <div class="section-head">\n          <h3>${escapeHtml(title)}</h3>\n          <button class="btn" type="button" data-copy="${encodeURIComponent(text)}">Copy</button>\n        </div>\n        <pre>${escapeHtml(text)}</pre>\n      </section>`;\n    }\n\n    function render(project) {\n      const pkg = project.generated_package || {};\n      lastProject = project;\n      lastText = [\n        "CLIENT QUOTE", textOf(pkg.client_quote), "",\n        "PAYMENT", textOf(pkg.payment_breakdown), "",\n        "CHECKLIST", textOf(pkg.project_checklist), "",\n        "DELIVERABLES", textOf(pkg.deliverables), "",\n        "EMAIL", textOf(pkg.client_email)\n      ].join("\\\\n");\n      const actions = `<div class="actions">\n        <button class="btn primary" type="button" data-copy="${encodeURIComponent(lastText)}">Copy Full Package</button>\n        <button class="btn" type="button" data-export="txt">Export TXT</button>\n        <button class="btn" type="button" data-export="md">Export MD</button>\n      </div>`;\n      const html = actions\n        + block("Client Quote", pkg.client_quote)\n        + block("Payment Breakdown", pkg.payment_breakdown)\n        + block("Project Checklist", pkg.project_checklist)\n        + block("Deliverables", pkg.deliverables)\n        + block("Client Email", pkg.client_email);\n      $("#output").innerHTML = `<div class="message"><strong>Generated successfully.</strong><p>Review, copy, or export below.</p></div><div class="results">${html}</div>`;\n      $("#preview").className = "results";\n      $("#preview").innerHTML = html;\n      $("#output").scrollIntoView({ behavior: "smooth", block: "start" });\n    }\n\n    async function loadServices() {\n      try {\n        const services = await api("/api/services");\n        const names = Object.keys(services);\n        $("#service").innerHTML = names.map((name) => `<option>${escapeHtml(name)}</option>`).join("");\n      } catch (error) {\n        $("#service").innerHTML = "<option>Brand Identity Design</option>";\n      }\n    }\n\n    $("#projectForm").addEventListener("submit", async (event) => {\n      event.preventDefault();\n      const button = $("#generateBtn");\n      const payload = Object.fromEntries(new FormData(event.currentTarget).entries());\n      const error = validate(payload);\n      if (error) {\n        $("#output").innerHTML = `<div class="message error">${escapeHtml(error)}</div>`;\n        toast(error);\n        return;\n      }\n      button.disabled = true;\n      $("#output").innerHTML = `<div class="loader"><span class="spinner"></span><div><strong>Generating...</strong><p>Your project package will show here.</p></div></div>`;\n      try {\n        const project = await api("/api/project", payload);\n        render(project);\n        toast("Project generated.");\n      } catch (error) {\n        $("#output").innerHTML = `<div class="message error"><strong>Generate failed.</strong><p>${escapeHtml(error.message)}</p></div>`;\n        toast("Generate failed.");\n      } finally {\n        button.disabled = false;\n      }\n    });\n\n    $("#clearBtn").addEventListener("click", () => {\n      $("#output").innerHTML = "";\n      $("#preview").className = "muted-box";\n      $("#preview").textContent = "Nothing generated yet.";\n      lastProject = null;\n      lastText = "";\n    });\n\n    $("#copyAllBtn").addEventListener("click", async () => {\n      if (!lastText) {\n        toast("Generate first.");\n        return;\n      }\n      await navigator.clipboard.writeText(lastText);\n      toast("Copied.");\n    });\n\n    document.addEventListener("click", async (event) => {\n      const copy = event.target.closest("[data-copy]");\n      if (copy) {\n        await navigator.clipboard.writeText(decodeURIComponent(copy.dataset.copy));\n        toast("Copied.");\n        return;\n      }\n      const exportButton = event.target.closest("[data-export]");\n      if (exportButton) {\n        if (!lastProject) {\n          toast("Generate first.");\n          return;\n        }\n        try {\n          const result = await api("/api/export", { project_id: lastProject.id, file_format: exportButton.dataset.export });\n          toast(`Saved: ${result.file_name || "export file"}`);\n        } catch (error) {\n          toast("Export failed.");\n        }\n      }\n    });\n\n    loadServices();\n  </script>\n</body>\n</html>'

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

    def read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        if not length:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.send_text(200, HTML, "text/html")
        else:
            self.send_text(404, "Not found", "text/plain")

    def do_POST(self):
        try:
            payload = self.read_json()
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
