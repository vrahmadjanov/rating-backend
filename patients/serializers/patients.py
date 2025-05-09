from rest_framework import serializers
from patients.models import Patient
from core.serializers import CustomUserPublicSerializer, CustomUserPrivateSerializer
from a_base.serializers import SocialStatusSerializer
from a_base.models import Gender


class PatientPublicSerializer(serializers.ModelSerializer):
    user = CustomUserPublicSerializer()
    social_status = SocialStatusSerializer()

    class Meta:
        model = Patient
        fields = [
            'id', 'user', 'passport', 'registration_address',
            'actual_address', 'sin', 'eng', 'social_status',
        ]


class PatientPrivateSerializer(serializers.ModelSerializer):
    user = CustomUserPrivateSerializer()
    social_status = SocialStatusSerializer(read_only=True)

    gender_id = serializers.IntegerField(
        write_only=True, 
        allow_null=True, 
        required=False,
        min_value=1
    )

    # TODO gender_id передается некорректно. Нужно найти способ как передать gender_id в составе user:{}
    class Meta:
        model = Patient
        fields = [
            'id', 'user', 'passport', 'registration_address',
            'actual_address', 'sin', 'eng', 'social_status', 
            'gender_id',
        ]

    def validate_gender_id(self, value):
        if value is None:
            return None
        try:
            return Gender.objects.get(pk=value)
        except Gender.DoesNotExist:
            raise serializers.ValidationError(f"Gender with id {value} does not exist.")

    def update(self, instance, validated_data):
        # Обрабатываем gender_id до передачи в user serializer
        gender = validated_data.pop('gender_id', None)
        
        user_data = validated_data.pop('user', {})
        
        # Если был передан gender_id - обновляем его напрямую
        if gender is not None:
            instance.user.gender = gender
            instance.user.save()
        
        # Обновляем остальные поля пользователя
        if user_data:
            user_serializer = CustomUserPrivateSerializer(
                instance=instance.user,
                data=user_data,
                partial=True,
                context=self.context
            )
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        # Обновляем поля пациента
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
        