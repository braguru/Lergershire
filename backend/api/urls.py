from django.urls import path, include
from .views import RegisterView, send_invitation, Profile, ChangePasswordView, NotificationView
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'profile', Profile)
router.register(r'notification', NotificationView)

urlpatterns = [
    path('register/',RegisterView.as_view(), name='register'),
    path('send_invitation/',send_invitation.as_view(), name='send_invitation'),
    path('login/', views.login_user, name='login'),
    path('user/', include(router.urls)),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    # path('notification/', views.NotificationView, name='notification'),
]

urlpatterns += router.urls