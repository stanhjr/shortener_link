from django.urls import path

from shortener import views

urlpatterns = [
    path('create-url/', views.CreateUrl.as_view(), name='create_url'),
    path('<str:shortened_part>', views.redirect_url_view, name='redirect')
]
