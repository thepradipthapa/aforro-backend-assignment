from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.orders.serializers import OrderCreateSerializer, OrderSerializer, StoreOrderListSerializer
from apps.orders.services import create_order
from apps.stores.models import Store
from django.db.models import Count
from rest_framework.generics import ListAPIView
from apps.orders.models import Order


class OrderCreateAPIView(APIView):
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        store = Store.objects.get(id=serializer.validated_data["store_id"])
        items = serializer.validated_data["items"]

        order = create_order(store=store, items=items)

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )

class StoreOrderListAPIView(ListAPIView):
    serializer_class = StoreOrderListSerializer

    def get_queryset(self):
        store_id = self.kwargs["store_id"]
        return (
            Order.objects
            .filter(store_id=store_id)
            .annotate(total_items=Count("items"))
            .order_by("-created_at")
        )