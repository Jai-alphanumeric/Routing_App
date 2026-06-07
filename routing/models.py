from django.db import models
from django.core.validators import MinValueValidator

class Node(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Edge(models.Model):
    source = models.ForeignKey(Node, related_name='outgoing_edges', on_delete=models.CASCADE)
    destination = models.ForeignKey(Node, related_name='incoming_edges', on_delete=models.CASCADE)
    latency = models.FloatField(validators=[MinValueValidator(0.0001)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['source', 'destination'], name='unique_edge')
        ]

    def __str__(self):
        return f"{self.source.name} -> {self.destination.name} ({self.latency})"

class RouteQueryHistory(models.Model):
    source_name = models.CharField(max_length=255)
    destination_name = models.CharField(max_length=255)
    total_latency = models.FloatField()
    path = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.source_name} to {self.destination_name} at {self.created_at}"
