from django.contrib import admin

from .models import Application, Contact, Interview, StatusHistory


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 0


class InterviewInline(admin.TabularInline):
    model = Interview
    extra = 0


class StatusHistoryInline(admin.TabularInline):
    model = StatusHistory
    extra = 0
    readonly_fields = ["from_status", "to_status", "changed_at"]


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        "company_name",
        "role_title",
        "status",
        "priority",
        "owner",
        "applied_date",
    ]
    list_filter = ["status", "priority"]
    search_fields = ["company_name", "role_title"]
    inlines = [ContactInline, InterviewInline, StatusHistoryInline]
