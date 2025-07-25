from datetime import datetime
from fastapi import FastAPI, Body
from gam_service import get_orders, create_order, create_bulk_line_items

app = FastAPI()

@app.get("/orders/automation-test")
def test_get_equivalent():
    return create_order_and_line_items()


@app.get("/")
def health_check():
    return {"status": "ok"}

@app.get("/orders")
def list_orders():
    try:
        orders = get_orders()
        return {"orders": [o['name'] for o in orders]}
    except Exception as e:
        return {"error": str(e)}

@app.post("/orders/automation-test")
def create_order_and_line_items():
    try:
        advertiser_id = 34005580
        trafficker_id = 134593300

        # ✅ Generate a unique order name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        order_name = f"jpenumaka_automation_test_{timestamp}"

        # Step 1: Create order
        order_id = create_order(order_name, advertiser_id, trafficker_id)

        # Step 2: Create 10 line items with CPMs increasing by $1
        line_item_ids = create_bulk_line_items(order_id, base_name="JP Floor Test")

        return {
            "order_name": order_name,
            "order_id": order_id,
            "line_item_ids": line_item_ids
        }

    except Exception as e:
        return {"error": str(e)}