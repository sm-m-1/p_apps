from django.contrib import admin
from .models import UserEmail

# Register your models here.
@admin.register(UserEmail)
class EmailAdmin(admin.ModelAdmin):
    pass