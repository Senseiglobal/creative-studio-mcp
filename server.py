from mcp.server.fastmcp import FastMCP

from business_tools import (
    calculate_payment as calculate_payment_data,
    create_project_package as create_project_package_data,
    create_quote as create_quote_text,
    delete_project as delete_project_data,
    empty_project_bin as empty_project_bin_data,
    export_project as export_project_data,
    generate_project_checklist as generate_project_checklist_data,
    get_brand_profile as get_brand_profile_data,
    list_deleted_projects as list_deleted_projects_data,
    list_recent_projects as list_recent_projects_data,
    list_services as list_services_data,
    save_brand_profile as save_brand_profile_data,
    save_project as save_project_data,
)

mcp = FastMCP("Creative Studio MCP")

@mcp.tool()
def get_brand_profile() -> dict:
    return get_brand_profile_data()

@mcp.tool()
def save_brand_profile(profile: dict) -> dict:
    return save_brand_profile_data(profile)

@mcp.tool()
def list_services() -> dict:
    return list_services_data()

@mcp.tool()
def calculate_payment(total_fee: int, upfront_percent: int = 70) -> dict:
    return calculate_payment_data(total_fee, upfront_percent)

@mcp.tool()
def generate_project_checklist(project_type: str) -> list[str]:
    return generate_project_checklist_data(project_type)

@mcp.tool()
def create_quote(client_name: str, service: str, design_fee: int, includes_printing: bool = False) -> str:
    return create_quote_text(client_name, service, design_fee, includes_printing)

@mcp.tool()
def create_project_package(client_name: str, service: str, design_fee: int, upfront_percent: int = 70, project_type: str = "") -> dict:
    return create_project_package_data(client_name, service, design_fee, upfront_percent, project_type)

@mcp.tool()
def save_project(client_name: str, service: str, design_fee: int, upfront_percent: int = 70, project_type: str = "") -> dict:
    package = create_project_package_data(client_name, service, design_fee, upfront_percent, project_type)
    return save_project_data(client_name, service, design_fee, upfront_percent, project_type, package)

@mcp.tool()
def list_recent_projects(limit: int = 8) -> list[dict]:
    return list_recent_projects_data(limit)

@mcp.tool()
def delete_project(project_id: str) -> dict:
    return delete_project_data(project_id)

@mcp.tool()
def list_deleted_projects(limit: int = 20) -> list[dict]:
    return list_deleted_projects_data(limit)

@mcp.tool()
def empty_project_bin() -> dict:
    return empty_project_bin_data()

@mcp.tool()
def export_project(project_id: str, file_format: str = "txt") -> dict:
    return export_project_data(project_id, file_format)

if __name__ == "__main__":
    mcp.run(transport="stdio")
