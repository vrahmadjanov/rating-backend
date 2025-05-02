from django.test import TestCase
from django.utils.translation import activate, get_language
from modeltranslation.translator import translator
from a_base.models import SocialStatus


class SocialStatusModelTest(TestCase):
    """Test cases for SocialStatus model with translations"""

    @classmethod
    def setUpTestData(cls):
        # Create a test social status that will be used across all tests
        cls.status = SocialStatus.objects.create(
            name_ru='Студент',
            description_ru='Обучается в учебном заведении',
            name_tg='Донишҷӯ',
            description_tg='Дар муассисаи таҳсилӣ таҳсил мекунад'
        )

    def test_model_creation(self):
        """Test that SocialStatus instance is created properly"""
        self.assertEqual(SocialStatus.objects.count(), 1)
        status = SocialStatus.objects.first()
        self.assertEqual(status.name_ru, 'Студент')
        self.assertEqual(status.name_tg, 'Донишҷӯ')


    def test_name_uniqueness(self):
        """Test that name must be unique"""
        with self.assertRaises(Exception):
            SocialStatus.objects.create(
                name_ru='Студент',  # Duplicate Russian name
                name_tg='Новый студент'
            )

    def test_str_representation(self):
        """Test string representation uses current language"""
        # Test Russian
        activate('ru')
        self.assertEqual(str(self.status), 'Студент')
        
        # Test Tajik
        activate('tg')
        self.assertEqual(str(self.status), 'Донишҷӯ')

    def test_translation_fields(self):
        """Test that translation fields are properly registered"""
        translation_options = translator.get_options_for_model(SocialStatus)
        self.assertEqual(sorted(translation_options.fields), sorted(['name', 'description']))

    def test_description_optional(self):
        """Test that description can be blank/null"""
        status = SocialStatus.objects.create(name_ru='Без описания', name_tg='Беш тавсиф')
        self.assertIsNone(status.description_ru)
        self.assertIsNone(status.description_tg)

    def test_verbose_names(self):
        """Test model meta options (verbose names)"""
        self.assertEqual(SocialStatus._meta.verbose_name, 'Социальный статус')
        self.assertEqual(SocialStatus._meta.verbose_name_plural, 'Социальные статусы')

    def test_field_max_length(self):
        """Test name field max length constraint"""
        field = SocialStatus._meta.get_field('name_ru')
        self.assertEqual(field.max_length, 50)

    def test_translation_switching(self):
        """Test that language switching works correctly"""
        activate('ru')
        self.assertEqual(self.status.name, 'Студент')
        self.assertEqual(self.status.description, 'Обучается в учебном заведении')

        activate('tg')
        self.assertEqual(self.status.name, 'Донишҷӯ')
        self.assertEqual(self.status.description, 'Дар муассисаи таҳсилӣ таҳсил мекунад')