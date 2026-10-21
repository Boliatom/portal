from django.urls import path

from . import views



urlpatterns = [
    path('login/', views.login),
    path('home/', views.home),
    path('users/<int:user_id>/', views.user_info),
    path('users/<int:user_id>/groups/', views.user_groups),
    path('groups/<int:group_id>/users/', views.group_users),
    path('check/', views.check_auth),
    path('modules/', views.module_list),
]
