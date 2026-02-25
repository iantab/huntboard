from datetime import timedelta

from apps.applications.models import APPLICATION_STATUSES, Application, StatusHistory
from django.db.models import Count
from django.db.models.functions import TruncWeek
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        apps = Application.objects.filter(owner=request.user)
        total = apps.count()

        by_stage = {status: 0 for status, _ in APPLICATION_STATUSES}
        for row in apps.values("status").annotate(count=Count("id")):
            by_stage[row["status"]] = row["count"]

        responded = apps.filter(
            status__in=["phone_screen", "interview", "offer", "rejected", "closed"]
        ).count()
        response_rate = round(responded / total * 100, 1) if total > 0 else 0.0

        first_responses = StatusHistory.objects.filter(
            application__owner=request.user,
            to_status="phone_screen",
            application__applied_date__isnull=False,
        ).select_related("application")
        days_list = [
            (record.changed_at.date() - record.application.applied_date).days
            for record in first_responses
        ]
        avg_days_to_response = (
            round(sum(days_list) / len(days_list), 1) if days_list else None
        )

        return Response(
            {
                "total": total,
                "by_stage": by_stage,
                "response_rate": response_rate,
                "avg_days_to_response": avg_days_to_response,
            }
        )


class DashboardActivityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        twelve_weeks_ago = timezone.now() - timedelta(weeks=12)
        activity = (
            Application.objects.filter(
                owner=request.user, created_at__gte=twelve_weeks_ago
            )
            .annotate(week=TruncWeek("created_at"))
            .values("week")
            .annotate(count=Count("id"))
            .order_by("week")
        )
        return Response(list(activity))
