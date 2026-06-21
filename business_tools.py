import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


PROJECTS_FILE = Path(__file__).resolve().parent / "projects.json"

SERVICES = {
    "Brand Identity Design": "$500 to $2,500+",
    "Product Packaging Design": "$400 to $1,500+",
    "Corporate Profile Design": "$300 to $1,200+",
    "Proposal / Presentation Design": "$150 to $700+",
    "Merchandise Design": "$250 to $1,000+",
    "Banner & Event Visual Design": "$50 to $500+",
}


def format_currency(value: int | float | str) -> str:
    amount = int(float(value))
    return f"${amount:,}"


def validate_project_inputs(
    client_name: str,
    service: str,
    design_fee: int | float | str,
    upfront_percent: int | float | str = 70,
    project_type: str = "",
) -> dict:
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


def list_services() -> dict:
    """List available creative studio services and price ranges."""
    return dict(SERVICES)


def calculate_payment(total_fee: int, upfront_percent: int = 70) -> dict:
    """Calculate upfront and balance payment for a project."""
    total_fee = int(float(total_fee))
    upfront_percent = int(float(upfront_percent))

    if total_fee <= 0:
        raise ValueError("Total fee must be greater than zero.")
    if upfront_percent < 0 or upfront_percent > 100:
        raise ValueError("Upfront percent must be between 0 and 100.")

    upfront = round(total_fee * upfront_percent / 100)
    balance = total_fee - upfront

    return {
        "total_fee": format_currency(total_fee),
        "upfront_percent": f"{upfront_percent}%",
        "upfront_payment": format_currency(upfront),
        "balance_payment": format_currency(balance),
    }


def generate_project_checklist(project_type: str) -> list[str]:
    """Generate a basic creative project checklist."""
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
    """Create a simple deliverables list for the selected service."""
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


def create_client_email(
    client_name: str,
    service: str,
    design_fee: int,
    upfront_percent: int = 70,
    project_type: str = "",
) -> str:
    """Create a short email draft for the client."""
    values = validate_project_inputs(
        client_name, service, design_fee, upfront_percent, project_type
    )
    payment = calculate_payment(values["design_fee"], values["upfront_percent"])

    return f"""Subject: Project Quote For {values['service']}

Hello {values['client_name']},

Thank you for your interest in working with us.

I have prepared a quote for {values['service']} at {format_currency(values['design_fee'])}.

Payment breakdown:
Upfront payment ({payment['upfront_percent']}): {payment['upfront_payment']}
Balance payment: {payment['balance_payment']}

Once approved, we can confirm the brief, timeline, and required files.

Best regards,
Thomas Ogun
"""


def create_quote(
    client_name: str,
    service: str,
    design_fee: int,
    includes_printing: bool = False,
) -> str:
    """Create a short client quotation message."""
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

Thank you for your interest in our creative services.

Service: {service}
Creative Design Fee: {format_currency(design_fee)}

Payment Terms:
70% upfront before project commencement.
30% balance before final delivery.

Note:
{printing_note}

Best regards,
Thomas Ogun
"""


def create_project_package(
    client_name: str,
    service: str,
    design_fee: int,
    upfront_percent: int = 70,
    project_type: str = "",
) -> dict:
    """Create a complete project package for daily business use."""
    values = validate_project_inputs(
        client_name, service, design_fee, upfront_percent, project_type
    )

    return {
        "client_quote": create_quote(
            values["client_name"], values["service"], values["design_fee"]
        ),
        "payment_breakdown": calculate_payment(
            values["design_fee"], values["upfront_percent"]
        ),
        "project_checklist": generate_project_checklist(values["project_type"]),
        "deliverables": create_deliverables_list(
            values["service"], values["project_type"]
        ),
        "client_email": create_client_email(
            values["client_name"],
            values["service"],
            values["design_fee"],
            values["upfront_percent"],
            values["project_type"],
        ),
    }


def ensure_projects_file() -> None:
    if not PROJECTS_FILE.exists():
        PROJECTS_FILE.write_text("[]", encoding="utf-8")


def _read_projects() -> list[dict]:
    ensure_projects_file()
    try:
        data = json.loads(PROJECTS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        data = []
    return data if isinstance(data, list) else []


def _write_projects(projects: list[dict]) -> None:
    PROJECTS_FILE.write_text(json.dumps(projects, indent=2), encoding="utf-8")


def save_project(
    client_name: str,
    service: str,
    design_fee: int,
    upfront_percent: int = 70,
    project_type: str = "",
    generated_package: dict | None = None,
) -> dict:
    """Save a generated project locally."""
    values = validate_project_inputs(
        client_name, service, design_fee, upfront_percent, project_type
    )
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
    """List recently saved projects."""
    projects = _read_projects()
    return projects[: max(1, int(limit))]
