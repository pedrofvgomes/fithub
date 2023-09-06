from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authentication', views.authentication, name="authentication"),
    path('login', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup'),
    path('logout', views.logout_view, name='logout'),
    path('edit_profile/<int:user_id>', views.edit_profile, name='edit_profile'),
    path('user/<int:user_id>', views.user_info, name='user_info'),
    path('edit_nutrition/<int:user_id>', views.edit_nutrition, name='edit_nutrition'),
    path('clear/<int:user_id>', views.clear, name='clear'),
    path('addfood/<int:user_id>', views.add_food, name='add_food'),
    path('removefood/<int:log_id>', views.remove_food, name='remove_food'),
    path('addweight/<int:user_id>/<str:weight>', views.add_weight, name='add_weight'),
    path('removeweight/<int:user_id>', views.remove_weight, name='remove_weight')
]