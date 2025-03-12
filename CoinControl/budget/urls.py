from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='home_page'),
    path('update_user', views.update_user_view, name='update_user'),
    path('login', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup'),
    path('delete_account', views.delete_account_view, name='delete_account'),
    path('logout', views.logout_view, name='logout'),
]