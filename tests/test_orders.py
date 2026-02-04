import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.products.models import Category, Product
from apps.stores.models import Store, Inventory
from apps.orders.models import Order


@pytest.mark.django_db
def test_order_confirmed_when_stock_sufficient():
    client = APIClient()

    category = Category.objects.create(name="Electronics")
    product = Product.objects.create(
        title="Phone", price=500, category=category
    )
    store = Store.objects.create(name="Store A", location="NY")
    Inventory.objects.create(store=store, product=product, quantity=10)

    response = client.post(
        "/orders/",
        {
            "store_id": store.id,
            "items": [{"product_id": product.id, "quantity": 2}],
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["status"] == Order.STATUS_CONFIRMED
