# doctors.models.schedule.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from doctors.models import Workplace
from datetime import datetime, time, timedelta
from typing import List, Optional, Tuple
from appointments.models import Appointment

class Schedule(models.Model):
    """Модель расписания работы врача с детальным недельным графиком.
    
    Позволяет настроить:
    - Рабочие часы для каждого дня недели отдельно
    - Длительность одного приема пациента
    - Гибкие настройки для разных графиков работы

    Relationships:
        workplace: OneToOne связь с местом работы врача (Workplace)

    Fields:
        Поля вида [day]_start/[day]_end: Время начала/окончания работы по дням недели
        appointment_interval: Длительность приема в минутах (15-360)
    """
    
    workplace = models.OneToOneField(
        Workplace,
        on_delete=models.CASCADE,
        related_name="schedule",
        verbose_name="Место работы",
        help_text="Связанное место работы врача в медицинском учреждении"
    )

    # Дни недели
    monday_start = models.TimeField(
        verbose_name="Понедельник - начало",
        blank=True, 
        null=True,
    )
    monday_end = models.TimeField(
        verbose_name="Понедельник - конец",
        blank=True,
        null=True,
    )
    
    # Аналогичные поля для других дней недели...
    tuesday_start = models.TimeField(verbose_name="Вторник - начало", blank=True, null=True)
    tuesday_end = models.TimeField(verbose_name="Вторник - конец", blank=True, null=True)
    wednesday_start = models.TimeField(verbose_name="Среда - начало", blank=True, null=True)
    wednesday_end = models.TimeField(verbose_name="Среда - конец", blank=True, null=True)
    thursday_start = models.TimeField(verbose_name="Четверг - начало", blank=True, null=True)
    thursday_end = models.TimeField(verbose_name="Четверг - конец", blank=True, null=True)
    friday_start = models.TimeField(verbose_name="Пятница - начало", blank=True, null=True)
    friday_end = models.TimeField(verbose_name="Пятница - конец", blank=True, null=True)
    saturday_start = models.TimeField(verbose_name="Суббота - начало", blank=True, null=True)
    saturday_end = models.TimeField(verbose_name="Суббота - конец", blank=True, null=True)
    sunday_start = models.TimeField(verbose_name="Воскресенье - начало", blank=True, null=True)
    sunday_end = models.TimeField(verbose_name="Воскресенье - конец", blank=True, null=True)

    appointment_interval = models.PositiveSmallIntegerField(
        verbose_name="Интервал приема",
        default=30,
        validators=[MinValueValidator(15), MaxValueValidator(360)],
        help_text="Длительность одного приема пациента в минутах (15-360)"
    )

    class Meta:
        verbose_name = "Расписание врача"
        verbose_name_plural = "Расписания врачей"
        ordering = ['workplace__doctor__user__last_name']

    def __str__(self) -> str:
        """Строковое представление в формате: Расписание [ФИО врача]"""
        return f"Расписание {self.workplace.doctor.user.get_full_name()}"

    def get_day_schedule(self, day_abbr: str) -> tuple[time | None, time | None]:
        """Возвращает временные границы работы для указанного дня.
        
        Args:
            day_abbr: Аббревиатура дня недели ('mon', 'tue', ..., 'sun')
            
        Returns:
            Кортеж (start_time, end_time) или (None, None) если не работает
            
        Raises:
            ValueError: Если передан некорректный код дня
            
        Example:
            >>> schedule.get_day_schedule('mon')
            (datetime.time(9, 0), datetime.time(18, 0))
        """
        day_map = {
            'mon': (self.monday_start, self.monday_end),
            'tue': (self.tuesday_start, self.tuesday_end),
            'wed': (self.wednesday_start, self.wednesday_end),
            'thu': (self.thursday_start, self.thursday_end),
            'fri': (self.friday_start, self.friday_end),
            'sat': (self.saturday_start, self.saturday_end),
            'sun': (self.sunday_start, self.sunday_end),
        }
        
        if day_abbr not in day_map:
            raise ValueError(f"Некорректный код дня: {day_abbr}. Используйте: {list(day_map.keys())}")
            
        return day_map[day_abbr]

    def is_working_day(self, day_abbr: str) -> bool:
        """Проверяет, работает ли врач в указанный день.
        
        Args:
            day_abbr: Аббревиатура дня недели ('mon', 'tue', ..., 'sun')
            
        Returns:
            True если врач работает в этот день, иначе False
        """
        start, end = self.get_day_schedule(day_abbr)
        return start is not None and end is not None
    
    def get_available_slots(self, date: datetime.date) -> List[Tuple[time, time]]:
        """Публичный метод для получения доступных слотов."""
        scheduler = AppointmentScheduler(self)
        return scheduler.get_available_slots(date)
    
    def is_time_slot_available(
        self,
        date: datetime.date,
        start_time: time,
        end_time: time
    ) -> bool:
        """Проверяет, доступен ли указанный временной слот для записи."""
        available_slots = self.get_available_slots(date)
        return (start_time, end_time) in available_slots

class AppointmentScheduler:
    """Сервис для расчета доступных временных слотов для записи к врачу."""
    
    def __init__(self, schedule: Schedule):
        self.schedule = schedule
        self.workplace = schedule.workplace
        self.doctor = self.workplace.doctor
    
    def get_available_slots(
        self, 
        date: datetime.date,
        duration: Optional[int] = None
    ) -> List[Tuple[time, time]]:
        """
        Возвращает список доступных временных слотов для записи на указанную дату.
        
        Args:
            date: Дата для поиска слотов
            duration: Длительность приема в минутах (если None - берется из расписания)
            
        Returns:
            Список кортежей (start_time, end_time) доступных слотов
        """
        day_abbr = date.strftime('%a').lower()[:3]  # 'mon', 'tue', etc.
        
        # Проверяем, работает ли врач в этот день
        if not self.schedule.is_working_day(day_abbr):
            return []
        
        # Получаем рабочие часы врача
        work_start, work_end = self.schedule.get_day_schedule(day_abbr)
        if not work_start or not work_end:
            return []
        
        # Определяем длительность приема
        interval = duration or self.schedule.appointment_interval
        interval_delta = timedelta(minutes=interval)
        
        # Получаем существующие записи на эту дату
        existing_appointments = Appointment.objects.filter(
            doctor=self.doctor,
            appointment_date=date,
            status=Appointment.Status.UPCOMING
        ).order_by('start_time')
        
        # Генерируем все возможные слоты в рабочие часы
        all_slots = self._generate_time_slots(work_start, work_end, interval_delta)
        
        # Исключаем занятые слоты
        available_slots = self._filter_available_slots(all_slots, existing_appointments)
        
        return available_slots
    
    def _generate_time_slots(
        self, 
        start_time: time, 
        end_time: time, 
        interval: timedelta
    ) -> List[Tuple[time, time]]:
        """Генерирует все возможные временные слоты в заданном диапазоне."""
        slots = []
        current_time = datetime.combine(datetime.today(), start_time)
        end_datetime = datetime.combine(datetime.today(), end_time)
        
        while current_time + interval <= end_datetime:
            slot_end = current_time + interval
            slots.append((
                current_time.time(),
                slot_end.time()
            ))
            current_time = slot_end
            
        return slots
    
    def _filter_available_slots(
        self, 
        all_slots: List[Tuple[time, time]], 
        appointments: List[Appointment]
    ) -> List[Tuple[time, time]]:
        """Фильтрует слоты, исключая уже занятые времена."""
        booked_slots = {
            (app.start_time, app.end_time)
            for app in appointments
        }
        
        return [
            slot for slot in all_slots
            if slot not in booked_slots
        ]