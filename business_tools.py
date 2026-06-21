import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


BASE_DIR = Path(__file__).resolve().parent
PROJECTS_FILE = BASE_DIR / "projects.json"
DELETED_PROJECTS_FILE = BASE_DIR / "deleted_projects.json"
BRAND_PROFILE_FILE = BASE_DIR / "brand_profile.json"
EXPORTS_DIR = BASE_DIR / "exports"

DEFAULT_SERVICES = {
    "Brand Identity Design": "$500 to $2,500+",
    "Product Packaging Design": "$400 to $1,500+",
    "Corporate Profile Design": "$300 to $1,200+",
    "Proposal / Presentation Design": "$150 to $700+",
    "Merchandise Design": "$250 to $1,000+",
    "Banner & Event Visual Design": "$50 to $500+",
}

DEFAULT_PROFILE = {
    "business_name": "Creative Studio",
    "owner_name": "Thomas Ogun",
    "email": "",
    "phone": "",
    "website": "",
    "location": "",
    "brand_voice": "Professional, clear, friendly, and confident.",
    "payment_terms": "70% upfront before project commencement. 30% balance before final delivery.",
    "currency": "USD",
    "services": DEFAULT_SERVICES,
}


def ensure_json_file(path: Path, default_value) -> None:
    if not path.exists():
        path.write_text(json.dumps(default_value, indent=2), encoding="utf-8")


def read_json(path: Path, default_value):
    ensure_json_file(path, default_value)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        data = default_value
    return data


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2), encoding="utf-8")


def format_currency(value, currency: str | None = None) -> str:
    amount = int(float(value))
    symbol = "$" if (currency or "USD").upper() == "USD" else f"{currency} "
    return f"{symbol}{amount:,}"


def get_brand_profile() -> dict:
    data = read_json(BRAND_PROFILE_FILE, DEFAULT_PROFILE)
    profile = dict(DEFAULT_PROFILE)
    if isinstance(data, dict):
        profile.update(data)
    if not isinstance(profile.get("services"), dict) or not profile["services"]:
        profile["services"] = dict(DEFAULT_SERVICES)
    return profile


def save_brand_profile(profile: dict) -> dict:
    current = get_brand_profile()
    cleaned = dict(current)
    for key in [
        "business_name",
        "owner_name",
        "email",
        "phone",
        "website",
        "location",
        "brand_voice",
        "payment_terms",
        "currency",
    ]:
        if key in profile:
            cleaned[key] = str(profile.get(key, "")).strip()
    services = profile.get("services")
    if isinstance(services, dict):
        cleaned["services"] = {
            str(name).strip(): str(price).strip()
            for name, price in services.items()
            if str(name).strip() and str(price).strip()
        } or dict(DEFAULT_SERVICES)
    write_json(BRAND_PROFILE_FILE, cleaned)
    return cleaned


def parse_services_text(text: str) -> dict:
    services = {}
    for raw_line in (text or "").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if "|" in line:
            name, price = line.split("|", 1)
        elif ":" in line:
            name, price = line.split(":", 1)
        else:
            continue
        name = name.strip()
        price = price.strip()
        if name and price:
            services[name] = price
    return services


def list_services() -> dict:
    return dict(get_brand_profile()["services"])


def validate_project_inputs(client_name, service, design_fee, upfront_percent=70, project_type="") -> dict:
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
    return {
        "client_name": client_name,
        "service": service,
        "design_fee": design_fee,
        "upfront_percent": upfront_percent,
        "project_type": project_type,
    }


def calculate_payment(total_fee: int, upfront_percent: int = 70) -> dict:
    profile = get_brand_profile()
    total_fee = int(float(total_fee))
    upfront_percent = int(float(upfront_percent))
    if total_fee <= 0:
        raise ValueError("Total fee must be greater than zero.")
    if upfront_percent < 0 or upfront_percent > 100:
        raise ValueError("Upfront percent must be between 0 and 100.")
    upfront = round(total_fee * upfront_percent / 100)
    balance = total_fee - upfront
    return {
        "total_fee": format_currency(total_fee, profile["currency"]),
        "upfront_percent": f"{upfront_percent}%",
        "upfront_payment": format_currency(upfront, profile["currency"]),
        "balance_payment": format_currency(balance, profile["currency"]),
    }


def generate_project_checklist(project_type: str) -> list[str]:
    project_type = (project_type or "Creative project").strip()
    return [
        f"Confirm project type: {project_type}",
        "Confirm client brief and brand goals",
        "Collect logo, references, and content assets",
        "Define deliverables",
        "Confirm design direction",
        "Create first draft",
        "Review client feedback",
        "Apply revisions",
        "Prepare final files",
        "Confirm printing or production separately if needed",
    ]


def create_deliverables_list(service: str, project_type: str = "") -> list[str]:
    service = (service or "Creative Service").strip()
    project_type = (project_type or service).strip()
    return [
        f"Creative direction for {project_type}",
        f"Design execution for {service}",
        "Client review version",
        "Revision support based on agreed scope",
        "Final client-ready files",
        "Basic usage or handover notes",
    ]


def create_quote(client_name: str, service: str, design_fee: int, includes_printing: bool = False) -> str:
    profile = get_brand_profile()
    client_name = (client_name or "Client").strip()
    service = (service or "Creative Service").strip()
    design_fee = int(float(design_fee))
    if design_fee <= 0:
        raise ValueError("Design fee must be greater than zero.")
    printing_note = (
        "Printing or production is included in this quote."
        if includes_printing
        else "Printing or production is not included and will be quoted separately after design approval."
    )
    return f"""Hello {client_name},

Thank you for your interest in {profile['business_name']}.

Service: {service}
Creative Design Fee: {format_currency(design_fee, profile['currency'])}

Payment Terms:
{profile['payment_terms']}

Note:
{printing_note}

Best regards,
{profile['owner_name']}
"""


def create_client_email(client_name: str, service: str, design_fee: int, upfront_percent: int = 70, project_type: str = "") -> str:
    profile = get_brand_profile()
    values = validate_project_inputs(client_name, service, design_fee, upfront_percent, project_type)
    payment = calculate_payment(values["design_fee"], values["upfront_percent"])
    contact_lines = []
    if profile.get("email"):
        contact_lines.append(f"Email: {profile['email']}")
    if profile.get("phone"):
        contact_lines.append(f"Phone: {profile['phone']}")
    if profile.get("website"):
        contact_lines.append(f"Website: {profile['website']}")
    contact = "\n".join(contact_lines)
    if contact:
        contact = "\n\n" + contact
    return f"""Subject: Project Quote For {values['service']}

Hello {values['client_name']},

Thank you for your interest in working with {profile['business_name']}.

I have prepared a quote for {values['service']} at {format_currency(values['design_fee'], profile['currency'])}.

Payment breakdown:
Upfront payment ({payment['upfront_percent']}): {payment['upfront_payment']}
Balance payment: {payment['balance_payment']}

Once approved, we can confirm the brief, timeline, and required files.

Best regards,
{profile['owner_name']}
{profile['business_name']}{contact}
"""


def create_project_package(client_name: str, service: str, design_fee: int, upfront_percent: int = 70, project_type: str = "") -> dict:
    values = validate_project_inputs(client_name, service, design_fee, upfront_percent, project_type)
    return {
        "client_quote": create_quote(values["client_name"], values["service"], values["design_fee"]),
        "payment_breakdown": calculate_payment(values["design_fee"], values["upfront_percent"]),
        "project_checklist": generate_project_checklist(values["project_type"]),
        "deliverables": create_deliverables_list(values["service"], values["project_type"]),
        "client_email": create_client_email(
            values["client_name"],
            values["service"],
            values["design_fee"],
            values["upfront_percent"],
            values["project_type"],
        ),
    }


def _read_projects() -> list[dict]:
    data = read_json(PROJECTS_FILE, [])
    return data if isinstance(data, list) else []


def _write_projects(projects: list[dict]) -> None:
    write_json(PROJECTS_FILE, projects)


def _read_deleted_projects() -> list[dict]:
    data = read_json(DELETED_PROJECTS_FILE, [])
    return data if isinstance(data, list) else []


def _write_deleted_projects(projects: list[dict]) -> None:
    write_json(DELETED_PROJECTS_FILE, projects)


def save_project(client_name: str, service: str, design_fee: int, upfront_percent: int = 70, project_type: str = "", generated_package: dict | None = None) -> dict:
    values = validate_project_inputs(client_name, service, design_fee, upfront_percent, project_type)
    package = generated_package or create_project_package(**values)
    project = {
        "id": str(uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "client_name": values["client_name"],
        "service": values["service"],
        "design_fee": values["design_fee"],
        "upfront_percent": values["upfront_percent"],
        "project_type": values["project_type"],
        "generated_package": package,
    }
    projects = _read_projects()
    projects.insert(0, project)
    _write_projects(projects)
    return project


def list_recent_projects(limit: int = 8) -> list[dict]:
    return _read_projects()[: max(1, int(limit))]


def delete_project(project_id: str) -> dict:
    project_id = str(project_id or "").strip()
    projects = _read_projects()
    keep = []
    removed = None
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
    _write_projects(keep)
    _write_deleted_projects(deleted)
    return removed


def list_deleted_projects(limit: int = 20) -> list[dict]:
    return _read_deleted_projects()[: max(1, int(limit))]


def restore_project(project_id: str) -> dict:
    project_id = str(project_id or "").strip()
    deleted = _read_deleted_projects()
    keep = []
    restored = None
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


def empty_project_bin() -> dict:
    count = len(_read_deleted_projects())
    _write_deleted_projects([])
    return {"deleted_count": count}


def _find_project(project_id: str) -> dict:
    for project in _read_projects() + _read_deleted_projects():
        if project.get("id") == project_id:
            return project
    raise ValueError("Project was not found.")


def _package_to_text(project: dict) -> str:
    package = project.get("generated_package", {})
    parts = [
        f"Project: {project.get('project_type', '')}",
        f"Client: {project.get('client_name', '')}",
        f"Service: {project.get('service', '')}",
        "",
        "CLIENT QUOTE",
        str(package.get("client_quote", "")),
        "",
        "PAYMENT BREAKDOWN",
        "\n".join(f"{key}: {value}" for key, value in package.get("payment_breakdown", {}).items()),
        "",
        "PROJECT CHECKLIST",
        "\n".join(f"{index + 1}. {item}" for index, item in enumerate(package.get("project_checklist", []))),
        "",
        "DELIVERABLES",
        "\n".join(f"{index + 1}. {item}" for index, item in enumerate(package.get("deliverables", []))),
        "",
        "CLIENT EMAIL",
        str(package.get("client_email", "")),
    ]
    return "\n".join(parts).strip() + "\n"


def _package_to_html(project: dict) -> str:
    import html
    profile = get_brand_profile()
    title = html.escape(project.get("project_type") or "Creative Project")
    body = html.escape(_package_to_text(project)).replace("\n", "<br>")
    business = html.escape(profile.get("business_name", "Creative Studio"))
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{title}</title>
<style>body{{font-family:Arial,sans-serif;line-height:1.5;margin:40px;color:#172018}}h1{{margin-bottom:4px}}.brand{{color:#5f6b63;margin-bottom:24px}}</style>
</head><body><h1>{title}</h1><div class="brand">{business}</div><div>{body}</div></body></html>
"""


def _package_to_csv(project: dict) -> str:
    package = project.get("generated_package", {})
    rows = [
        ["field", "value"],
        ["client_name", project.get("client_name", "")],
        ["service", project.get("service", "")],
        ["design_fee", project.get("design_fee", "")],
        ["upfront_percent", project.get("upfront_percent", "")],
        ["project_type", project.get("project_type", "")],
        ["client_quote", package.get("client_quote", "")],
        ["client_email", package.get("client_email", "")],
    ]
    output = []
    for row in rows:
        escaped = [str(cell).replace('"', '""') for cell in row]
        output.append(",".join(f'"{cell}"' for cell in escaped))
    return "\n".join(output) + "\n"


def _simple_pdf_bytes(text: str) -> bytes:
    def esc(value: str) -> str:
        return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    lines = []
    for raw in text.splitlines():
        if len(raw) <= 92:
            lines.append(raw)
        else:
            for index in range(0, len(raw), 92):
                lines.append(raw[index:index + 92])
    pages = []
    for start in range(0, len(lines), 44):
        chunk = lines[start:start + 44]
        commands = ["BT", "/F1 10 Tf", "50 790 Td", "14 TL"]
        for line in chunk:
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
    for number, obj in enumerate(objects, start=1):
        offsets.append(len(result))
        result.extend(f"{number} 0 obj\n".encode())
        result.extend(obj)
        result.extend(b"\nendobj\n")
    xref = len(result)
    result.extend(f"xref\n0 {len(objects) + 1}\n".encode())
    result.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        result.extend(f"{offset:010d} 00000 n \n".encode())
    result.extend(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    return bytes(result)


def export_project(project_id: str, file_format: str = "txt") -> dict:
    project = _find_project(project_id)
    EXPORTS_DIR.mkdir(exist_ok=True)
    safe_client = "".join(ch if ch.isalnum() else "-" for ch in project.get("client_name", "project")).strip("-").lower() or "project"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    file_format = (file_format or "txt").lower().strip()
    if file_format in {"text", "txt"}:
        suffix, content = "txt", _package_to_text(project).encode("utf-8")
    elif file_format in {"md", "markdown"}:
        suffix, content = "md", f"# {project.get('project_type') or 'Creative Project'}\n\n```text\n{_package_to_text(project)}\n```\n".encode("utf-8")
    elif file_format in {"html", "htm"}:
        suffix, content = "html", _package_to_html(project).encode("utf-8")
    elif file_format == "json":
        suffix, content = "json", json.dumps(project, indent=2).encode("utf-8")
    elif file_format == "csv":
        suffix, content = "csv", _package_to_csv(project).encode("utf-8")
    elif file_format in {"doc", "word"}:
        suffix, content = "doc", _package_to_html(project).encode("utf-8")
    elif file_format == "pdf":
        suffix, content = "pdf", _simple_pdf_bytes(_package_to_text(project))
    else:
        raise ValueError("Unsupported export format.")
    path = EXPORTS_DIR / f"{safe_client}-{stamp}.{suffix}"
    path.write_bytes(content)
    return {"project_id": project.get("id"), "format": suffix, "path": str(path), "file_name": path.name}
