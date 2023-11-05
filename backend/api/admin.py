from django.contrib import admin
from .models import User, InvitationEmail, login, Setting


# Register your models here.
admin.site.register(User)
admin.site.register(InvitationEmail)
admin.site.register(login)
admin.site.register(Setting)