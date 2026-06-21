import json
import socket
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from business_tools import (
    calculate_payment,
    create_quote,
    generate_project_checklist,
    list_services,
)


HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Creative Studio MCP</title>
  <style>
    :root {
      --bg: #f6f7f2;
      --ink: #152016;
      --muted: #5e685f;
      --line: #d8dfd7;
      --panel: #ffffff;
      --green: #1f883d;
      --green-dark: #15602a;
      --gold: #d99a22;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Arial, Helvetica, sans-serif;
      line-height: 1.45;
    }

    main {
      width: min(1080px, calc(100% - 28px));
      margin: 0 auto;
      padding: 28px 0 40px;
    }

    header,
    section,
    .tool,
    .output {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }

    header {
      padding: 24px;
      margin-bottom: 16px;
    }

    h1,
    h2,
    h3 {
      margin: 0;
      letter-spacing: 0;
    }

    h1 { font-size: 32px; }
    h2 { font-size: 22px; }
    h3 { font-size: 18px; }

    p {
      margin: 8px 0 0;
      color: var(--muted);
    }

    .grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }

    .tool {
      padding: 18px;
    }

    label {
      display: block;
      margin-top: 12px;
      font-weight: 700;
      color: var(--ink);
    }

    input,
    select {
      width: 100%;
      min-height: 42px;
      margin-top: 6px;
      padding: 9px 10px;
      border: 1px solid var(--line);
      border-radius: 6px;
      font: inherit;
      background: #fff;
      color: var(--ink);
    }

    .row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }

    button {
      min-height: 42px;
      margin-top: 14px;
      padding: 0 14px;
      border: 1px solid var(--green);
      border-radius: 6px;
      background: var(--green);
      color: #fff;
      font: inherit;
      font-weight: 700;
      cursor: pointer;
    }

    button:hover { background: var(--green-dark); }

    button.secondary {
      background: #fff;
      color: var(--green-dark);
      border-color: var(--line);
    }

    .output {
      margin-top: 16px;
      padding: 18px;
    }

    pre {
      white-space: pre-wrap;
      word-break: break-word;
      margin: 12px 0 0;
      padding: 14px;
      border-radius: 6px;
      background: #111827;
      color: #f9fafb;
      font-family: Consolas, Monaco, monospace;
      font-size: 15px;
    }

    .notice {
      padding: 12px 14px;
      margin-top: 12px;
      border-radius: 6px;
      border-left: 5px solid var(--gold);
      background: #fff8e6;
      color: var(--ink);
    }

    @media (max-width: 820px) {
      h1 { font-size: 27px; }
      .grid,
      .row { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <main>
    <header>
      <h1>Creative Studio MCP</h1>
      <p>Create quotes, payment breakdowns, service lists, and project checklists without connecting Claude first.</p>
      <div class="notice">This local app works on its own. Claude and OpenAI are optional extra connections.</div>
    </header>

    <div class="grid">
      <section class="tool">
        <h2>Services</h2>
        <p>Show the creative services and price ranges.</p>
        <button type="button" data-action="services">List Services</button>
      </section>

      <section class="tool">
        <h2>Payment</h2>
        <div class="row">
          <label>Total fee
            <input id="payment-total" type="number" min="0" value="5000">
          </label>
          <label>Upfront percent
            <input id="payment-percent" type="number" min="0" max="100" value="70">
          </label>
        </div>
        <button type="button" data-action="payment">Calculate Payment</button>
      </section>

      <section class="tool">
        <h2>Quote</h2>
        <label>Client name
          <input id="quote-client" value="John Smith">
        </label>
        <label>Service
          <select id="quote-service"></select>
        </label>
        <label>Design fee
          <input id="quote-fee" type="number" min="0" value="3000">
        </label>
        <button type="button" data-action="quote">Create Quote</button>
      </section>

      <section class="tool">
        <h2>Checklist</h2>
        <label>Project type
          <input id="checklist-type" value="Product packaging design">
        </label>
        <button type="button" data-action="checklist">Create Checklist</button>
      </section>
    </div>

    <section class="output">
      <h2>Result</h2>
      <p>Your result will appear here.</p>
      <pre id="result">Click a button to start.</pre>
      <button class="secondary" type="button" id="copy">Copy Result</button>
    </section>
  </main>

  <script>
    const result = document.getElementById("result");
    const serviceSelect = document.getElementById("quote-service");

    function show(value) {
      if (typeof value === "string") {
        result.textContent = value;
        return;
      }
      if (Array.isArray(value)) {
        result.textContent = value.map((item, index) => `${index + 1}. ${item}`).join("\n");
        return;
      }
      result.textContent = Object.entries(value)
        .map(([key, item]) => `${key}: ${item}`)
        .join("\n");
    }

    async function post(path, payload) {
      const response = await fetch(path, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload || {})
      });
      if (!response.ok) {
        throw new Error("Request failed");
      }
      return response.json();
    }

    async function loadServices() {
      const data = await post("/api/services");
      serviceSelect.innerHTML = "";
      Object.keys(data.result).forEach((name) => {
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        serviceSelect.appendChild(option);
      });
    }

    document.querySelectorAll("[data-action]").forEach((button) => {
      button.addEventListener("click", async () => {
        try {
          const action = button.dataset.action;
          if (action === "services") {
            show((await post("/api/services")).result);
          }
          if (action === "payment") {
            show((await post("/api/payment", {
              total_fee: document.getElementById("payment-total").value,
              upfront_percent: document.getElementById("payment-percent").value
            })).result);
          }
          if (action === "quote") {
            show((await post("/api/quote", {
              client_name: document.getElementById("quote-client").value,
              service: document.getElementById("quote-service").value,
              design_fee: document.getElementById("quote-fee").value
            })).result);
          }
          if (action === "checklist") {
            show((await post("/api/checklist", {
              project_type: document.getElementById("checklist-type").value
            })).result);
          }
        } catch (error) {
          result.textContent = "Something went wrong. Close this window and double-click START_APP.bat again.";
        }
      });
    });

    document.getElementById("copy").addEventListener("click", async () => {
      await navigator.clipboard.writeText(result.textContent);
    });

    loadServices().catch(() => {
      result.textContent = "The app started, but services could not load.";
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
                    bool(payload.get("includes_printing", False)),
                )
            elif self.path == "/api/checklist":
                result = generate_project_checklist(payload.get("project_type", ""))
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
