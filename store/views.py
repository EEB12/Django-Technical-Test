from django.core.cache import cache
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from django.utils.timezone import now
class CategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        cache_key = 'store:categories'
        categories = cache.get(cache_key)

        if categories:
            print(f"[{now()}] Cache hit: {cache_key}")
        else:
            print(f"[{now()}] Cache miss: {cache_key}")
            # Fetch data from the database
            queryset = Category.objects.all()
            # Serialize the data
            serializer = CategorySerializer(queryset, many=True)
            categories = serializer.data
            # Store serialized data in the cache
            cache.set(cache_key, categories, timeout=300)

        return Response(categories)
    def retrieve(self, request, pk=None):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('store:categories')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('store:categories')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        category = Category.objects.get(pk=pk)
        category.delete()
        cache.delete('store:categories')
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        # Define cache key
        cache_key = 'store:products'
        products = cache.get(cache_key)

        if products:
            print(f"[{now()}] Cache hit: {cache_key}")
        else:
            print(f"[{now()}] Cache miss: {cache_key}")

            # Fetch all products from the database
            queryset = Product.objects.all()

            # Apply filters if query parameters are provided
            category_filter = request.query_params.get('category')
            price_min = request.query_params.get('price_min')
            price_max = request.query_params.get('price_max')

            if category_filter:
                queryset = queryset.filter(category__name=category_filter)
            if price_min:
                queryset = queryset.filter(price__gte=price_min)
            if price_max:
                queryset = queryset.filter(price__lte=price_max)

            # Serialize the data
            serializer = ProductSerializer(queryset, many=True)
            products = serializer.data

            # Cache the serialized data
            cache.set(cache_key, products, timeout=300)

        return Response(products)

    def retrieve(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('store:products')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('store:products')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        product.delete()
        cache.delete('store:products')
        return Response(status=status.HTTP_204_NO_CONTENT)
