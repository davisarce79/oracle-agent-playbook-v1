# Gumroad API Skill

Manage your Gumroad products, sales, affiliates, and license keys programmatically.

**Authentication:** Uses API key stored in `~/.openclaw/workspace/.openclaw/credentials/gumroad.txt`

---

## Quick Start

```python
# List all products
result = await use_skill('gumroad-api', {'action': 'list_products'})

# Get sales for a specific product
result = await use_skill('gumroad-api', {
    'action': 'get_sales',
    'product_id': 'your-product-permalink',
    'limit': 50
})

# Check API health
result = await use_skill('gumroad-api', {'action': 'health_check'})
```

---

## Actions

| Action | Required Params | Optional Params | Description |
|--------|----------------|-----------------|-------------|
| `list_products` | none | - | Get all products |
| `get_product` | `product_id` | - | Get product details by ID or permalink |
| `create_product` | `product_data` (dict) | - | Create new product |
| `update_product` | `product_id`, `product_data` | - | Update existing product |
| `get_sales` | none | `product_id`, `limit` | List sales (all or filtered) |
| `get_affiliates` | none | `product_id` | List affiliates |
| `generate_license` | `product_id`, `email` | - | Generate license key |
| `health_check` | none | - | Test API connectivity |

---

## Examples

### Check current products and sales
```python
# List products
products = await use_skill('gumroad-api', {'action': 'list_products'})
for p in products.get('products', []):
    print(f"{p['name']} - {p['price']} - {p['permalink']}")
    
# Get recent sales
sales = await use_skill('gumroad-api', {'action': 'get_sales', 'limit': 10})
for s in sales.get('sales', []):
    print(f"{s['email']} bought {s['product_name']} for {s['price']}")
```

### Update product price
```python
result = await use_skill('gumroad-api', {
    'action': 'update_product',
    'product_id': 'oracle-agent-playbook',
    'product_data': {
        'price': 29.00,
        'description': 'Updated description...'
    }
})
```

### Generate license key for a customer
```python
result = await use_skill('gumroad-api', {
    'action': 'generate_license',
    'product_id': 'oracle-agent-playbook',
    'email': 'customer@example.com'
})
```

---

## Gumroad API Notes

- **Base URL:** `https://api.gumroad.com/v2`
- **Authentication:** Bearer token (your API key)
- **Docs:** https://gumroad.com/api

The skill wraps all major Gumroad endpoints. For advanced usage, you can extend `gumroad_api.py` with additional endpoints.

---

## Setup

The API key should be stored at:
```
~/.openclaw/workspace/.openclaw/credentials/gumroad.txt
```

With content being just the API key (no extra whitespace).

To get an API key:
1. Go to https://gumroad.com/settings/api
2. Create a new API key with appropriate permissions (products read/write, sales read)
3. Save it to the credentials file above

---

## Integration with *The Mechanical Soul* Marketing

Use this skill to:
- Auto-upload the manuscript as a product when ready
- Check sales daily in your heartbeat
- Generate license keys for advanced buyers (e.g., "Founder's Tier")
- Track affiliate referrals
- Update product price during launch promos

---

## Limitations

- Gumroad API rate limits: ~60 requests/minute (plenty for our use)
- Only works with Gumroad (not Stripe directly)
- File uploads require pre-hosted file URL (Gumroad doesn't host; use Vercel/Cloudflare R2)
