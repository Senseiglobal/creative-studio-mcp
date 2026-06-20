from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Creative Studio MCP")


@mcp.tool()
def list_services() -> dict:
    """List available creative studio services and price ranges."""
    return {
        "Brand Identity Design": "$500 to $2,500+",
        "Product Packaging Design": "$400 to $1,500+",
        "Corporate Profile Design": "$300 to $1,200+",
        "Proposal / Presentation Design": "$150 to $700+",
        "Merchandise Design": "$250 to $1,000+",
        "Banner & Event Visual Design": "$50 to $500+",
    }


@mcp.tool()
def calculate_payment(total_fee: int, upfront_percent: int = 70) -> dict:
    """Calculate upfront and balance payment for a project."""
    upfront = round(total_fee * upfront_percent / 100)
    balance = total_fee - upfront

    return {
        "total_fee": f"${total_fee:,}",
        "upfront_percent": f"{upfront_percent}%",
        "upfront_payment": f"${upfront:,}",
        "balance_payment": f"${balance:,}",
    }


@mcp.tool()
def generate_project_checklist(project_type: str) -> list[str]:
    """Generate a basic creative project checklist."""
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
        "Confirm printing/production separately if needed",
    ]


@mcp.tool()
def create_quote(
    client_name: str,
    service: str,
    design_fee: int,
    includes_printing: bool = False,
) -> str:
    """Create a short client quotation message."""
    printing_note = (
        "Printing/production is included in this quote."
        if includes_printing
        else "Printing/production is not included and will be quoted separately after design approval."
    )

    return f"""
Hello {client_name},

Thank you for your interest in our creative services.

Service: {service}
Creative Design Fee: ${design_fee:,}

Payment Terms:
70% upfront before project commencement.
30% balance before final delivery.

Note:
{printing_note}

Best regards,
Thomas Ogun
"""


if __name__ == "__main__":
    mcp.run()
