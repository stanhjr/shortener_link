import datetime

from django.test import TestCase
from django.utils import timezone

from shortener.models import Url
from shortener.services import UrlService


class TestServices(TestCase):

    def setUp(self):
        self.initial_link_obj = Url.objects.create(full_url='https://docs.djangoproject.com/',
                                                   life_time_at=timezone.now() + datetime.timedelta(days=90))

    def test_check_instance(self):
        service = UrlService(full_url='https://docs.djangoproject.com/')
        instance = service.create_or_update_url()
        self.assertTrue(instance)

    def test_check_not_instance(self):
        service = UrlService(full_url='https://docs.djangoproject.com/22')
        instance = service.create_or_update_url()
        self.assertTrue(isinstance(instance, Url))

    def test_check_default_life_time(self):
        default_date_time = timezone.now() + datetime.timedelta(days=90)
        self.assertEqual(self.initial_link_obj.life_time_at.day, default_date_time.day)

    def test_get_life_time_date_time(self):
        life_time_days_numbers = 300
        default_date_time = timezone.now() + datetime.timedelta(days=life_time_days_numbers)
        service = UrlService(full_url='https://docs.djangoproject.com/22')
        self.assertNotEqual(service._get_life_time_date_time(life_time_days_numbers), default_date_time)

    def test_get_life_time_date_time_no_valid(self):
        life_time_days_numbers = 300
        default_date_time = timezone.now() + datetime.timedelta(days=life_time_days_numbers)
        service = UrlService(full_url='https://docs.djangoproject.com/22')
        self.assertNotEqual(service._get_life_time_date_time(100), default_date_time)

    def test_create_or_update_url_update(self):
        service = UrlService(full_url='https://docs.djangoproject.com/')
        instance = service.create_or_update_url()
        self.assertEqual(instance, self.initial_link_obj)

    def test_create_or_update_url_create(self):
        service = UrlService(full_url='https://docs.djangoproject.com/222')
        instance = service.create_or_update_url()
        self.assertNotEqual(instance, self.initial_link_obj)

    def test_create_or_update_url_update_date_time(self):
        service = UrlService(full_url='https://docs.djangoproject.com/', life_time_days_numbers=80)
        instance = service.create_or_update_url()
        default_date_time = timezone.now() + datetime.timedelta(days=90)
        self.assertEqual(instance.life_time_at.day, default_date_time.day)

    def test_create_or_update_url_update_date_time_2(self):
        service = UrlService(full_url='https://docs.djangoproject.com/', life_time_days_numbers=100)
        instance = service.create_or_update_url()
        default_date_time = timezone.now() + datetime.timedelta(days=100)
        self.assertEqual(instance.life_time_at.day, default_date_time.day)





