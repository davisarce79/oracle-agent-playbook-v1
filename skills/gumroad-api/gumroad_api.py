#!/usr/bin/env python3
"""
Gumroad API Skill - Manage products, sales, and affiliates
"""

import os
import json
import requests
from typing import Dict, Any, List

# Load API key from credentials file
CRED_PATH = os.path.expanduser('~/.openclaw/workspace/.openclaw/credentials/gumroad.txt')
if os.path.exists(CRED_PATH):
    with open(CRED_PATH, 'r') as f:
        API_KEY = f.read().strip()
else:
    API_KEY = None

BASE_URL = "https://api.gumroad.com/v2"

def get_headers() -> Dict[str, str]:
    """Get request headers with API key."""
    if not API_KEY:
        raise ValueError("Gumroad API key not found. Please ensure credentials file exists.")
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

def list_products() -> Dict[str, Any]:
    """List all products."""
    resp = requests.get(f"{BASE_URL}/products", headers=get_headers())
    resp.raise_for_status()
    return resp.json()

def get_product(product_id: str) -> Dict[str, Any]:
    """Get product details by ID or permalink."""
    resp = requests.get(f"{BASE_URL}/products/{product_id}", headers=get_headers())
    resp.raise_for_status()
    return resp.json()

def create_product(product_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new product.
    
    Required fields: name, price, description, file_url (or use custom fields)
    """
    resp = requests.post(f"{BASE_URL}/products", headers=get_headers(), json=product_data)
    resp.raise_for_status()
    return resp.json()

def update_product(product_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """Update an existing product."""
    resp = requests.put(f"{BASE_URL}/products/{product_id}", headers=get_headers(), json=updates)
    resp.raise_for_status()
    return resp.json()

def get_sales(product_id: str = None, limit: int = 100) -> Dict[str, Any]:
    """Get sales data. Filter by product_id if provided."""
    params = {'limit': limit}
    if product_id:
        params['product_id'] = product_id
    resp = requests.get(f"{BASE_URL}/sales", headers=get_headers(), params=params)
    resp.raise_for_status()
    return resp.json()

def get_affiliates(product_id: str = None) -> Dict[str, Any]:
    """List affiliates. Optionally filter by product."""
    params = {}
    if product_id:
        params['product_id'] = product_id
    resp = requests.get(f"{BASE_URL}/affiliates", headers=get_headers(), params=params)
    resp.raise_for_status()
    return resp.json()

def generate_license_key(product_id: str, email: str) -> Dict[str, Any]:
    """Generate a license key for a product."""
    resp = requests.post(
        f"{BASE_URL}/products/{product_id}/license_keys",
        headers=get_headers(),
        json={"email": email}
    )
    resp.raise_for_status()
    return resp.json()

def check_api_health() -> Dict[str, Any]:
    """Test API connectivity."""
    try:
        resp = requests.get(f"{BASE_URL}/products", headers=get_headers(), timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return {
                "status": "ok",
                "products_count": len(data.get('products', [])),
                "message": "Gumroad API accessible"
            }
        else:
            return {
                "status": "error",
                "code": resp.status_code,
                "message": resp.text
            }
    except Exception as e:
        return {"status": "error", "exception": str(e)}

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python gumroad_api.py <command> [args...]")
        print("Commands: products, get <id>, sales [product_id], affiliates [product_id], health")
        sys.exit(1)
    
    cmd = sys.argv[1]
    try:
        if cmd == "products":
            result = list_products()
        elif cmd == "get" and len(sys.argv) >= 3:
            result = get_product(sys.argv[2])
        elif cmd == "sales":
            pid = sys.argv[2] if len(sys.argv) > 2 else None
            result = get_sales(product_id=pid)
        elif cmd == "affiliates":
            pid = sys.argv[2] if len(sys.argv) > 2 else None
            result = get_affiliates(product_id=pid)
        elif cmd == "health":
            result = check_api_health()
        else:
            print(f"Unknown command: {cmd}")
            sys.exit(1)
        
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
