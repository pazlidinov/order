from django.contrib import admin
from .models import Customer


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "telegram_id", "username", "invited", "balance"]
    list_filter = ["invited", "balance"]
    list_display_links = ["telegram_id", "username"]
    list_per_page = 10
