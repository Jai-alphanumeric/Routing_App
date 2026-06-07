from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Node, Edge, RouteQueryHistory

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['id', 'name']

class EdgeSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(slug_field='name', queryset=Node.objects.all())
    destination = serializers.SlugRelatedField(slug_field='name', queryset=Node.objects.all())

    class Meta:
        model = Edge
        fields = ['id', 'source', 'destination', 'latency']
        validators = [
            UniqueTogetherValidator(
                queryset=Edge.objects.all(),
                fields=['source', 'destination'],
                message="This edge already exists."
            )
        ]

    def validate_latency(self, value):
        if value <= 0:
            raise serializers.ValidationError("Latency must be greater than 0.")
        return value

class RouteQueryHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteQueryHistory
        fields = ['id', 'source_name', 'destination_name', 'total_latency', 'path', 'created_at']
