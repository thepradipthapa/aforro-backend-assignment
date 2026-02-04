import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.products.models import Category, Product
from apps.stores.models import Store, Inventory
from apps.orders.models import Order

@pytest.mark.django_db
def test_inventory_listing_sorted():
    client = APIClient()

    category = Category.objects.create(name="Food")
    store = Store.objects.create(name="Store C", location="TX")

    p1 = Product.objects.create(title="Apple", price=1, category=category)
    p2 = Product.objects.create(title="Banana", price=1, category=category)

    Inventory.objects.create(store=store, product=p2, quantity=5)
    Inventory.objects.create(store=store, product=p1, quantity=5)

    response = client.get(f"/stores/{store.id}/inventory/")

    titles = [item["product_title"] for item in response.data]
    assert titles == ["Apple", "Banana"]
