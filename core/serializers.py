# serializers.py
from rest_framework import serializers
from .models import CustomUser
from django.utils import translation
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from a_base.serializers import DistrictSerializer, SubscriptionSerializer, GenderSerializer
from a_base.models import District

User = get_user_model()

class GroupSerializer(serializers.Serializer):
    name = serializers.CharField()

class CustomUserSerializer(serializers.ModelSerializer):
    district = DistrictSerializer(read_only=True)
    groups = GroupSerializer(many=True, read_only=True)
    subscription = SubscriptionSerializer(read_only=True)
    gender = GenderSerializer(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserShortSerializer(serializers.ModelSerializer):
    district = DistrictSerializer(read_only=True)
    gender = GenderSerializer()
    
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'profile_picture', 'gender', 'district']


# Сериализатор для регистрации нового пользователя
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    district = serializers.PrimaryKeyRelatedField(
        queryset=District.objects.all(),
        write_only=True,
        required=True
    )
    class Meta:
        model = User
        fields = ['first_name', 'phone_number', 'date_of_birth', 'district', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['phone_number'] = user.phone_number
        token['group'] = list(user.groups.values_list("name", flat=True)) if user.groups else None
        token['subscription'] = user.subscription.name if user.subscription else None
        
        return token