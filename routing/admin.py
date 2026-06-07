from django.contrib import admin
from .models import Node, Edge, RouteQueryHistory

@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Edge)
class EdgeAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'destination', 'latency')
    list_filter = ('source', 'destination')
    search_fields = ('source__name', 'destination__name')

@admin.register(RouteQueryHistory)
class RouteQueryHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'source_name', 'destination_name', 'total_latency', 'created_at')
    list_filter = ('source_name', 'destination_name', 'created_at')
