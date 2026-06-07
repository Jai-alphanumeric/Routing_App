from rest_framework import generics, status, views
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .models import Node, Edge, RouteQueryHistory
from .serializers import (
    NodeSerializer,
    EdgeSerializer,
    RouteQueryHistorySerializer
)
from .services import find_shortest_path


class NodeListCreateView(generics.ListCreateAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

class NodeDestroyView(generics.DestroyAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

class EdgeListCreateView(generics.ListCreateAPIView):
    queryset = Edge.objects.all()
    serializer_class = EdgeSerializer

class EdgeDestroyView(generics.DestroyAPIView):
    queryset = Edge.objects.all()
    serializer_class = EdgeSerializer


class ShortestRouteView(views.APIView):
    def post(self, request, *args, **kwargs):
        source_name = request.data.get('source')
        destination_name = request.data.get('destination')

        if not source_name or not destination_name:
            return Response({"error": "Both 'source' and 'destination' fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        if not Node.objects.filter(name=source_name).exists():
            return Response({"error": f"Source node '{source_name}' does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if not Node.objects.filter(name=destination_name).exists():
            return Response({"error": f"Destination node '{destination_name}' does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        total_latency, path = find_shortest_path(source_name, destination_name)

        if path is None:
            return Response(
                {"error": f"No path exists between {source_name} and {destination_name}"},
                status=status.HTTP_404_NOT_FOUND
            )

        RouteQueryHistory.objects.create(
            source_name=source_name,
            destination_name=destination_name,
            total_latency=total_latency,
            path=path
        )

        return Response({
            "total_latency": total_latency,
            "path": path
        }, status=status.HTTP_200_OK)


class RouteQueryHistoryView(generics.ListAPIView):
    serializer_class = RouteQueryHistorySerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name='source', description='Filter by source node name', required=False, type=OpenApiTypes.STR),
            OpenApiParameter(name='destination', description='Filter by destination node name', required=False, type=OpenApiTypes.STR),
            OpenApiParameter(name='date_from', description='Filter by start date (YYYY-MM-DD)', required=False, type=OpenApiTypes.DATE),
            OpenApiParameter(name='date_to', description='Filter by end date (YYYY-MM-DD)', required=False, type=OpenApiTypes.DATE),
            OpenApiParameter(name='limit', description='Limit number of results', required=False, type=OpenApiTypes.INT),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = RouteQueryHistory.objects.all()
        query_params = self.request.query_params

        if source := query_params.get('source'):
            queryset = queryset.filter(source_name__iexact=source)
        if destination := query_params.get('destination'):
            queryset = queryset.filter(destination_name__iexact=destination)
        if date_from := query_params.get('date_from'):
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to := query_params.get('date_to'):
            queryset = queryset.filter(created_at__lte=date_to)

        limit = query_params.get('limit')
        if limit and limit.isdigit():
            queryset = queryset[:int(limit)]

        return queryset
