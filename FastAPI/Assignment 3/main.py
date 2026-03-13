from fastapi import FastAPI, Query, Response, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

# ── Temporary data — acting as our database for now ──────────
products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True },
    {'id': 2, 'name': 'Notebook',       'price':  99,  'category': 'Stationery',  'in_stock': True },
    {'id': 3, 'name': 'USB Hub',        'price': 799,  'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set',        'price':  49,  'category': 'Stationery',  'in_stock': True },
    {'id': 5, 'name': 'Laptop Stand',   'price': 1299, 'category': 'Electronics', 'in_stock': True },
    {'id': 6, 'name': 'Mechanical Keyboard', 'price': 2499, 'category': 'Electronics', 'in_stock': True },
    {'id': 7, 'name': 'Webcam',         'price': 1899, 'category': 'Electronics', 'in_stock': False},
]

# ── Orders list (for Q5 and Bonus) ────────────────────────────
orders = []
order_counter = 0

# ── Feedback list (for Q3) ────────────────────────────────────
feedback = []

# ── Pydantic Model for Adding New Product ────────────────────
class NewProduct(BaseModel):
    name:        str           = Field(..., min_length=1, max_length=100)
    price:       int           = Field(..., gt=0)
    category:    str           = Field(..., min_length=1, max_length=50)
    in_stock:    bool          = Field(default=True)

# ── Pydantic Models for Q3 ────────────────────────────────────
class CustomerFeedback(BaseModel):
    customer_name: str            = Field(..., min_length=2, max_length=100)
    product_id:   int             = Field(..., gt=0)
    rating:       int             = Field(..., ge=1, le=5)
    comment:      Optional[str]   = Field(None, max_length=300)

# ── Pydantic Models for Q5 ────────────────────────────────────
class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity:   int = Field(..., gt=0, le=50)

class BulkOrder(BaseModel):
    company_name:  str           = Field(..., min_length=2)
    contact_email: str           = Field(..., min_length=5)
    items:         List[OrderItem] = Field(..., min_length=1)

# ── Pydantic Model for Orders (Bonus) ─────────────────────────
class OrderRequest(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity:   int = Field(..., gt=0, le=10)

# ── Helper function to find product by ID ─────────────────────
def find_product(product_id: int):
    for product in products:
        if product['id'] == product_id:
            return product
    return None

def find_product_by_name(name: str):
    for product in products:
        if product['name'].lower() == name.lower():
            return product
    return None

# ── Endpoint 0 — Home ────────────────────────────────────────
@app.get('/')
def home():
    return {'message': 'Welcome to FastAPI Day 2 - Advanced Endpoints'}

# ── GET /products — Get all products ─────────────────────────
@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}

# ── SPECIFIC ROUTES (MUST COME BEFORE PARAMETERIZED ROUTES) ──
@app.get('/products/filter')
def filter_products(
    category:  Optional[str] = Query(None, description='Electronics or Stationery'),
    max_price: Optional[int] = Query(None, description='Maximum price'),
    in_stock:  Optional[bool] = Query(None, description='True = in stock only'),
    min_price: Optional[int] = Query(None, description='Minimum price')
):
    result = products
    
    if category:
        result = [p for p in result if p['category'] == category]
    
    if max_price is not None:
        result = [p for p in result if p['price'] <= max_price]
    
    if in_stock is not None:
        result = [p for p in result if p['in_stock'] == in_stock]
    
    if min_price is not None:
        result = [p for p in result if p['price'] >= min_price]
    
    return {'filtered_products': result, 'count': len(result)}

@app.get('/products/audit')
def product_audit():
    in_stock_list = [p for p in products if p['in_stock']]
    out_stock_list = [p for p in products if not p['in_stock']]
    stock_value = sum(p['price'] * 10 for p in in_stock_list)
    priciest = max(products, key=lambda p: p['price'])
    
    return {
        'total_products': len(products),
        'in_stock_count': len(in_stock_list),
        'out_of_stock_names': [p['name'] for p in out_stock_list],
        'total_stock_value': stock_value,
        'most_expensive': {'name': priciest['name'], 'price': priciest['price']}
    }

@app.get('/products/summary')
def product_summary():
    in_stock = [p for p in products if p['in_stock']]
    out_stock = [p for p in products if not p['in_stock']]
    expensive = max(products, key=lambda p: p['price'])
    cheapest = min(products, key=lambda p: p['price'])
    categories = list(set(p['category'] for p in products))
    
    return {
        'total_products': len(products),
        'in_stock_count': len(in_stock),
        'out_of_stock_count': len(out_stock),
        'most_expensive': {'name': expensive['name'], 'price': expensive['price']},
        'cheapest': {'name': cheapest['name'], 'price': cheapest['price']},
        'categories': categories,
    }

@app.put('/products/discount')
def bulk_discount(
    category: str = Query(..., description='Category to discount'),
    discount_percent: int = Query(..., ge=1, le=99, description='% off')
):
    updated = []
    
    for p in products:
        if p['category'].lower() == category.lower():
            old_price = p['price']
            p['price'] = int(old_price * (1 - discount_percent / 100))
            updated.append({
                'id': p['id'],
                'name': p['name'],
                'old_price': old_price,
                'new_price': p['price']
            })
    
    if not updated:
        return {'message': f'No products found in category: {category}'}
    
    return {
        'message': f'{discount_percent}% discount applied to {category}',
        'updated_count': len(updated),
        'updated_products': updated
    }

@app.get('/products/{product_id}/price')
def get_product_price(product_id: int):
    for product in products:
        if product['id'] == product_id:
            return {'name': product['name'], 'price': product['price']}
    return {'error': 'Product not found'}

# ── PARAMETERIZED ROUTES (MUST COME LAST) ─────────────────────
@app.get('/products/{product_id}')
def get_product(product_id: int):
    product = find_product(product_id)
    
    if not product:
        raise HTTPException(status_code=404, detail={'error': 'Product not found'})
    
    return {'product': product}

@app.put('/products/{product_id}')
def update_product(product_id: int, price: Optional[int] = None, in_stock: Optional[bool] = None):
    product = find_product(product_id)
    
    if not product:
        raise HTTPException(status_code=404, detail={'error': 'Product not found'})
    
    # Update only the fields that were provided
    if price is not None:
        product['price'] = price
    
    if in_stock is not None:
        product['in_stock'] = in_stock
    
    return {
        'message': 'Product updated',
        'product': product
    }

@app.delete('/products/{product_id}')
def delete_product(product_id: int, response: Response):
    product = find_product(product_id)
    
    if not product:
        response.status_code = 404
        return {'error': 'Product not found'}
    
    products.remove(product)
    return {'message': f"Product '{product['name']}' deleted"}

# ── Q1: POST /products — Add new product ─────────────────────
@app.post('/products')
def add_product(new_product: NewProduct):
    # Check for duplicate name
    existing = find_product_by_name(new_product.name)
    if existing:
        raise HTTPException(
            status_code=400,
            detail={'error': f"Product with name '{new_product.name}' already exists"}
        )
    
    # Generate new ID
    next_id = max(p['id'] for p in products) + 1
    
    product_data = {
        'id': next_id,
        'name': new_product.name,
        'price': new_product.price,
        'category': new_product.category,
        'in_stock': new_product.in_stock
    }
    
    products.append(product_data)
    
    return {
        'message': 'Product added',
        'product': product_data
    }

# ── Feedback Endpoint ─────────────────────────────────────────
@app.post('/feedback')
def submit_feedback(data: CustomerFeedback):
    feedback.append(data.dict())
    return {
        'message': 'Feedback submitted successfully',
        'feedback': data.dict(),
        'total_feedback': len(feedback),
    }

# ── Q5: Bulk Order Processing ────────────────────────────────
@app.post('/orders/bulk')
def place_bulk_order(order: BulkOrder):
    confirmed = []
    failed = []
    grand_total = 0
    
    for item in order.items:
        product = next((p for p in products if p['id'] == item.product_id), None)
        
        if not product:
            failed.append({
                'product_id': item.product_id,
                'reason': 'Product not found'
            })
        elif not product['in_stock']:
            failed.append({
                'product_id': item.product_id,
                'reason': f"{product['name']} is out of stock"
            })
        else:
            subtotal = product['price'] * item.quantity
            grand_total += subtotal
            confirmed.append({
                'product': product['name'],
                'qty': item.quantity,
                'subtotal': subtotal
            })
    
    return {
        'company': order.company_name,
        'confirmed': confirmed,
        'failed': failed,
        'grand_total': grand_total
    }

# ── BONUS: Order Status Tracker ──────────────────────────────
@app.post('/orders')
def place_order(order_data: OrderRequest):
    global order_counter
    order_counter += 1
    
    product = next((p for p in products if p['id'] == order_data.product_id), None)
    
    if not product:
        return {'error': 'Product not found'}
    
    if not product['in_stock']:
        return {'error': f"{product['name']} is out of stock"}
    
    total_price = product['price'] * order_data.quantity
    
    new_order = {
        'order_id': order_counter,
        'product_id': order_data.product_id,
        'product_name': product['name'],
        'quantity': order_data.quantity,
        'total_price': total_price,
        'status': 'pending'
    }
    
    orders.append(new_order)
    
    return {
        'message': 'Order placed successfully (pending confirmation)',
        'order': new_order
    }

@app.get('/orders/{order_id}')
def get_order(order_id: int):
    for order in orders:
        if order['order_id'] == order_id:
            return {'order': order}
    return {'error': 'Order not found'}

@app.patch('/orders/{order_id}/confirm')
def confirm_order(order_id: int):
    for order in orders:
        if order['order_id'] == order_id:
            order['status'] = 'confirmed'
            return {
                'message': 'Order confirmed',
                'order': order
            }
    return {'error': 'Order not found'}
