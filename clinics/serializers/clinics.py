from django.utils import translation
from rest_framework import serializers
from clinics.models import Clinic
from clinics.serializers import ClinicTypeSerializer
from a_base.serializers import DistrictSerializer
from django.conf import settings

class ClinicSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    clinic_type = ClinicTypeSerializer()
    district = DistrictSerializer()
    
    class Meta:
        model = Clinic
        fields = ['id', 'clinic_type', 'name', 'address', 'country', 'district', 
                  'phone_number', 'email', 'website', 'latitude', 'longitude']
    
    def get_name(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'name_{lang}', getattr(obj, f'name_{fallback_lang}', 'Нет перевода'))
    
    def get_address(self, obj):
        lang = translation.get_language()
        fallback_lang = settings.FALLBACK_LANGUAGES.get(lang, 'ru')
        return getattr(obj, f'address_{lang}', getattr(obj, f'address_{fallback_lang}', 'Нет перевода'))