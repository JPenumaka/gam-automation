from googleads import ad_manager
from datetime import datetime, timedelta
from config import API_VERSION

def get_client():
    return ad_manager.AdManagerClient.LoadFromStorage('googleads.yaml')

def get_orders():
    client = get_client()
    order_service = client.GetService('OrderService', version=API_VERSION)

    statement = ad_manager.StatementBuilder(version=API_VERSION).Limit(10)
    response = order_service.getOrdersByStatement(statement.ToStatement())

    return response['results'] if 'results' in response else []

def create_order(name: str, advertiser_id: int, trafficker_id: int):
    client = get_client()
    order_service = client.GetService("OrderService", version=API_VERSION)
    order = {
        "name": name,
        "advertiserId": advertiser_id,
        "traffickerId": trafficker_id
    }
    created = order_service.createOrders([order])
    return created[0]["id"]

def create_bulk_line_items(order_id: int, base_name: str = "Test Line Item"):
    client = get_client()
    line_item_service = client.GetService("LineItemService", version=API_VERSION)
    inventory_service = client.GetService("InventoryService", version=API_VERSION)

    # Get root ad unit
    statement = ad_manager.StatementBuilder(version=API_VERSION).Limit(1)
    response = inventory_service.getAdUnitsByStatement(statement.ToStatement())
    root_ad_unit_id = response["results"][0]["id"]

    # Set dynamic future start and end times to avoid "startDateTime is in the past" error
    now = datetime.utcnow()
    start_date = now + timedelta(minutes=5)
    end_date = start_date + timedelta(days=30)

    start_datetime = {
        "date": {
            "year": start_date.year,
            "month": start_date.month,
            "day": start_date.day
        },
        "hour": start_date.hour,
        "minute": start_date.minute,
        "second": start_date.second,
        "timeZoneId": "America/Los_Angeles"
    }

    end_datetime = {
        "date": {
            "year": end_date.year,
            "month": end_date.month,
            "day": end_date.day
        },
        "hour": end_date.hour,
        "minute": end_date.minute,
        "second": end_date.second,
        "timeZoneId": "America/Los_Angeles"
    }

    line_items = []

    for i in range(1, 11):  # Create 10 line items with CPM $1–$10
        line_item = {
            "name": f"{base_name} ${i}",
            "orderId": order_id,
            "targeting": {
                "inventoryTargeting": {
                    "targetedAdUnits": [{"adUnitId": root_ad_unit_id}]
                }
            },
            "lineItemType": "STANDARD",
            "allowOverbook": True,
            "startDateTime": start_datetime,
            "endDateTime": end_datetime,
            "primaryGoal": {
                "goalType": "LIFETIME",
                "unitType": "IMPRESSIONS",
                "units": 10000
            },
            "costType": "CPM",
            "costPerUnit": {
                "currencyCode": "USD",
                "microAmount": i * 1_000_000  # $1 CPM = 1,000,000 micros
            },
            "creativePlaceholders": [{
                "size": {"width": 300, "height": 250}
            }]
        }

        line_items.append(line_item)

    created = line_item_service.createLineItems(line_items)
    return [li["id"] for li in created]
