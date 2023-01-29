import datetime
from django.utils import timezone

from shortener.models import Url


class UrlService:
    model = Url

    def __init__(self, full_url: str, life_time_days_numbers: int = 90, *args, **kwargs):
        self.full_url = full_url
        self.life_time = self._get_life_time_date_time(life_time_days_numbers)

    @staticmethod
    def _get_life_time_date_time(life_time_days_numbers: int) -> datetime:
        return timezone.now() + datetime.timedelta(days=life_time_days_numbers)

    def _check_instance(self):
        return self.model.objects.filter(full_url=self.full_url, life_time_at__gte=timezone.now()).first()

    @classmethod
    def get_full_url(cls, short_part: str):
        return cls.model.objects.filter(short_url=short_part, life_time_at__gte=timezone.now()).first().full_url

    def create_or_update_url(self) -> Url:
        instance = self._check_instance()
        if not instance:
            return self.model.objects.create(full_url=self.full_url,
                                             life_time_at=self.life_time,
                                             short_url=Url.get_shortened_url())
        if instance.life_time_at > self.life_time:
            return instance
        instance.life_time_at = self.life_time
        instance.save()
        return instance
