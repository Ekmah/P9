from django.urls import path

from . import views

urlpatterns = [
    path('', views.flux, name='flux'),
    path('posts', views.posts, name='posts'),
    path('ask_critic', views.ask_critic, name='ask_critic'),
    path('create_critic', views.create_critic, name='create_critic'),
    path('answer_critic/<int:ticket_id>', views.answer_critic,
         name='answer_critic'),
    path('modify_critic/<int:review_id>', views.modify_critic,
         name='modify_critic'),
    path('modify_ask/<int:ticket_id>', views.modify_ask, name='modify_ask'),
    path('follows', views.follows, name='follows'),
    path('login', views.login_view, name='login_v'),
    path('logout', views.logout_view, name='logout_v'),
    path('signup', views.signup_view, name='signup_v'),
    ]
