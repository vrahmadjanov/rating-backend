from rest_framework import serializers
from .models import Subscription, Advantage

class AdvantageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advantage
        fields = ['name']

class SubscriptionSerializer(serializers.ModelSerializer):
    advantages = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = [
            'id',
            'name',
            'description',
            'price',
            'duration_days',
            'advantages'
        ]

    def get_advantages(self, obj):
        """Получаем список названий преимуществ"""
        return obj.get_advantages_list()