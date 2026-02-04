import pytest
from rest_framework.test import APIClient
from apps.products.models import Category, Product

@pytest.mark.django_db
def test_product_search_by_keyword():
    client = APIClient()

    category = Category.objects.create(name="Tech")
    Product.objects.create(
        title="Laptop", price=1000, category=category
    )

    response = client.get("/api/search/products/?q=laptop")

    assert response.status_code == 200
    assert response.data["count"] == 1
