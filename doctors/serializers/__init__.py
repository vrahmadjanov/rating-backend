# doctors/serializers/__init__.py
from .doctor import DoctorSerializer, DoctorShortSerializer, DoctorCardSerializer
from .language import LanguageSerializer
from .education import EducationSerializer
from .medical_institution import MedicalInstitutionSerializer, MedicalInstitutionShortSerializer
from .schedule import ScheduleSerializer
from .workplace import WorkplaceSerializer, WorkplaceShortSerializer
from .specialty import SpecialtySerializers

__all__ = [
    'DoctorSerializer',
    'DoctorShortSerializer',
    'DoctorCardSerializer',
    'LanguageSerializer',
    'EducationSerializer',
    'MedicalInstitutionSerializer',
    'MedicalInstitutionShortSerializer',
    'ScheduleSerializer',
    'WorkplaceSerializer',
    'WorkplaceShortSerializer',
    'SpecialtySerializers'
]