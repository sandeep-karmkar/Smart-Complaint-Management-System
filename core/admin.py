from django.contrib import admin
from .models import Complaint


class ComplaintAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'user',
        'status'
    )

admin.site.register(
    Complaint,
    ComplaintAdmin
)