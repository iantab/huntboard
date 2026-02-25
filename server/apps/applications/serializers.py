from rest_framework import serializers

from .models import Application, Contact, Interview, StatusHistory


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "name", "role", "email", "linkedin_url"]


class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ["id", "round_number", "interview_date", "format", "notes"]


class StatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusHistory
        fields = ["id", "from_status", "to_status", "changed_at"]


class ApplicationListSerializer(serializers.ModelSerializer):
    interview_count = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            "id",
            "company_name",
            "role_title",
            "location",
            "salary_min",
            "salary_max",
            "job_url",
            "status",
            "priority",
            "applied_date",
            "follow_up_date",
            "is_overdue",
            "notes",
            "interview_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_interview_count(self, obj):
        return obj.interviews.count()

    def get_is_overdue(self, obj):
        return obj.is_overdue


class ApplicationDetailSerializer(ApplicationListSerializer):
    contacts = ContactSerializer(many=True, read_only=True)
    interviews = InterviewSerializer(many=True, read_only=True)
    history = StatusHistorySerializer(many=True, read_only=True)

    class Meta(ApplicationListSerializer.Meta):
        fields = ApplicationListSerializer.Meta.fields + [
            "contacts",
            "interviews",
            "history",
        ]
