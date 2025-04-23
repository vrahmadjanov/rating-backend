# serializers.py
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from a_base.serializers import CitySerializer
from a_base.models import City

User = get_user_model()

class GroupSerializer(serializers.Serializer):
    name = serializers.CharField()

class SubscriptionSerializer(serializers.Serializer):
    name = serializers.CharField()

class CustomUserSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    groups = GroupSerializer(many=True, read_only=True)
    subscription = SubscriptionSerializer(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'groups': {'read_only': True},
        }

    def update(self, instance, validated_data):
        # Убираем возможность изменения группы и прав через API
        validated_data.pop('groups', None)
        validated_data.pop('user_permissions', None)
        return super().update(instance, validated_data)

class CustomUserShortSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'profile_picture', 'gender', 'city']


# Сериализатор для регистрации нового пользователя
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        write_only=True,
        required=True
    )
    class Meta:
        model = User
        fields = ['first_name', 'phone_number', 'date_of_birth', 'city', 'password']

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