from django.urls import path

from . import views

urlpatterns = [
    path("", views.ApplicationListCreateView.as_view(), name="application-list"),
    path(
        "<uuid:pk>/", views.ApplicationDetailView.as_view(), name="application-detail"
    ),
    path(
        "<uuid:pk>/advance/",
        views.AdvanceStageView.as_view(),
        name="application-advance",
    ),
    path(
        "<uuid:pk>/history/",
        views.StatusHistoryListView.as_view(),
        name="application-history",
    ),
    path(
        "<uuid:pk>/contacts/",
        views.ContactListCreateView.as_view(),
        name="contact-list",
    ),
    path(
        "<uuid:pk>/contacts/<uuid:cid>/",
        views.ContactDetailView.as_view(),
        name="contact-detail",
    ),
    path(
        "<uuid:pk>/interviews/",
        views.InterviewListCreateView.as_view(),
        name="interview-list",
    ),
    path(
        "<uuid:pk>/interviews/<uuid:iid>/",
        views.InterviewDetailView.as_view(),
        name="interview-detail",
    ),
]
