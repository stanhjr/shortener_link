from rest_framework import serializers

from core.settings import HOST_NAME
from shortener.models import Url
from shortener.services import UrlService


class UrlSerializer(serializers.ModelSerializer):
    life_time_days_numbers = serializers.IntegerField(required=False, min_value=1, max_value=365)
    full_url = serializers.URLField(required=True)

    class Meta:
        model = Url
        fields = ('full_url', 'life_time_days_numbers')

    def create(self, validated_data):
        url_service = UrlService(**validated_data)
        instance = url_service.create_or_update_url()
        return instance


class UrlResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = '__all__'

    def to_representation(self, instance):
        data = super(UrlResponseSerializer, self).to_representation(instance)
        data.update(short_url=f'{HOST_NAME}/{instance.short_url}')
        return data
