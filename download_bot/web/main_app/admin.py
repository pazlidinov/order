from django.contrib import admin
from .models import Customer


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id",  "username", "invited", "balance"]
    list_filter = ["invited", "balance"]
    list_display_links = ["id", "username"]
    list_per_page = 10
