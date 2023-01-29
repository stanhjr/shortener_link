from django.db import models

from shortener.utils import create_random_code


class Url(models.Model):
    full_url = models.URLField(unique=True)
    short_url = models.URLField(unique=True, blank=True)
    life_time_at = models.DateTimeField(blank=True, null=True)

    @classmethod
    def get_shortened_url(cls):
        random_code = create_random_code()
        if cls.objects.filter(short_url=random_code).exists():
            return cls.get_shortened_url()
        return random_code

    def save(self, *args, **kwargs):
        self.short_url = self.get_shortened_url()
        return super().save(*args, **kwargs)
