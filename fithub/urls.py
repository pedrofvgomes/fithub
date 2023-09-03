from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authentication', views.authentication, name="authentication"),
    path('login', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup'),
    path('logout', views.logout_view, name='logout'),
    path('edit_profile/<int:user_id>', views.edit_profile, name='edit_profile'),
    path('user/<int:user_id>', views.user_info, name='user_info')
]