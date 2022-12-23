from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('sign-in/', views.sign_in, name='sign-in'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('profile/', views.profile, name='profile'),
    path('sign-out/', views.sign_out, name='sign-out'),
    path('delete-user/', views.delete_user, name='delete-user')
]