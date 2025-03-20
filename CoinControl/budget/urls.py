from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='home_page'),
    path('update_user', views.update_user_view, name='update_user'),
    path('add_transaction', views.add_transaction, name='add_transaction'),
    path('update_transaction', views.update_transaction, name='update_transaction'),
    path('delete_transaction', views.delete_transaction, name='delete_transaction'),
    path('add_account', views.add_account, name='add_account'),
    path('update_account', views.update_account, name='update_account'),
    path('delete_account', views.delete_account, name='delete_account'),
    path('login', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup'),
    path('delete_user', views.delete_user_view, name='delete_user'),
    path('logout', views.logout_view, name='logout'),
]