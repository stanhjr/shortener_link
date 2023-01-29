import datetime

from django.test import TestCase, RequestFactory
from django.utils import timezone

from shortener.models import Url
from shortener.views import CreateUrl, redirect_url_view


class ShortenerViewsTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.initial_link_obj = Url.objects.create(full_url='https://docs.djangoproject.com/',
                                                   life_time_at=timezone.now() + datetime.timedelta(days=90))

    def test_create_shortened_url(self):
        request = self.factory.post('/', {'full_url': 'https://docs.djangoproject.com/222'})
        response = CreateUrl.as_view()(request)
        self.assertEqual(response.status_code, 201)

    def test_update_shortened_url(self):
        request = self.factory.post('/', {'full_url': 'https://docs.djangoproject.com/'})
        response = CreateUrl.as_view()(request)
        self.assertEqual(response.status_code, 201)

    def test_redirect_shortener_status(self):
        request = self.factory.get('/')
        response = redirect_url_view(request, self.initial_link_obj.short_url)
        self.assertEqual(response.status_code, 302)

    def test_redirect_shortener_url(self):
        request = self.factory.get('/')
        response = redirect_url_view(request, self.initial_link_obj.short_url)
        self.assertEqual(response.url, 'https://docs.djangoproject.com/')
