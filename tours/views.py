from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Tour, TourToken
from .serializers import FormDataSerializer, LoginSerializer, UserSerializer

def index(request):
    return HttpResponse('hello')

class FormDataView(APIView):
    def post(self, request):
        serializer = FormDataSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "success": True,
                "message": "User created successfully",
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            user = validated_data["user"]
            
            return Response({
                "success": True,
                "message": "Login successful",
                "data": {
                    "token": validated_data["token"],
                    "role": user.role,
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "phone": user.phone,
                        "company": user.company,
                    }
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "success": False,
            "message": "Invalid credentials",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        # Get token from Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Token '):
            return Response({
                "success": False,
                "message": "No token provided"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        token_key = auth_header.split(' ')[1]
        
        try:
            token = TourToken.objects.get(key=token_key)
            token.delete()
            return Response({
                "success": True,
                "message": "Logged out successfully"
            }, status=status.HTTP_200_OK)
        except TourToken.DoesNotExist:
            return Response({
                "success": False,
                "message": "Invalid token"
            }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def validate_token(request):
    """Endpoint to validate if a token is still valid"""
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header or not auth_header.startswith('Token '):
        return Response({
            "valid": False,
            "message": "No token provided"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    token_key = auth_header.split(' ')[1]
    
    try:
        token = TourToken.objects.get(key=token_key)
        user = token.user
        
        if not user.is_active:
            return Response({
                "valid": False,
                "message": "User is inactive"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "valid": True,
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)
        
    except TourToken.DoesNotExist:
        return Response({
            "valid": False,
            "message": "Invalid token"
        }, status=status.HTTP_400_BAD_REQUEST)

# Protected view example
@api_view(['GET'])
def protected_view(request):
    """Example of a protected endpoint that requires token authentication"""
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header or not auth_header.startswith('Token '):
        return Response({
            "error": "Authentication required"
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    token_key = auth_header.split(' ')[1]
    
    try:
        token = TourToken.objects.get(key=token_key)
        user = token.user
        
        return Response({
            "message": f"Hello {user.name}!",
            "user_role": user.role,
            "protected_data": "This is protected content"
        })
        
    except TourToken.DoesNotExist:
        return Response({
            "error": "Invalid token"
        }, status=status.HTTP_401_UNAUTHORIZED)
from rest_framework import generics
from .models import Booking
from .serializers import BookingSerializer

class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Log serializer errors for debugging
        print("Booking validation errors:", serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import viewsets
from .models import SafariPackage
from .serializers import SafariPackageSerializer

class SafariPackageViewSet(viewsets.ModelViewSet):
    queryset = SafariPackage.objects.all()
    serializer_class = SafariPackageSerializer
    
    
from rest_framework.parsers import MultiPartParser, FormParser
class SafariPackageCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser)  # Handle multipart/form-data

    def post(self, request, *args, **kwargs):
        print("Request data:", request.data)  # Debug incoming request
        serializer = SafariPackageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("Serializer errors:", serializer.errors)  # Debug errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    