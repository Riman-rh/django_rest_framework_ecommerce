import coreapi
from django.utils.decorators import method_decorator

from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from elasticsearch_dsl import Search
import elasticsearch
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


ELASTIC_HOST = 'http://localhost:9200'
client = elasticsearch.Elasticsearch(hosts=[ELASTIC_HOST])
INDEXES = ['products_1']
id_param = openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)

''''
def get_x_content(query, index=INDEXES, fields=['name_en', 'description', 'comment']):
    if not query:
        return
    hits = Search(index=index).using(client).query("multi_match", fields=fields, fuzziness='AUTO',
                                                   query=query)
    print(hits)
    results = []
    for hit in hits:
        data = {
            'id': hit.id,
            'category': hit.category,
            'name_ar': hit.name_ar,
            'name_en': hit.name_en,
            'name_fr': hit.name_fr
        }
        results.append(data)
        
    return results
'''

@api_view(['POST'])
def registration(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    return Response(serializer.errors)


@api_view(['GET'])
def category_list(request):
    category = Category.objects.all()
    serializer = CategoryListSerializer(category, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='get', manual_parameters=[id_param])
@api_view(['GET'])
def product_list(request):

    req = ProductListreqSerializer(data=request.data)
    if req.is_valid():
        try:
            category = Category.objects.get(id=req.data['id'])
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        products = Product.objects.filter(category=category.id)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)
    return Response('not valid')


@swagger_auto_schema(method='post', manual_parameters=[
    openapi.Parameter('category', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    openapi.Parameter('name_ar', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    openapi.Parameter('name_en', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    openapi.Parameter('name_fr', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    openapi.Parameter('photo', openapi.IN_QUERY, type=openapi.TYPE_FILE),
    openapi.Parameter('description', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    openapi.Parameter('stock', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
],)
@api_view(['POST'])
def product_create(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', manual_parameters=[id_param])
@api_view(['GET'])
def product_get(request):
    req = ProductGetSerializer(data=request.data)
    if req.is_valid():
        try:
            product = Product.objects.get(id=req.data['id'])
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductListSerializer(product, many=False)
        return Response(serializer.data)
    return Response("not valid")


@swagger_auto_schema(method='get', manual_parameters=[id_param])
@api_view(['GET'])
def review_list(request):
    req = ProductGetSerializer(data=request.data)
    if req.is_valid():
        try:
            product = Product.objects.get(id=req.data["id"])
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        reviews = Review.objects.filter(product=product.id)
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)
    return Response('not valid')


@swagger_auto_schema(method='post', manual_parameters=[
    openapi.Parameter('owner', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    openapi.Parameter('product', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    openapi.Parameter('rating', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    openapi.Parameter('comment', openapi.IN_QUERY, type=openapi.TYPE_STRING),
],)
@api_view(['POST'])
def review_create(request):
    if request.user.is_authenticated:
        serializer = ReviewListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(method='post', manual_parameters=[
    openapi.Parameter('product', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    openapi.Parameter('quantity', openapi.IN_QUERY, type=openapi.TYPE_STRING),

],)
@api_view(['POST'])
def orderProcess(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(owner=request.user, complete=False)
        print(request.data)
        for data in request.data:
            serializer = OrderItemSerializer(data=data)
            if serializer.is_valid():
                serializer.save(order=order)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(method='post', manual_parameters=[id_param])
@api_view(['POST'])
def orderComplete(request):
    if request.user.is_superuser:
        req = OrderGetSerializer(data=request.data)
        if req.is_valid():
            order = Order.objects.get(id=req.data["id"])
            order.complete = True
            order.save()
            return Response('ok')
        return Response('not valid')
    return Response(status=status.HTTP_401_UNAUTHORIZED)


