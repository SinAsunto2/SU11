from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='index'),
    path('challenges/' , views.challenges, name='challenges'),
    path('users_response/' , views.handle_user_response, name='users_response'),
    path('ranking/', views.ranking, name='ranking'),
    # path('profile/', views.edit_profile, name='edit_profile'),
    # path('users/' , views.users, name='users'),
    # path('profile/', views.profile, name='profile'),
]
