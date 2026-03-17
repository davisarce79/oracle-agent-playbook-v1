"""Gumroad API Skill - Manage products, sales, and affiliates"""

from .gumroad_api import (
    list_products,
    get_product,
    create_product,
    update_product,
    get_sales,
    get_affiliates,
    generate_license_key,
    check_api_health
)

# Skill metadata for OpenClaw
SKILL_INFO = {
    "name": "gumroad-api",
    "description": "Interact with Gumroad API for product management, sales tracking, and affiliate management. Uses stored credentials.",
    "capabilities": ["ecommerce", "products", "sales"],
    "parameters": {
        "action": {
            "type": "string",
            "required": True,
            "description": "Action to perform: list_products, get_product, create_product, update_product, get_sales, get_affiliates, generate_license, health_check"
        },
        "product_id": {"type": "string", "required": False, "description": "Product ID or permalink (for get, update, sales, affiliates, generate_license)"},
        "product_data": {"type": "object", "required": False, "description": "Product data for create/update (name, price, description, file_url, etc.)"},
        "email": {"type": "string", "required": False, "description": "Email for license key generation"},
        "limit": {"type": "integer", "default": 100, "description": "Limit for sales/affiliates list"}
    }
}

async def handle_call(params: dict) -> dict:
    """
    Gumroad API skill entry point.
    
    Required params:
        action (string): one of [list_products, get_product, create_product, update_product, get_sales, get_affiliates, generate_license, health_check]
    
    Optional params depend on action:
        product_id: for get, update, sales, affiliates, generate_license
        product_data: for create, update
        email: for generate_license
        limit: for sales, affiliates
    
    Returns:
        Dict with API response data.
    """
    action = params.get("action")
    if not action:
        return {"error": "Missing required parameter: action"}
    
    try:
        if action == "list_products":
            return list_products()
        
        elif action == "get_product":
            pid = params.get("product_id")
            if not pid:
                return {"error": "product_id required for get_product"}
            return get_product(pid)
        
        elif action == "create_product":
            pdata = params.get("product_data")
            if not pdata or not isinstance(pdata, dict):
                return {"error": "product_data (dict) required for create_product"}
            return create_product(pdata)
        
        elif action == "update_product":
            pid = params.get("product_id")
            pdata = params.get("product_data")
            if not pid or not pdata:
                return {"error": "product_id and product_data required for update_product"}
            return update_product(pid, pdata)
        
        elif action == "get_sales":
            pid = params.get("product_id")
            limit = int(params.get("limit", 100))
            return get_sales(product_id=pid, limit=limit)
        
        elif action == "get_affiliates":
            pid = params.get("product_id")
            return get_affiliates(product_id=pid)
        
        elif action == "generate_license":
            pid = params.get("product_id")
            email = params.get("email")
            if not pid or not email:
                return {"error": "product_id and email required for generate_license"}
            return generate_license_key(pid, email)
        
        elif action == "health_check":
            return check_api_health()
        
        else:
            return {"error": f"Unknown action: {action}"}
    
    except requests.HTTPError as e:
        return {
            "error": f"HTTP {e.response.status_code}",
            "detail": e.response.text if e.response else str(e)
        }
    except Exception as e:
        return {"error": str(e)}
