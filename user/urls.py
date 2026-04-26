from django.contrib.auth.views import LogoutView
from django.urls import path

from user import views
from user.views import LoginUser, RegisterUser, check_username

app_name = 'user'

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    # path('profile/',),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('check_us/', views.check_username, name='check_username'),
    path('check_em/', views.check_email, name='check_email'),

]