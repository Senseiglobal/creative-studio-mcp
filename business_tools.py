import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

BASE_DIR = Path(__file__).resolve().parent
PROJECTS_FILE = BASE_DIR / "projects.json"
DELETED_PROJECTS_FILE = BASE_DIR / "deleted_projects.json"
BRAND_PROFILE_FILE = BASE_DIR / "brand_profile.json"
EXPORTS_DIR = BASE_DIR / "exports"
DELETED_PROJECT_LIMIT = 100

DEFAULT_SERVICES = {
    "Brand Identity Design": "$500 to $2,500+",
    "Product Packaging Design": "$400 to $1,500+",
    "Corporate Profile Design": "$300 to $1,200+",
    "Proposal / Presentation Design": "$150 to $700+",
    "Merchandise Design": "$250 to $1,000+",
    "Banner & Event Visual Design": "$50 to $500+",
}

DEFAULT_PROFILE = {
    "business_name": "Senseiglobal Creative Studio",
    "owner_name": "",
    "email": "",
    "phone": "",
    "website": "",
    "location": "",
    "brand_voice": "Professional, clear, friendly, and confident.",
    "payment_terms": "70% upfront before project commencement. 30% balance before final delivery.",
    "currency": "USD",
    "services": DEFAULT_SERVICES,
}

def ensure_json(path, default):
    if not path.exists():
        path.write_text(json.dumps(default, indent=2), encoding="utf-8")

def read_json(path, default):
    ensure_json(path, default)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        value = default
    return value

def write_json(path, value):
    path.write_text(json.dumps(value, indent=2), encoding="utf-8")

def format_currency(value, currency=None):
    amount = int(float(value))
    symbol = "$" if (currency or "USD").upper() == "USD" else f"{currency} "
    return f"{symbol}{amount:,}"

def get_brand_profile():
    data = read_json(BRAND_PROFILE_FILE, DEFAULT_PROFILE)
    profile = dict(DEFAULT_PROFILE)
    if isinstance(data, dict):
        profile.update(data)
    if not isinstance(profile.get("services"), dict) or not profile["services"]:
        profile["services"] = dict(DEFAULT_SERVICES)
    return profile

def save_brand_profile(profile):
    current = get_brand_profile()
    cleaned = dict(current)
    for key in ["business_name", "owner_name", "email", "phone", "website", "location", "brand_voice", "payment_terms", "currency"]:
        if key in profile:
            cleaned[key] = str(profile.get(key, "")).strip()
    services = profile.get("services")
    if isinstance(services, dict):
        cleaned["services"] = {str(k).strip(): str(v).strip() for k, v in services.items() if str(k).strip() and str(v).strip()} or dict(DEFAULT_SERVICES)
    write_json(BRAND_PROFILE_FILE, cleaned)
    return cleaned

def parse_services_text(text):
    services = {}
    for raw in (text or "").splitlines():
        line = raw.strip()
        if not line:
            continue
        if "|" in line:
            name, price = line.split("|", 1)
        elif ":" in line:
            name, price = line.split(":", 1)
        else:
            continue
        if name.strip() and price.strip():
            services[name.strip()] = price.strip()
    return services

def list_services():
    return dict(get_brand_profile()["services"])

def validate_project_inputs(client_name, service, design_fee, upfront_percent=70, project_type=""):
    client_name = (client_name or "").strip()
    service = (service or "").strip()
    project_type = (project_type or service or "Creative project").strip()
    if not client_name:
        raise ValueError("Client name is required.")
    if not service:
        raise ValueError("Service is required.")
    try:
        design_fee = int(float(design_fee))
    except (TypeError, ValueError) as exc:
        raise ValueError("Design fee must be a number.") from exc
    try:
        upfront_percent = int(float(upfront_percent))
    except (TypeError, ValueError) as exc:
        raise ValueError("Upfront percent must be a number.") from exc
    if design_fee <= 0:
        raise ValueError("Design fee must be greater than zero.")
    if upfront_percent < 0 or upfront_percent > 100:
        raise ValueError("Upfront percent must be between 0 and 100.")
    return {"client_name": client_name, "service": service, "design_fee": design_fee, "upfront_percent": upfront_percent, "project_type": project_type}

def calculate_payment(total_fee, upfront_percent=70):
    profile = get_brand_profile()
    total_fee = int(float(total_fee))
    upfront_percent = int(float(upfront_percent))
    if total_fee <= 0:
        raise ValueError("Total fee must be greater than zero.")
    if upfront_percent < 0 or upfront_percent > 100:
        raise ValueError("Upfront percent must be between 0 and 100.")
    upfront = round(total_fee * upfront_percent / 100)
    balance = total_fee - upfront
    return {"total_fee": format_currency(total_fee, profile["currency"]), "upfront_percent": f"{upfront_percent}%", "upfront_payment": format_currency(upfront, profile["currency"]), "balance_payment": format_currency(balance, profile["currency"])}

def generate_project_checklist(project_type):
    project_type = (project_type or "Creative project").strip()
    return [f"Confirm project type: {project_type}", "Confirm client brief and brand goals", "Collect logo, references, and content assets", "Define deliverables", "Confirm design direction", "Create first draft", "Review client feedback", "Apply revisions", "Prepare final files", "Confirm printing or production separately if needed"]

def create_deliverables_list(service, project_type=""):
    service = (service or "Creative Service").strip()
    project_type = (project_type or service).strip()
    key = project_type.lower()
    presets = [
        ("brand", ["Logo concepts", "Final logo files", "Color palette", "Typography guide", "Brand usage guide", "Social media profile assets"]),
        ("logo", ["Logo concepts", "Primary logo", "Secondary logo", "Icon or mark", "Black and white version", "Final logo files"]),
        ("packaging", ["Packaging concept", "Front label design", "Back label design", "Print-ready artwork", "Mockup preview", "Production notes"]),
        ("corporate profile", ["Company profile layout", "Cover page design", "About section", "Services section", "Team or leadership section", "PDF-ready final file"]),
        ("proposal", ["Proposal cover", "Project overview pages", "Pricing page", "Timeline page", "Call-to-action page", "Editable presentation file"]),
        ("presentation", ["Presentation cover", "Slide template", "Content slides", "Section divider slides", "Closing slide", "Editable presentation file"]),
        ("merchandise", ["Merchandise concept", "Artwork placement", "Mockup preview", "Color options", "Print-ready files", "Production notes"]),
        ("banner", ["Banner layout", "Event key visual", "Size adaptations", "Print-ready file", "Digital sharing file", "Production notes"]),
        ("event", ["Event key visual", "Banner layout", "Social media announcement", "Directional signage", "Print-ready files", "Digital sharing files"]),
        ("social", ["Post design templates", "Story design templates", "Campaign visual direction", "Editable source files", "Exported image files", "Usage notes"]),
        ("website", ["Homepage concept", "Inner page layout", "Mobile layout", "Asset handoff", "Basic content structure", "Launch-ready design files"]),
    ]
    for needle, deliverables in presets:
        if needle in key:
            return deliverables
    words = [word.capitalize() for word in project_type.replace("/", " ").replace("-", " ").split() if len(word) > 2]
    focus = " ".join(words[:3]) or project_type
    return [f"{focus} concept direction", f"{focus} design draft", "Client review version", "Revision support based on agreed scope", "Final client-ready files", "Basic handover notes"]

def create_quote(client_name, service, design_fee, project_type="", includes_printing=False):
    if isinstance(project_type, bool):
        includes_printing = project_type
        project_type = ""
    profile = get_brand_profile()
    client_name = (client_name or "Client").strip()
    service = (service or "Creative Service").strip()
    project_type = (project_type or service).strip()
    design_fee = int(float(design_fee))
    if design_fee <= 0:
        raise ValueError("Design fee must be greater than zero.")
    printing_note = "Printing or production is included in this quote." if includes_printing else "Printing or production is not included and will be quoted separately after design approval."
    return f"""Hello {client_name},

Thank you for your interest in {profile['business_name']}.

Service: {service}
Project Type: {project_type}
Creative Design Fee: {format_currency(design_fee, profile['currency'])}

Payment Terms:
{profile['payment_terms']}

Note:
{printing_note}

Best regards,
{profile.get('owner_name') or profile.get('business_name', '')}
"""

def create_client_email(client_name, service, design_fee, upfront_percent=70, project_type=""):
    profile = get_brand_profile()
    values = validate_project_inputs(client_name, service, design_fee, upfront_percent, project_type)
    payment = calculate_payment(values["design_fee"], values["upfront_percent"])
    contact = []
    for key, label in [("email", "Email"), ("phone", "Phone"), ("website", "Website")]:
        if profile.get(key):
            contact.append(f"{label}: {profile[key]}")
    contact_text = "\n\n" + "\n".join(contact) if contact else ""
    return f"""Subject: Project Quote For {values['service']}

Hello {values['client_name']},

Thank you for your interest in working with {profile['business_name']}.

I have prepared a quote for {values['service']} at {format_currency(values['design_fee'], profile['currency'])}.

Payment breakdown:
Upfront payment ({payment['upfront_percent']}): {payment['upfront_payment']}
Balance payment: {payment['balance_payment']}

Once approved, we can confirm the brief, timeline, and required files.

Best regards,
{profile.get('owner_name') or profile.get('business_name', '')}
{profile['business_name']}{contact_text}
"""

def create_project_package(client_name, service, design_fee, upfront_percent=70, project_type=""):
    values = validate_project_inputs(client_name, service, design_fee, upfront_percent, project_type)
    return {
        "client_quote": create_quote(values["client_name"], values["service"], values["design_fee"], values["project_type"]),
        "payment_breakdown": calculate_payment(values["design_fee"], values["upfront_percent"]),
        "project_checklist": generate_project_checklist(values["project_type"]),
        "deliverables": create_deliverables_list(values["service"], values["project_type"]),
        "client_email": create_client_email(values["client_name"], values["service"], values["design_fee"], values["upfront_percent"], values["project_type"]),
    }

def _read_projects():
    data = read_json(PROJECTS_FILE, [])
    return data if isinstance(data, list) else []

def _write_projects(projects):
    write_json(PROJECTS_FILE, projects)

def _read_deleted_projects():
    data = read_json(DELETED_PROJECTS_FILE, [])
    return data if isinstance(data, list) else []

def _write_deleted_projects(projects):
    write_json(DELETED_PROJECTS_FILE, projects[:DELETED_PROJECT_LIMIT])

def _trim_deleted_projects(projects):
    kept = projects[:DELETED_PROJECT_LIMIT]
    return kept, max(0, len(projects) - len(kept))

def save_project(client_name, service, design_fee, upfront_percent=70, project_type="", generated_package=None):
    values = validate_project_inputs(client_name, service, design_fee, upfront_percent, project_type)
    package = generated_package or create_project_package(**values)
    project = {"id": str(uuid4()), "created_at": datetime.now(timezone.utc).isoformat(), "client_name": values["client_name"], "service": values["service"], "design_fee": values["design_fee"], "upfront_percent": values["upfront_percent"], "project_type": values["project_type"], "generated_package": package}
    projects = _read_projects()
    projects.insert(0, project)
    _write_projects(projects)
    return project

def list_recent_projects(limit=8):
    return _read_projects()[: max(1, int(limit))]

def delete_project(project_id):
    projects = _read_projects()
    keep, removed = [], None
    for project in projects:
        if project.get("id") == project_id:
            removed = dict(project)
        else:
            keep.append(project)
    if not removed:
        raise ValueError("Project was not found.")
    removed["deleted_at"] = datetime.now(timezone.utc).isoformat()
    deleted = _read_deleted_projects()
    deleted.insert(0, removed)
    deleted, auto_cleaned_count = _trim_deleted_projects(deleted)
    _write_projects(keep)
    _write_deleted_projects(deleted)
    removed["bin_count"] = len(deleted)
    removed["auto_cleaned_count"] = auto_cleaned_count
    return removed

def list_deleted_projects(limit=20):
    limit = min(DELETED_PROJECT_LIMIT, max(1, int(limit)))
    return _read_deleted_projects()[:limit]

def move_all_projects_to_bin():
    projects = _read_projects()
    if not projects:
        return {"moved_count": 0, "bin_count": len(_read_deleted_projects()), "auto_cleaned_count": 0}
    now = datetime.now(timezone.utc).isoformat()
    moved = []
    for project in projects:
        item = dict(project)
        item["deleted_at"] = now
        moved.append(item)
    deleted = moved + _read_deleted_projects()
    deleted, auto_cleaned_count = _trim_deleted_projects(deleted)
    _write_projects([])
    _write_deleted_projects(deleted)
    return {"moved_count": len(moved), "bin_count": len(deleted), "auto_cleaned_count": auto_cleaned_count}

def restore_project(project_id):
    deleted = _read_deleted_projects()
    keep, restored = [], None
    for project in deleted:
        if project.get("id") == project_id:
            restored = dict(project)
            restored.pop("deleted_at", None)
        else:
            keep.append(project)
    if not restored:
        raise ValueError("Deleted project was not found.")
    projects = _read_projects()
    projects.insert(0, restored)
    _write_projects(projects)
    _write_deleted_projects(keep)
    return restored

def empty_project_bin():
    count = len(_read_deleted_projects())
    _write_deleted_projects([])
    return {"deleted_count": count}

def _find_project(project_id):
    for project in _read_projects() + _read_deleted_projects():
        if project.get("id") == project_id:
            return project
    raise ValueError("Project was not found.")

def package_to_text(project):
    package = project.get("generated_package", {})
    def lines(title, value):
        if isinstance(value, dict):
            body = "\n".join(f"{k}: {v}" for k, v in value.items())
        elif isinstance(value, list):
            body = "\n".join(f"{i + 1}. {item}" for i, item in enumerate(value))
        else:
            body = str(value)
        return f"{title}\n{body}"
    return "\n\n".join([f"Project: {project.get('project_type', '')}", f"Client: {project.get('client_name', '')}", f"Service: {project.get('service', '')}", lines("CLIENT QUOTE", package.get("client_quote", "")), lines("PAYMENT BREAKDOWN", package.get("payment_breakdown", {})), lines("PROJECT CHECKLIST", package.get("project_checklist", [])), lines("DELIVERABLES", package.get("deliverables", [])), lines("CLIENT EMAIL", package.get("client_email", ""))]) + "\n"

def package_to_markdown(project):
    title = project.get("project_type") or "Creative Project"
    return f"# {title}\n\n```text\n{package_to_text(project)}\n```\n"

def _package_to_html(project):
    import html
    title = html.escape(project.get("project_type") or "Creative Project")
    body = html.escape(package_to_text(project)).replace("\n", "<br>")
    return f"<!doctype html><html><head><meta charset='utf-8'><title>{title}</title><style>body{{font-family:Arial,sans-serif;line-height:1.5;margin:40px;color:#172018}}</style></head><body><h1>{title}</h1><div>{body}</div></body></html>"

def _package_to_csv(project):
    package = project.get("generated_package", {})
    rows = [["field", "value"], ["client_name", project.get("client_name", "")], ["service", project.get("service", "")], ["design_fee", project.get("design_fee", "")], ["upfront_percent", project.get("upfront_percent", "")], ["project_type", project.get("project_type", "")], ["client_quote", package.get("client_quote", "")], ["client_email", package.get("client_email", "")]]
    output = []
    for row in rows:
        output.append(",".join(f'"{str(cell).replace(chr(34), chr(34) + chr(34))}"' for cell in row))
    return "\n".join(output) + "\n"

def _simple_pdf_bytes(text):
    def esc(value):
        return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    lines = []
    for raw in text.splitlines():
        lines.extend([raw[i:i + 92] for i in range(0, max(len(raw), 1), 92)])
    pages = []
    for start in range(0, len(lines), 44):
        commands = ["BT", "/F1 10 Tf", "50 790 Td", "14 TL"]
        for line in lines[start:start + 44]:
            commands.append(f"({esc(line)}) Tj")
            commands.append("T*")
        commands.append("ET")
        pages.append("\n".join(commands).encode("latin-1", errors="replace"))
    objects = [b"<< /Type /Catalog /Pages 2 0 R >>"]
    page_refs = []
    font_obj = 3 + (len(pages) * 2)
    for index, content in enumerate(pages):
        page_obj = 3 + (index * 2)
        content_obj = page_obj + 1
        page_refs.append(f"{page_obj} 0 R")
        objects.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 842] /Resources << /Font << /F1 {font_obj} 0 R >> >> /Contents {content_obj} 0 R >>".encode())
        objects.append(b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"\nendstream")
    objects.insert(1, f"<< /Type /Pages /Kids [{' '.join(page_refs)}] /Count {len(pages)} >>".encode())
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    result = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for number, obj in enumerate(objects, 1):
        offsets.append(len(result))
        result.extend(f"{number} 0 obj\n".encode() + obj + b"\nendobj\n")
    xref = len(result)
    result.extend(f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        result.extend(f"{offset:010d} 00000 n \n".encode())
    result.extend(f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    return bytes(result)

def export_project(project_id, file_format="txt"):
    project = _find_project(project_id)
    EXPORTS_DIR.mkdir(exist_ok=True)
    safe_client = "".join(ch if ch.isalnum() else "-" for ch in project.get("client_name", "project")).strip("-").lower() or "project"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    file_format = (file_format or "txt").lower().strip()
    if file_format in {"txt", "text"}:
        suffix, content = "txt", package_to_text(project).encode("utf-8")
    elif file_format in {"md", "markdown"}:
        suffix, content = "md", package_to_markdown(project).encode("utf-8")
    elif file_format in {"html", "htm"}:
        suffix, content = "html", _package_to_html(project).encode("utf-8")
    elif file_format == "json":
        suffix, content = "json", json.dumps(project, indent=2).encode("utf-8")
    elif file_format == "csv":
        suffix, content = "csv", _package_to_csv(project).encode("utf-8")
    elif file_format in {"doc", "word"}:
        suffix, content = "doc", _package_to_html(project).encode("utf-8")
    elif file_format == "pdf":
        suffix, content = "pdf", _simple_pdf_bytes(package_to_text(project))
    else:
        raise ValueError("Unsupported export format.")
    path = EXPORTS_DIR / f"{safe_client}-{stamp}.{suffix}"
    path.write_bytes(content)
    return {"project_id": project.get("id"), "format": suffix, "path": str(path), "file_name": path.name}

def export_projects_zip():
    EXPORTS_DIR.mkdir(exist_ok=True)
    projects = _read_projects()
    deleted = _read_deleted_projects()
    profile = get_brand_profile()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    path = EXPORTS_DIR / f"creative-studio-backup-{stamp}.zip"
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("projects.json", json.dumps(projects, indent=2))
        archive.writestr("deleted_projects.json", json.dumps(deleted, indent=2))
        archive.writestr("brand_profile.json", json.dumps(profile, indent=2))
        archive.writestr("README.txt", "Creative Studio MCP backup.\nKeep this file private because it may contain client and business information.\n")
        for index, project in enumerate(projects, 1):
            safe_client = "".join(ch if ch.isalnum() else "-" for ch in project.get("client_name", "project")).strip("-").lower() or "project"
            archive.writestr(f"active-projects/{index:03d}-{safe_client}.txt", package_to_text(project))
            archive.writestr(f"active-projects/{index:03d}-{safe_client}.md", package_to_markdown(project))
    return {"format": "zip", "path": str(path), "file_name": path.name, "project_count": len(projects), "deleted_count": len(deleted)}
