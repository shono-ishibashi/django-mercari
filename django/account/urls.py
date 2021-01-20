from django.urls import include, path

from account.views import CreateUser, Login, logout_view

app_name = 'account'

urlpatterns = [
    path('register/', CreateUser.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]
