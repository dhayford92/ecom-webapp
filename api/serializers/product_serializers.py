from rest_framework import serializers
from store.models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        depth = 1
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsImage
        depth = 1
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        depth = 1
        fields = '__all__'


class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        depth = 1
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'
        
        
        
class AddRemoveFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        depth = 1
        fields = '__all__'
        read_only_fields = ['id']