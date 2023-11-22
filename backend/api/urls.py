from django.urls import path, include
from .views import RegisterView, send_invitation, Profile, ChangePasswordView, Routes, logout_user, PasswordTokenCheckAPI, forgot_password
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'profile', Profile)

urlpatterns = [
    path('', views.Routes, name='routes'),
    path('register/',RegisterView.as_view(), name='register'),
    path('send_invitation/',send_invitation.as_view(), name='send_invitation'),
    path('login/', views.login_user, name='login'),
    path('logout/', logout_user.as_view(), name='logout'),
    path('user/', include(router.urls)),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('forgot_password/<str:uidb64>/<str:token>/', PasswordTokenCheckAPI.as_view(), name='forgot_password'),
    path('reset_password/', forgot_password.as_view(), name='reset_password'),
]

urlpatterns += router.urls
