from rest_framework import serializers
from apps.orders.models import Order, OrderItem


class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    store_id = serializers.IntegerField()
    items = OrderItemInputSerializer(many=True)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity_requested"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "status", "created_at", "items"]

class StoreOrderListSerializer(serializers.ModelSerializer):
    total_items = serializers.IntegerField()

    class Meta:
        model = Order
        fields = ["id", "status", "created_at", "total_items"]
