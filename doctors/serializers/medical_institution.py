from a_base.serializers import DistrictSerializer, RegionSerializer
from .base import BaseMedicalInstitutionSerializer

class MedicalInstitutionSerializer(BaseMedicalInstitutionSerializer):
    district = DistrictSerializer()
    region = RegionSerializer()
    
    class Meta(BaseMedicalInstitutionSerializer.Meta):
        fields = [
            'id', 'name', 'institution_type', 'country', 'region', 
            'district', 'address', 'phone_number', 'email', 'website'
        ]

class MedicalInstitutionShortSerializer(BaseMedicalInstitutionSerializer):
    district = DistrictSerializer()
    
    class Meta(BaseMedicalInstitutionSerializer.Meta):
        fields = ['id', 'name', 'district', 'address']