from django.urls import path
from authentication.views.register_view import register_view
from authentication.views.login_view import login_view
from authentication.views.logout_view import logout_view

from authentication.views.user_management_views import user_management_view, user_edit_view, user_delete_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('users/', user_management_view, name='user_management'),
    path('users/<int:user_id>/edit/', user_edit_view, name='user_edit'),
    path('users/<int:user_id>/delete/', user_delete_view, name='user_delete'),
]