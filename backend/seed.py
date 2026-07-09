"""
Run once after setting up the database:
    python seed.py

Populates the `products` table with the catalog currently hardcoded in
products.html, so the same data can eventually be served dynamically.
"""
from app.database import SessionLocal, Base, engine
from app.models.product import Product

Base.metadata.create_all(bind=engine)

CATALOG = [
    dict(name="Water Cups", category="cups", description="Lightweight, leak-proof paper cups for cold drinks.", price_per_piece=1.00, badge="Eco"),
    dict(name="Tea Cups", category="cups", description="Heat-resistant paper cups for hot beverages.", price_per_piece=1.50, badge="Popular"),
    dict(name="Tiffin Plates", category="plates", description="3/4-compartment meal plates.", price_per_piece=3.00, badge="Bulk Deal"),
    dict(name="Round Dinner Plates", category="plates", description="Heavy-duty bagasse plates, microwave-safe.", price_per_piece=2.50, badge="Popular"),
    dict(name="Soup Bowls", category="others", description="Deep-walled disposable bowls, available with lids.", price_per_piece=2.00, badge=None),
    dict(name="Spoon & Fork Set", category="others", description="Sturdy CPLA & wooden cutlery sets.", price_per_piece=0.80, badge="Eco"),
]

db = SessionLocal()
try:
    if db.query(Product).count() == 0:
        db.bulk_insert_mappings(Product, CATALOG)
        db.commit()
        print(f"Seeded {len(CATALOG)} products.")
    else:
        print("Products table already has data — skipping seed.")
finally:
    db.close()
