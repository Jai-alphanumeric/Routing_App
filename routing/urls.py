from django.urls import path
from .views import (
    NodeListCreateView,
    NodeDestroyView,
    EdgeListCreateView,
    EdgeDestroyView,
    ShortestRouteView,
    RouteQueryHistoryView
)
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        "message": "Welcome to the Network Route Optimization API!",
        "endpoints": ["/api/nodes/", "/api/edges/", "/api/routes/shortest/", "/api/routes/history/"]
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('nodes/', NodeListCreateView.as_view(), name='node-list-create'),
    path('nodes/<int:pk>/', NodeDestroyView.as_view(), name='node-destroy'),
    path('edges/', EdgeListCreateView.as_view(), name='edge-list-create'),
    path('edges/<int:pk>/', EdgeDestroyView.as_view(), name='edge-destroy'),
    path('routes/shortest/', ShortestRouteView.as_view(), name='route-shortest'),
    path('routes/history/', RouteQueryHistoryView.as_view(), name='route-history'),
]
