from django.db import transaction
from django.db.models import F
from apps.orders.models import Order, OrderItem
from apps.stores.models import Inventory


@transaction.atomic
def create_order(store, items):
    """
    items: list of dicts -> [{product_id, quantity}]
    """

    order = Order.objects.create(
        store=store,
        status=Order.STATUS_PENDING
    )

    # Lock inventory rows for this store + products
    product_ids = [item["product_id"] for item in items]

    inventories = (
        Inventory.objects
        .select_for_update()
        .filter(store=store, product_id__in=product_ids)
    )

    inventory_map = {
        inv.product_id: inv for inv in inventories
    }

    # Validate stock
    for item in items:
        product_id = item["product_id"]
        qty = item["quantity"]

        inventory = inventory_map.get(product_id)
        if not inventory or inventory.quantity < qty:
            order.status = Order.STATUS_REJECTED
            order.save(update_fields=["status"])
            return order

    # Deduct stock + create order items
    for item in items:
        inventory = inventory_map[item["product_id"]]
        inventory.quantity = F("quantity") - item["quantity"]
        inventory.save(update_fields=["quantity"])

        OrderItem.objects.create(
            order=order,
            product_id=item["product_id"],
            quantity_requested=item["quantity"]
        )

    order.status = Order.STATUS_CONFIRMED
    order.save(update_fields=["status"])

    return order
