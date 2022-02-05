from api.serializers.product_serializers import *
from rest_framework import generics, permissions
from store.models import *


#category list
class CategoryApiView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = ProductCategory.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    
    
#product list
class ProductApiView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    filter_queryset = ['category']
    
    
#product image
class ProductImageApiView(generics.ListAPIView):
    serializer_class = ImageSerializer
    queryset = ProductsImage.objects.all()
    filter_queryset = ['product']
    
    
#Product variation list    
class ProductVariationApiView(generics.ListAPIView):
    serializer_class = VariationSerializer
    queryset = Variation.objects.all()
    filter_queryset = ['product']
    
    
 #add and lis favorite   
class AddListFavoriteApiView(generics.ListCreateAPIView):
    serializer_class = AddRemoveFavoriteSerializer
    queryset = Favorite.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    
    def perform_create(self, request):
        return self.serializer_class.save(user=request.user)
    

# remove from favorite    
class RemoveFromFavoriteApiView(generics.DestroyAPIView):
    serializer_class = AddRemoveFavoriteSerializer
    queryset = Favorite.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


# -- Product review
class ProductReviewApiView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    
    def perform_create(self):
        return self.serializer_class.save()