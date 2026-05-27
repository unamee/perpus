from django.urls import include, path

from .views import dashboard, dashboard_metrics

urlpatterns = [
    path("", dashboard, name="reports_dashboard"),
    path("metrics/", dashboard_metrics, name="dashboard_metrics"),
]
