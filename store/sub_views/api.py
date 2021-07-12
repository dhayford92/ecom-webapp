from rest_framework import generics
from store.models import*
from store.serializers import*


class ProductView(generics.ListAPIView):
    quaryset = Product
    class_serializer = ProductSerializer


class ImageView(generics.ListAPIView):
    quaryset = ProductsImage
    class_serializer = ImageSerializer


class CategoryView(generics.ListAPIView):
    quaryset = ProductCategory
    class_serializer = CategorySerializer


class ReviewView(generics.ListAPIView):
    quaryset = ProductReview
    class_serializer = ReviewSerializer


class VariationView(generics.ListAPIView):
    quaryset = Variation
    class_serializer = VariationSerializer