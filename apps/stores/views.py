from rest_framework.generics import ListAPIView
from apps.stores.models import Inventory
from apps.stores.serializers import InventorySerializer


class StoreInventoryListAPIView(ListAPIView):
    serializer_class = InventorySerializer

    def get_queryset(self):
        store_id = self.kwargs["store_id"]
        return (
            Inventory.objects
            .filter(store_id=store_id)
            .select_related("product", "product__category")
            .order_by("product__title")
        )
