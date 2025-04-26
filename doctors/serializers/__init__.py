# doctors/serializers/__init__.py
from .doctor import DoctorSerializer
from .language import LanguageSerializer
from .education import EducationSerializer
from .schedule import ScheduleSerializer
from .workplace import WorkplaceSerializer

__all__ = [
    'DoctorSerializer',
    'LanguageSerializer',
    'EducationSerializer',
    'ScheduleSerializer',
    'WorkplaceSerializer',
]