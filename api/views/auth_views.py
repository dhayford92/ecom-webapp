from api.serializers.auth_serializers import LoginSerializer, ProfileSerializer, RegisterSerializer
from authentication.models import User, Profile
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import authenticate


class RegisterApiView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
            email = request.data.get('email', None)
            password = request.data.get('password', None)
            user = authenticate(email=email, password=password)
            
            if user:
                serializer = self.serializer_class(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid Credentail, Please again!'}, status=status.HTTP_401_UNAUTHORIZED)
        
        


class ProfileAPIView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated(),]
    

class ProfileDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated(),]