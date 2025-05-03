# serializers.py
from rest_framework import serializers
from .models import CustomUser
from django.utils import translation
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from a_base.serializers import DistrictSerializer, SubscriptionSerializer, GenderSerializer, GroupSerializer
from a_base.models import District, Gender

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    district = DistrictSerializer(read_only=True)
    gender = GenderSerializer(read_only=True)
    groups = GroupSerializer(many=True, read_only=True)
    subscription = SubscriptionSerializer(read_only=True)

    gender_id = serializers.PrimaryKeyRelatedField(
        queryset=Gender.objects.all(),
        source="gender",
        write_only=True,
        required=False,
        allow_null=True,
    )
    district_id = serializers.PrimaryKeyRelatedField(
        queryset=District.objects.all(),
        source="district",
        write_only=True,
        required=False,
        allow_null=True,
    )
    
    class Meta:
        model = CustomUser
        exclude = ['subscription_start_date', 'subscription_end_date', 
                   'confirmation_code', 'confirmation_code_created_at',
                   'user_permissions', 'is_staff', 'is_active', 'is_superuser', 
                   'last_login']
        extra_kwargs = {
            'password': {'write_only': True}
            }
        

    def get_gender(self, obj):
        if not obj.gender:
            return None
        return {
            "id": obj.gender.id,
            "name": obj.gender.name,
        }

    def get_district(self, obj):
        if not obj.district:
            return None
        return {
            "id": obj.district.id,
            "name": obj.district.name,
        }


    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr != 'subscription':
                setattr(instance, attr, value)
        
        instance.save()
        return instance


class CustomUserPrivateSerializer(CustomUserSerializer):
    pass

class CustomUserPublicSerializer(serializers.ModelSerializer):
    gender = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'gender', 'district']

    def get_gender(self, obj):
        return obj.gender.name if obj.gender else None

    def get_district(self, obj):
        return obj.district.name if obj.district else None


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