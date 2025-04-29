from django.test import TestCase
from django.utils.translation import activate
from django.utils import translation
from a_base.models import Language, LanguageLevel
from a_base.serializers import LanguageSerializer, LanguageLevelSerializer


class LanguageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестовые данные один раз для всех тестов
        cls.language = Language.objects.create(
            name="Таджикский",
            name_ru="Таджикский",
            name_tg="Точикӣ"
        )

    def test_language_creation(self):
        """Тест создания объекта Language"""
        activate('ru')
        self.assertEqual(self.language.name, "Таджикский")
        self.assertEqual(self.language.name_ru, "Таджикский")
        self.assertEqual(self.language.name_tg, "Точикӣ")

    def test_language_str_method(self):
        """Тест метода __str__"""
        activate('ru')
        self.assertEqual(str(self.language), "Таджикский")

    def test_language_translations(self):
        """Тест перевода названия языка"""
        # Проверяем русский перевод
        activate('ru')
        self.assertEqual(self.language.name, "Таджикский")
        
        # Проверяем таджикский перевод
        activate('tg')
        self.assertEqual(self.language.name, "Точикӣ")

    def test_language_unique_constraint(self):
        """Тест уникальности названия языка"""
        with self.assertRaises(Exception):
            Language.objects.create(
                name="Таджикский",
                name_ru="Таджикский",
                name_tg="Точикӣ"
            )

class LanguageLevelModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестовые данные один раз для всех тестов
        cls.level = LanguageLevel.objects.create(
            level="Родной язык",
            level_ru="Родной язык",
            level_tg="Забони модарӣ"
        )

    def test_language_level_creation(self):
        """Тест создания объекта LanguageLevel"""
        activate('ru')
        self.assertEqual(self.level.level, "Родной язык")
        self.assertEqual(self.level.level_ru, "Родной язык")
        self.assertEqual(self.level.level_tg, "Забони модарӣ")

    def test_language_level_str_method(self):
        """Тест метода __str__"""
        activate('ru')
        self.assertEqual(str(self.level), "Родной язык")

    def test_language_level_translations(self):
        """Тест перевода уровня владения языком"""
        # Проверяем русский перевод
        activate('ru')
        self.assertEqual(self.level.level, "Родной язык")
        
        # Проверяем таджикский перевод
        activate('tg')
        self.assertEqual(self.level.level, "Забони модарӣ")

    def test_language_level_unique_constraint(self):
        """Тест уникальности уровня владения языком"""
        with self.assertRaises(Exception):
            LanguageLevel.objects.create(
                level="Родной язык",
                level_ru="Родной язык",
                level_tg="Забони модарӣ"
            )


class LanguageSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.language = Language.objects.create(
            name="Таджикский",
            name_ru="Таджикский",
            name_tg="Точикӣ"
        )

    def setUp(self):
        # Устанавливаем язык по умолчанию для тестов
        translation.activate('ru')

    def tearDown(self):
        # Сбрасываем язык после теста
        translation.deactivate()

    def test_serializer_fields(self):
        """Тест наличия полей в сериализаторе"""
        serializer = LanguageSerializer()
        self.assertEqual(set(serializer.fields.keys()), {'id', 'name'})

    def test_serializer_data_ru(self):
        """Тест данных сериализатора для русского языка"""
        translation.activate('ru')
        serializer = LanguageSerializer(self.language)
        expected_data = {
            'id': self.language.id,
            'name': 'Таджикский'
        }
        self.assertEqual(serializer.data, expected_data)

    def test_serializer_data_tg(self):
        """Тест данных сериализатора для таджикского языка"""
        translation.activate('tg')
        serializer = LanguageSerializer(self.language)
        expected_data = {
            'id': self.language.id,
            'name': 'Точикӣ'
        }
        self.assertEqual(serializer.data, expected_data)

    def test_serializer_data_fallback(self):
        """Тест fallback на русский язык при неизвестном языке"""
        translation.activate('en')  # Язык, для которого нет перевода
        serializer = LanguageSerializer(self.language)
        expected_data = {
            'id': self.language.id,
            'name': 'Таджикский'  # Должен вернуть русскую версию как fallback
        }
        self.assertEqual(serializer.data, expected_data)

    def test_serializer_data_no_translation(self):
        """Тест случая, когда нет перевода"""
        # Создаем объект без перевода
        language = Language.objects.create(name="Французский")
        translation.activate('tg')
        serializer = LanguageSerializer(language)
        self.assertEqual(serializer.data['name'], 'Французский')


class LanguageLevelSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.level = LanguageLevel.objects.create(
            level="Родной язык",
            level_ru="Родной язык",
            level_tg="Забони модарӣ"
        )

    def setUp(self):
        # Устанавливаем язык по умолчанию для тестов
        translation.activate('ru')

    def tearDown(self):
        # Сбрасываем язык после теста
        translation.deactivate()

    def test_serializer_fields(self):
        """Тест наличия полей в сериализаторе"""
        serializer = LanguageLevelSerializer()
        self.assertEqual(set(serializer.fields.keys()), {'id', 'level'})

    def test_serializer_data_ru(self):
        """Тест данных сериализатора для русского языка"""
        translation.activate('ru')
        serializer = LanguageLevelSerializer(self.level)
        expected_data = {
            'id': self.level.id,
            'level': 'Родной язык'
        }
        self.assertEqual(serializer.data, expected_data)

    def test_serializer_data_tg(self):
        """Тест данных сериализатора для таджикского языка"""
        translation.activate('tg')
        serializer = LanguageLevelSerializer(self.level)
        expected_data = {
            'id': self.level.id,
            'level': 'Забони модарӣ'
        }
        self.assertEqual(serializer.data, expected_data)

    def test_serializer_data_fallback(self):
        """Тест fallback на русский язык при неизвестном языке"""
        translation.activate('en')  # Язык, для которого нет перевода
        serializer = LanguageLevelSerializer(self.level)
        expected_data = {
            'id': self.level.id,
            'level': 'Родной язык'  # Должен вернуть русскую версию как fallback
        }
        self.assertEqual(serializer.data, expected_data)

    def test_serializer_data_no_translation(self):
        """Тест случая, когда нет перевода"""
        # Создаем объект без перевода
        level = LanguageLevel.objects.create(level="Профессиональный уровень")
        translation.activate('tg')
        serializer = LanguageLevelSerializer(level)
        self.assertEqual(serializer.data['level'], 'Профессиональный уровень')