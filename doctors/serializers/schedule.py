# from rest_framework import serializers
# from ..models import Schedule

# class ScheduleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Schedule
#         fields = ['appointment_interval',
#                   'monday_start', 'monday_end',
#                   'tuesday_start', 'tuesday_end',
#                   'wednesday_start', 'wednesday_end',
#                   'thursday_start', 'thursday_end',
#                   'friday_start', 'friday_end',
#                   'saturday_start', 'saturday_end',
#                   'sunday_start', 'sunday_end']

#     def validate(self, data):
#         """Проверка временных диапазонов для каждого дня"""
#         days = [
#             ('monday', data.get('monday_start'), data.get('monday_end')),
#             ('tuesday', data.get('tuesday_start'), data.get('tuesday_end')),
#             ('wednesday', data.get('wednesday_start'), data.get('wednesday_end')),
#             ('thursday', data.get('thursday_start'), data.get('thursday_end')),
#             ('friday', data.get('friday_start'), data.get('friday_end')),
#             ('saturday', data.get('saturday_start'), data.get('saturday_end')),
#             ('sunday', data.get('sunday_start'), data.get('sunday_end')),
#         ]

#         for day, start, end in days:
#             if (start is None) != (end is None):
#                 raise serializers.ValidationError(
#                     {day: "Укажите оба времени или оставьте оба пустыми"}
#                 )
#             if start and end and start >= end:
#                 raise serializers.ValidationError(
#                     {day: "Время окончания должно быть позже времени начала"}
#                 )

#         # Проверка что есть хотя бы один рабочий день
#         if not any(start and end for _, start, end in days):
#             raise serializers.ValidationError(
#                 "Укажите хотя бы один рабочий день"
#             )

#         return data

#     def to_representation(self, instance):
#         """Форматирование вывода времени в HH:MM"""
#         representation = super().to_representation(instance)
        
#         # Форматируем все TimeField в HH:MM
#         for field in representation:
#             if field.endswith(('_start', '_end')) and representation[field]:
#                 representation[field] = representation[field][:5]
        
#         return representation