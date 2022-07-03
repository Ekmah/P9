from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('', views.flux, name='flux'),
    path('login', views.login_view, name='login_v'),
    path('logout', views.logout_view, name='logout_v'),
    path('signup', views.signup_view, name='signup_v'),
    ]

