from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('', views.flux, name='flux'),
    path('ask_critic', views.ask_critic, name='ask_critic'),
    path('create_critic', views.create_critic, name='create_critic'),
    path('answer_critic', views.answer_critic, name='answer_critic'),
    path('modify_critic', views.modify_critic, name='modify_critic'),
    path('modify_ask', views.modify_ask, name='modify_ask'),
    path('login', views.login_view, name='login_v'),
    path('logout', views.logout_view, name='logout_v'),
    path('signup', views.signup_view, name='signup_v'),
    ]

