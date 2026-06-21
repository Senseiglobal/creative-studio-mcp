from mcp.server.fastmcp import FastMCP

from business_tools import (
    calculate_payment as calculate_payment_data,
    create_project_package as create_project_package_data,
    create_quote as create_quote_text,
    generate_project_checklist as generate_project_checklist_data,
    list_recent_projects as list_recent_projects_data,
    list_services as list_services_data,
    save_project as save_project_data,
)


mcp = FastMCP("Creative Studio MCP")


@mcp.tool()
def list_services() -> dict:
    """List available creative studio services and price ranges."""
    return list_services_data()


@mcp.tool()
def calculate_payment(total_fee: int, upfront_percent: int = 70) -> dict:
    """Calculate upfront and balance payment for a project."""
    return calculate_payment_data(total_fee, upfront_percent)


@mcp.tool()
def generate_project_checklist(project_type: str) -> list[str]:
    """Generate a basic creative project checklist."""
    return generate_project_checklist_data(project_type)


@mcp.tool()
def create_quote(
    client_name: str,
    service: str,
    design_fee: int,
    includes_printing: bool = False,
) -> str:
    """Create a short client quotation message."""
    return create_quote_text(client_name, service, design_fee, includes_printing)


@mcp.tool()
def create_project_package(
    client_name: str,
    service: str,
    design_fee: int,
    upfront_percent: int = 70,
    project_type: str = "",
) -> dict:
    """Create a complete creative project package."""
    return create_project_package_data(
        client_name, service, design_fee, upfront_percent, project_type
    )


@mcp.tool()
def save_project(
    client_name: str,
    service: str,
    design_fee: int,
    upfront_percent: int = 70,
    project_type: str = "",
) -> dict:
    """Save a generated creative project locally."""
    package = create_project_package_data(
        client_name, service, design_fee, upfront_percent, project_type
    )
    return save_project_data(
        client_name, service, design_fee, upfront_percent, project_type, package
    )


@mcp.tool()
def list_recent_projects(limit: int = 8) -> list[dict]:
    """List recent saved projects."""
    return list_recent_projects_data(limit)


if __name__ == "__main__":
    mcp.run(transport="stdio")
