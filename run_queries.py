import sqlite3
import json
from collections import defaultdict

conn = sqlite3.connect("invoice_app.db")
conn.row_factory = sqlite3.Row

print("✅ Database connected!")
print("📊 Invoice Analytics Project\n")

print("=== Q1: Top 5 Customers by Revenue ===")

rows = conn.execute("""
    SELECT ir.customer_name, ir.created_at, id.full_data
    FROM invoice_records ir
    JOIN invoice_details id ON id.invoice_record_id = ir.id
""").fetchall()

revenue = defaultdict(float)

for row in rows:
    data = json.loads(row["full_data"])
    name = row["customer_name"].strip().lower()
    for product in data.get("products", []):
        revenue[name] += product.get("total", 0)

top5 = sorted(revenue.items(), key=lambda x: x[1], reverse=True)[:5]

for name, total in top5:
    print(f"  {name.title()} → ₹{total:,.2f}")

# ============================================
# Q2: Most Sold Products by Quantity
# ============================================
print("\n=== Q2: Most Sold Products ===")

product_qty = defaultdict(float)

for row in rows:
    data = json.loads(row["full_data"])
    for product in data.get("products", []):
        name = product["name"].strip().lower()
        product_qty[name] += product.get("qty", 0)

top5_products = sorted(product_qty.items(), key=lambda x: x[1], reverse=True)[:5]

for name, qty in top5_products:
    print(f"  {name.title()} → {qty} units")
# ============================================
# Q3: Monthly Invoice Trend (JSON se)
# ============================================
print("\n=== Q3: Monthly Invoice Trend ===")

from collections import defaultdict

monthly = defaultdict(lambda: {"invoices": 0, "revenue": 0.0})

for row in rows:
    data = json.loads(row["full_data"])
    month = row["created_at"][:7]  # "30-03-2026" → "30-03-20"
    
    total = sum(p.get("total", 0) for p in data.get("products", []))
    monthly[month]["invoices"] += 1
    monthly[month]["revenue"] += total

for month in sorted(monthly.keys()):
    m = monthly[month]
    print(f"  {month} → {m['invoices']} invoices → ₹{m['revenue']:,.2f}")

    # ============================================
# Q4: Inactive Customers (30+ days)
# ============================================
print("\n=== Q4: Inactive Customers ===")

rows_inactive = conn.execute("""
    SELECT name, last_used_at
    FROM customers
    WHERE last_used_at < date('now', '-30 days')
    ORDER BY last_used_at ASC
""").fetchall()

for row in rows_inactive:
    print(f"  {row['name']} → Last seen: {row['last_used_at'][:10]}")