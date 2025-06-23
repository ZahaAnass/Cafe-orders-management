def validate_customer(name, phone, email):
    if not name or not phone or not email:
        return False
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        return False
    return True

def validate_order_item(product, quantity, price):
    if not product or not quantity or not price:
        return False
    if not re.match(r"^[a-zA-Z0-9_]+$", product):
        return False
    if not re.match(r"^\d+$", quantity):
        return False
    if not re.match(r"^\d+(\.\d+)?$", price):
        return False
    return True

def validate_order_status(status):
    if status not in ["Pending", "Preparing", "Served", "Paid"]:
        return False
    return True
