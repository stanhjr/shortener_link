from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response

from shortener.models import Url
from shortener.serializers import UrlSerializer, UrlResponseSerializer
from shortener.services import UrlService


class CreateUrl(generics.CreateAPIView):
    serializer_class = UrlSerializer
    queryset = Url.objects.all()
    response_serializer_class = UrlResponseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(self.response_serializer_class(instance).data, status=status.HTTP_201_CREATED, headers=headers)


def redirect_url_view(request, shortened_part):
    full_url = UrlService.get_full_url(shortened_part)
    if not full_url:
        raise Http404('Sorry this link is broken :(')
    return HttpResponseRedirect(full_url)
