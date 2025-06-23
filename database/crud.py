from sqlalchemy.orm import Session
from database.models import Customer, Product, Order, OrderItem

def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()

def get_customers(db: Session):
    return db.query(Customer).all()

def create_customer(db: Session, customer: Customer):
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def update_customer(db: Session, customer: Customer):
    db.merge(customer)
    db.commit()
    return customer

def delete_customer(db: Session, customer: Customer):
    db.delete(customer)
    db.commit()

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session):
    return db.query(Product).all()

def create_product(db: Session, product: Product):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update_product(db: Session, product: Product):
    db.merge(product)
    db.commit()
    return product

def delete_product(db: Session, product: Product):
    db.delete(product)
    db.commit()

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def get_orders(db: Session):
    return db.query(Order).all()

def create_order(db: Session, order: Order):
    db.add(order)
    db.commit()
    db.refresh(order)
    for item in order.order_items:
        db.refresh(item)
    return order

def update_order(db: Session, order: Order):
    db.merge(order)
    db.commit()
    return order

def delete_order(db: Session, order: Order):
    db.delete(order)
    db.commit()

def get_total_sales(db: Session):
    return db.query(db.func.sum(Order.total)).scalar()

def get_top_product(db: Session):
    return db.query(Product).join(OrderItem).join(Order).\
        group_by(Product.id).\
        order_by(db.func.sum(OrderItem.quantity).desc()).first()

def get_top_customer(db: Session):
    return db.query(Customer).join(Order).\
        group_by(Customer.id).\
        order_by(db.func.sum(Order.total).desc()).first()
