from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from a_base.serializers import DistrictSerializer, SubscriptionSerializer, GenderSerializer, GroupSerializer
from a_base.models import District, Gender

User = get_user_model()

class CustomUserPrivateSerializer(serializers.ModelSerializer):
    """Приватный сериализатор для обновления данных"""
    district = DistrictSerializer(read_only=True)
    gender = GenderSerializer(read_only=True)
    groups = GroupSerializer(many=True, read_only=True)
    subscription = SubscriptionSerializer(read_only=True)

    gender_id = serializers.PrimaryKeyRelatedField(
        queryset=Gender.objects.all(),
        source='gender',
        write_only=True,
        allow_null=True,
        required=False
    )

    class Meta:
        model = CustomUser
        fields = [
            'id', 'first_name', 'last_name', 'middle_name', 'date_of_birth', 'gender', 'gender_id', 
            'phone_number', 'district', 'profile_picture', 'subscription', 'groups', 'email', 'inn'
        ]
        extra_kwargs = {
            'phone_number': {'read_only': True}
        }

    def update(self, instance, validated_data):
        # Удаляем поля, которые не должны обновляться
        validated_data.pop('subscription', None)
        validated_data.pop('groups', None)
        
        # Обновляем остальные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    

class CustomUserPublicSerializer(serializers.ModelSerializer):
    """Публичный сериализатор только для чтения с ограниченным набором полей"""
    gender = GenderSerializer()
    district = DistrictSerializer()

    class Meta:
        model = CustomUser
        fields = [
            'id', 'first_name', 'last_name', 'middle_name', 
            'gender', 'district','date_of_birth'
        ]
        read_only_fields = fields  


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