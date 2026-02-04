from celery import shared_task
from apps.orders.models import Order
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_order_confirmation(order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        logger.warning(f"Order {order_id} not found")
        return

    # Simulate sending email / notification
    logger.info(
        f"Order {order.id} confirmed for store {order.store.name}"
    )
