import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.products.models import Category, Product
from apps.stores.models import Store, Inventory
from apps.orders.models import Order

@pytest.mark.django_db
def test_order_rejected_when_insufficient_stock():
    client = APIClient()

    category = Category.objects.create(name="Books")
    product = Product.objects.create(
        title="Django Book", price=50, category=category
    )
    store = Store.objects.create(name="Store B", location="LA")
    Inventory.objects.create(store=store, product=product, quantity=1)

    response = client.post(
        "/orders/",
        {
            "store_id": store.id,
            "items": [{"product_id": product.id, "quantity": 5}],
        },
        format="json",
    )

    assert response.data["status"] == Order.STATUS_REJECTED
