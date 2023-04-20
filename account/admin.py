from django.contrib import admin
from allauth.account.admin import EmailConfirmation


@admin.register(EmailConfirmation)
class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ("email_address", "created", "sent", "key")
    search_fields = ("email_adress",)
