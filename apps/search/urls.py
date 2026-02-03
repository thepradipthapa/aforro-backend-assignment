from django.urls import path
from apps.search.views import ProductSearchAPIView, ProductSuggestAPIView

urlpatterns = [
    path("api/search/products/", ProductSearchAPIView.as_view()),
    path("api/search/suggest/", ProductSuggestAPIView.as_view()),
]
