from rest_framework import serializers
from .models import Tour, TourToken
from django.contrib.auth.hashers import check_password

class FormDataSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Tour
        fields = ['name', 'email', 'phone', 'password', 'company', 'role']
    
    def create(self, validated_data):
        # Password will be hashed automatically in the model's save method
        return Tour.objects.create(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        try:
            user = Tour.objects.get(email=email, is_active=True)
        except Tour.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist or is inactive.")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password.")
        
        # Get or create token
        token, created = TourToken.objects.get_or_create(user=user)
        
        return {
            "user": user,
            "token": token.key,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        }

class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data (excluding password)"""
    class Meta:
        model = Tour
        fields = ['id', 'name', 'email', 'phone', 'company', 'role', 'date_created']
from .models import Booking

from rest_framework import serializers
from .models import Booking, SafariPackage  # Make sure SafariPackage is imported

class BookingSerializer(serializers.ModelSerializer):
    safari_package = serializers.PrimaryKeyRelatedField(queryset=SafariPackage.objects.all())

    class Meta:
        model = Booking
        fields = '__all__'
from .models import SafariPackage

# class SafariPackageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SafariPackage
#         fields = '__all__'        

class SafariPackageSerializer(serializers.ModelSerializer):
    def validate(self, data):
        print("Received data:", data)  # Debug incoming data
        return data

    class Meta:
        model = SafariPackage
        fields = ['id', 'name', 'description', 'group_size_min', 'group_size_max', 'picture']        