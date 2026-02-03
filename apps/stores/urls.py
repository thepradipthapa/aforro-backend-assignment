from django.urls import path
from apps.stores.views import StoreInventoryListAPIView

urlpatterns = [
    path("stores/<int:store_id>/inventory/", StoreInventoryListAPIView.as_view()),
]
