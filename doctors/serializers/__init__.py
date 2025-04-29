# doctors/serializers/__init__.py
from .doctor import DoctorSerializer
from .doc_language import DoctorLanguageSerializer
from .education import EducationSerializer
from .schedule import ScheduleSerializer
from .workplace import WorkplaceSerializer

__all__ = [
    'DoctorSerializer',
    'DoctorLanguageSerializer',
    'EducationSerializer',
    'ScheduleSerializer',
    'WorkplaceSerializer',
]