from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import ApplicationFilter
from .models import Application, Contact, Interview, StatusHistory
from .serializers import (
    ApplicationDetailSerializer,
    ApplicationListSerializer,
    ContactSerializer,
    InterviewSerializer,
    StatusHistorySerializer,
)

STATUS_PROGRESSION = {
    "wishlist": "applied",
    "applied": "phone_screen",
    "phone_screen": "interview",
    "interview": "offer",
}


class ApplicationListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ApplicationListSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ApplicationFilter
    search_fields = ["company_name", "role_title"]
    ordering_fields = ["applied_date", "company_name", "updated_at"]
    ordering = ["-updated_at"]

    def get_queryset(self):
        return Application.objects.filter(owner=self.request.user).prefetch_related(
            "interviews", "contacts", "history"
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ApplicationDetailSerializer

    def get_queryset(self):
        return Application.objects.filter(owner=self.request.user).prefetch_related(
            "interviews", "contacts", "history"
        )


class AdvanceStageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        application = get_object_or_404(Application, pk=pk, owner=request.user)
        next_status = STATUS_PROGRESSION.get(application.status)
        if not next_status:
            return Response(
                {"detail": "Cannot advance from current status."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        application.status = next_status
        application.save()
        return Response(ApplicationDetailSerializer(application).data)


class StatusHistoryListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StatusHistorySerializer

    def get_queryset(self):
        application = get_object_or_404(
            Application, pk=self.kwargs["pk"], owner=self.request.user
        )
        return application.history.all()


class ContactListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer

    def get_application(self):
        return get_object_or_404(
            Application, pk=self.kwargs["pk"], owner=self.request.user
        )

    def get_queryset(self):
        return self.get_application().contacts.all()

    def perform_create(self, serializer):
        serializer.save(application=self.get_application())


class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer
    lookup_url_kwarg = "cid"

    def get_queryset(self):
        application = get_object_or_404(
            Application, pk=self.kwargs["pk"], owner=self.request.user
        )
        return application.contacts.all()


class InterviewListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InterviewSerializer

    def get_application(self):
        return get_object_or_404(
            Application, pk=self.kwargs["pk"], owner=self.request.user
        )

    def get_queryset(self):
        return self.get_application().interviews.all()

    def perform_create(self, serializer):
        serializer.save(application=self.get_application())


class InterviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InterviewSerializer
    lookup_url_kwarg = "iid"

    def get_queryset(self):
        application = get_object_or_404(
            Application, pk=self.kwargs["pk"], owner=self.request.user
        )
        return application.interviews.all()
