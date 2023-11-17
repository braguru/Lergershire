from django.contrib import admin
from .models import User, InvitationEmail, Profile


# Register your models here.
admin.site.register(User)
admin.site.register(InvitationEmail)
admin.site.register(Profile)
