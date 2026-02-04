from django.db.models import Q, F, Value, IntegerField
from django.db.models.functions import Coalesce
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache

from apps.products.models import Product
from apps.stores.models import Inventory
from apps.search.serializers import ProductSearchSerializer

class ProductSearchPagination(PageNumberPagination):
    page_size = 10

class ProductSearchAPIView(APIView):
    def get(self, request):
        params = request.query_params
        cache_key = f"product_search:{params.urlencode()}"

        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        qs = Product.objects.select_related("category")

        # Keyword search
        q = params.get("q")
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(category__name__icontains=q)
            )

        # Filters
        if params.get("category"):
            qs = qs.filter(category__name=params["category"])

        if params.get("min_price"):
            qs = qs.filter(price__gte=params["min_price"])

        if params.get("max_price"):
            qs = qs.filter(price__lte=params["max_price"])

        store_id = params.get("store_id")
        in_stock = params.get("in_stock")

        if store_id:
            qs = qs.annotate(
                inventory_quantity=Coalesce(
                    Inventory.objects.filter(
                        store_id=store_id,
                        product_id=F("id")
                    ).values("quantity")[:1],
                    Value(0),
                    output_field=IntegerField()
                )
            )

            if in_stock == "true":
                qs = qs.filter(inventory_quantity__gt=0)

        # Sorting
        sort = params.get("sort")

        if sort == "price":
            qs = qs.order_by("price")
        elif sort == "newest":
            qs = qs.order_by("-created_at")
        else:
            qs = qs.order_by("-created_at")
            
        paginator = ProductSearchPagination()
        page = paginator.paginate_queryset(qs, request)

        data = ProductSearchSerializer(page, many=True).data
        response = paginator.get_paginated_response(data).data

        cache.set(cache_key, response, timeout=60)  

        return Response(response)


class ProductSuggestAPIView(APIView):
    def get(self, request):
        q = request.query_params.get("q", "").strip()

        if len(q) < 3:
            return Response([])

        cache_key = f"product_suggest:{q}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        prefix_matches = list(
            Product.objects
            .filter(title__istartswith=q)
            .values_list("title", flat=True)[:10]
        )

        remaining = 10 - len(prefix_matches)

        contains_matches = []
        if remaining > 0:
            contains_matches = list(
                Product.objects
                .filter(title__icontains=q)
                .exclude(title__istartswith=q)
                .values_list("title", flat=True)[:remaining]
            )

        results = prefix_matches + contains_matches

        cache.set(cache_key, results, timeout=300) 

        return Response(results)
